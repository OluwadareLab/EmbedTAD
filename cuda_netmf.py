import numpy as np
# import networkx as nx
import cugraph
import cupy as cp
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from cuda_estimator import Estimator
import utils


class NetMF(Estimator):
    r"""An implementation of `"NetMF" <https://keg.cs.tsinghua.edu.cn/jietang/publications/WSDM18-Qiu-et-al-NetMF-network-embedding.pdf>`_
    from the WSDM '18 paper "Network Embedding as Matrix Factorization: Unifying
    DeepWalk, LINE, PTE, and Node2Vec". The procedure uses sparse truncated SVD to
    learn embeddings for the pooled powers of the PMI matrix computed from powers
    of the normalized adjacency matrix.

    Args:
        dimensions (int): Number of embedding dimension. Default is 32.
        iteration (int): Number of SVD iterations. Default is 10.
        order (int): Number of PMI matrix powers. Default is 2.
        negative_samples (in): Number of negative samples. Default is 1.
        seed (int): SVD random seed. Default is 42.
    """

    def __init__(
        self,
        dimensions: int = 32,
        iteration: int = 10,
        order: int = 2,
        negative_samples: int = 1,
        seed: int = 42,
    ):
        self.dimensions = dimensions
        self.iterations = iteration
        self.order = order
        self.negative_samples = negative_samples
        self.seed = seed

    def _create_D_inverse(self, graph):
        """
        Creating a sparse inverse degree matrix.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be embedded.

        Return types:
            * **D_inverse** *(Scipy array)* - Diagonal inverse degree matrix.
        """
        offsets, indices, weights = graph.view_adj_list()
        num_vertices = offsets.size - 1
        g_degrees = graph.in_degree()
        vertices = g_degrees.vertex.values
        degrees = g_degrees.degree.values

        values = cp.zeros(num_vertices)
        for node in range(num_vertices):
            di = cp.where(vertices == node)[0]
            if len(di) > 0:
                degree_index = di[0]
                values[node] = 1.0 / degrees[degree_index]
        values = cp.asnumpy(values)
                        
        # values = np.array(
        #     [1.0/g_degrees[g_degrees['vertex'] == node]['degree'].iloc[0] for node in range(graph.number_of_vertices())]
        # )
        index = np.arange(num_vertices)
        shape = (num_vertices, num_vertices)
        D_inverse = sparse.coo_matrix((values, (index, index)), shape=shape)
        return D_inverse

    def _create_base_matrix(self, graph: cugraph.Graph):
        """
        Creating the normalized adjacency matrix.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be embedded.

        Return types:
            * **(A_hat, A_hat, A_hat, D_inverse)** *(SciPy arrays)* - Normalized adjacency matrices.
        """
        A = cp.asnumpy(utils.get_adjacency_matrix(graph=graph))
        D_inverse = self._create_D_inverse(graph).toarray()
        A_hat = D_inverse.dot(A)
        return (A_hat, A_hat, A_hat, D_inverse)

    def _create_target_matrix(self, graph):
        """
        Creating a log transformed target matrix.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be embedded.

        Return types:
            * **target_matrix** *(SciPy array)* - The shifted PMI matrix.
        """
        A_pool, A_tilde, A_hat, D_inverse = self._create_base_matrix(graph)
        for _ in range(self.order - 1):
            A_tilde = sparse.coo_matrix(A_tilde.dot(A_hat))
            A_pool = A_pool + A_tilde
        A_pool = (graph.number_of_edges() * A_pool) / (
            self.order * self.negative_samples
        )
        A_pool = sparse.coo_matrix(A_pool.dot(D_inverse))
        A_pool.data[A_pool.data < 1.0] = 1.0
        target_matrix = sparse.coo_matrix(
            (np.log(A_pool.data), (A_pool.row, A_pool.col)),
            shape=A_pool.shape,
            dtype=np.float32,
        )
        return target_matrix

    def _create_embedding(self, target_matrix):
        """
        Fitting a truncated SVD embedding of a PMI matrix.
        """
        svd = TruncatedSVD(
            n_components=self.dimensions, n_iter=self.iterations, random_state=self.seed
        )
        svd.fit(target_matrix)
        embedding = svd.transform(target_matrix)
        return embedding

    def fit(self, graph: cugraph.Graph):
        """
        Fitting a NetMF model.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be embedded.
        """
        self._set_seed()
        graph = self._check_graph(graph)
        target_matrix = self._create_target_matrix(graph)
        self._embedding = self._create_embedding(target_matrix)

    def get_embedding(self) -> np.array:
        r"""Getting the node embedding.

        Return types:
            * **embedding** *(Numpy array)* - The embedding of nodes.
        """
        return self._embedding