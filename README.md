# EmbedTAD
***
#### [OluwadareLab, University of Colorado, Colorado Springs](https://uccs-bioinformatics.com/)
***
#### Developers:

H M A Mohit Chowdhury<br>
Department of Computer Science<br>
University of Colorado Colorado Springs<br>
Email: hchowdhu@uccs.edu<br>
<br>

#### Contact:

Dr. Oluwatosin Oluwadare <br>
Department of Computer Science <br>
University of Colorado, Colorado Springs <br>
Email: ooluwada@uccs.edu <br>
***


#### Required packages
cupy-cuda12x
cugraph-cu12 --extra-index-url=https://pypi.nvidia.com
tqdm==4.65.0
networkx==3.4.2
pandas==2.0.3
numpy==1.24.4
scipy==1.15.1
scikit-learn==1.6.1
seaborn==0.13.2

#### Pip install 
Install requirements one by one or run requirements.txt

#### Docker

#### Parameters
-i or --input: nxn matrix file. (Required)
-r or --resolution: Resolution of the nxn matrix such as 5000 for 5Kb, 10000 for 10Kb (Required)
-o or --output: output file name without extension (Required)
-w or --worker: which version you want to use (OPTIONAL). Available option: CPU, GPU. Default: GPU
-n or --normalization: if you want to normalize your input matrix with Gaussian Filter (OPTIONAL). Available option: True, False. Default: True
