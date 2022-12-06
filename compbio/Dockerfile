
FROM nvidia/cuda:11.0.3-base-ubuntu20.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
RUN conda --version
RUN conda install -c conda-forge openmm cudatoolkit
RUN conda install -c conda-forge mdtraj
RUN conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia

RUN export PATH=“/root/miniconda3/bin:$PATH”
RUN pip install fair-esm 
RUN pip install "fair-esm[esmfold]"
RUN apt-get update && apt-get install -y git g++
RUN pip install 'dllogger @ git+https://github.com/NVIDIA/dllogger.git'
RUN pip install 'openfold @ git+https://github.com/aqlaboratory/openfold.git@4b41059694619831a7db195b7e0988fc4ff3a307'
RUN pip install biotite

COPY ./download.py ./download.py
RUN python download.py

COPY ./tests/2dri-processed.pdb ./
COPY ./workflows ./workflows