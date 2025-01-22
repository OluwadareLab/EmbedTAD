# EmbedTAD
***
### [OluwadareLab, University of Colorado, Colorado Springs](https://uccs-bioinformatics.com/)
***
### Developers:

H M A Mohit Chowdhury<br>
Department of Computer Science<br>
University of Colorado Colorado Springs<br>
Email: hchowdhu@uccs.edu<br>
<br>

### Contact:

Dr. Oluwatosin Oluwadare <br>
Department of Computer Science <br>
University of Colorado, Colorado Springs <br>
Email: ooluwada@uccs.edu <br>
***

## Installation
We provided GPU and CPU implementation of EmbedTAD. We recommand to use **Python 3.12** and the following packages with the mentioned version. We recommand to use Docker images from our remote repository.

### GPU
#### Required packages
We recommand to use Python 3.12 and the following packages with the mentioned version.

* cupy-cuda12x==13.3.0
* cugraph-cu12 --extra-index-url=https://pypi.nvidia.com
* pandas==2.0.3
* scipy==1.15.1
* scikit-learn==1.6.1
* tqdm==4.65.0
* seaborn==0.13.2

Optional: for converting *.hic/.cool* files into nXn matrix.
* hic-straw==1.3.1
* cooler==0.10.3

#### Pip
1. First clone the git repository
   ```
   git clone https://github.com/OluwadareLab/EmbedTAD.git
   cd EmbedTAD
   ```
2. Run the following command to install all the pip packages.
   ```
   python3 -m pip install -r requirements.txt
   ``` 

#### Conda
1. First clone the git repository
   ```
   git clone https://github.com/OluwadareLab/EmbedTAD.git
   cd EmbedTAD
   ```
2. Run the following command to create conda environment with all dependencies.
   ```
   conda env create -f environment.yml
   ``` 
3. Activate conda environment
   ```
   conda activate embedtad
   ```

#### Docker
1. You can build EmbedTAD docker image locally or you can pull form our remote Repository
    * Build image in local
        1. Clone git repository
        ```
        git clone https://github.com/OluwadareLab/EmbedTAD.git
        cd EmbedTAD
        ```
        2. Build docker image 
        ```
        docker build -t embedtad .
        ```
    * Clone image from remote
        1. Clone EmbedTAD image from our docker repository
        ```
        docker pull oluwadarelab/embedtad:latest
        ```
2. Run the EmbedTAD container and mount the present working directory to the container using 
   ```
   docker run -itd --gpus all --privileged -v ${PWD}:${PWD} --name embedtad embedtad:latest
   ```
3. Enter into EmbedTAD container using 
   ```
   docker exec -it embedtad bash
   ```
4. Install packages
   ```
   python3 -m pip install -r requirements.txt
   ```

### CPU
#### Required packages
We recommand to use Python 3.12 and the following packages with the mentioned version.

* pandas
* scipy==1.15.1
* scikit-learn==1.6.1
* tqdm==4.65.0
* seaborn==0.13.2
* networkx==3.4.2

Optional: for converting *.hic/.cool* files into nXn matrix.
* hic-straw==1.3.1
* cooler==0.10.3

#### Pip
1. First clone the git repository
   ```
   git clone https://github.com/OluwadareLab/EmbedTAD.git
   cd EmbedTAD
   ```
2. Run the following command to install all the pip packages..
   ```
   python3 -m pip install -r requirements.cpu.txt
   ``` 

#### Conda
1. First clone the git repository
   ```
   git clone https://github.com/OluwadareLab/EmbedTAD.git
   cd EmbedTAD
   ```
2. Run the following command to create conda environment with all dependencies.
   ```
   conda env create -f environment.cpu.yml
   ``` 
3. Activate conda environment
   ```
   conda activate embedtad_cpu
   ```

#### Docker
1. You can build EmbedTAD docker image locally or you can pull form our remote Repository
    * Build image in local
        1. Clone git repository
        ```
        git clone https://github.com/OluwadareLab/EmbedTAD.git
        cd EmbedTAD
        ```
        2. Build docker image 
        ```
        docker build -f Dockerfile.cpu -t embedtad:cpu .
        ```
    * Clone image from remote
        1. Clone EmbedTAD image from our docker repository
        ```
        docker pull oluwadarelab/embedtad:cpu
        ```
2. Run the EmbedTAD container and mount the present working directory to the container using 
   ```
   docker run -itd -v ${PWD}:${PWD} --name embedtad_cpu embedtad:cpu
   ```
3. Enter into EmbedTAD container using 
   ```
   docker exec -it embedtad_cpu bash
   ```
4. Install packages
   ```
   python3 -m pip install -r requirements.cpu.txt
   ```

## Run EmbedTAD
### Parameters
* -i or --input: nXn matrix file (Required). 
* -r or --resolution: Resolution of the nXn matrix such as 5000 for 5Kb, 10000 for 10Kb (Required).
* -o or --output: output file name without extension (Required).
* -w or --worker: which version you want to use (OPTIONAL). Available option: CPU, GPU. Default: GPU
* -n or --normalization: if you want to normalize your input matrix with Gaussian Filter (OPTIONAL). Available option: True, False. Default: True
* -h or --help: show the available parameters.

```
python3 embedtad.py --input input_matrix.txt --output output --resolution 10000 --worker GPU --normalization True
```

### Example with our provided data:
1. Unzip example data
```
cd test
unzip gm12878_10k_chr21.txt.zip
cd ..
```
2. Run GPU or CPU implementation
    * GPU
        ```
        python3 embedtad.py --input ./test/gm12878_combined_10000_chr21.txt --output ./test/embedtad_gm12878_combined_10000_chr21 --resolution 10000 --worker GPU --normalization True
        ```
    * CPU
        ```
        python3 embedtad.py --input ./test/gm12878_combined_10000_chr21.txt --output ./test/embedtad_gm12878_combined_10000_chr21 --resolution 10000 --worker CPU --normalization True
        ```
3. Observe results
```
cd test
```


## Output
* <*>.bed (BED-like) file contains TAD regions as follows-

| Start (bin) | Start | End (bin) | End | Count (bin) |
|-------|-------------|-----|-----------|------------|
| 945   | 9440000     | 955 | 9550000   | 11         |
| 968   | 9670000     | 983 | 9830000   | 16         |
| 988   | 9870000     | 1007| 10070000  | 20         |
| 1011  | 10100000    | 1069| 10690000  | 59         |
| 1084  | 10830000    | 1101| 11010000  | 18         |
| 1121  | 11200000    | 1434| 14340000  | 314        |
| 1436  | 14350000    | 1520| 15200000  | 85         |
| 1521  | 15200000    | 1530| 15300000  | 10         |
| 1531  | 15300000    | 1541| 15410000  | 11         |
| 1542  | 15410000    | 1552| 15520000  | 11         |

* <*>_tq.txt file contains TAD Quality score.
* <*>.png file is the visualizstion of first few TADs.
