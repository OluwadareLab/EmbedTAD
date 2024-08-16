import cupy as cp
import cugraph

def get_adjacency_matrix(graph: cugraph.Graph):
        offsets, indices, weights = graph.view_adj_list()
        num_vertices = offsets.size - 1
        adj_matrix = cp.zeros((num_vertices, num_vertices), dtype=cp.float64)

        for i in range(num_vertices):
            for j in range(offsets[i], offsets[i + 1]):
                adj_matrix[i, indices[j]] = weights[j] if weights is not None else 0.0

        return adj_matrix