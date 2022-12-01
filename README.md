# ![Openzyme](https://user-images.githubusercontent.com/9427089/205163968-380db264-57ef-459f-8d56-051a90b655fd.png)

### Make Molecular Machines

## Compbio Local Dev
1) Build compbio image
```
$ docker build -t compbio -f ./compbio/Dockerfile ./compbio/
```

2) Check that GPU Platform is available
```
$ docker run --gpus all compbio python -m openmm.testInstallation
```

2) Run a Molecular Simulation Locally
```
$ docker run --gpus all -v $PWD/compbio/output:/code/output compbio python workflows/simulate-protein.py
```
Output files should appear in compbio/output after the docker run finishes

3) (Optional) Deploy Code Changes
```
$ docker tag compbio openzyme/compbio:a0.2
$ docker push openzyme/compbio:a0.2
```

## Bacalhau Jobs
1) Build Dockerized Bacalhau Connection
```
$ sudo sysctl -w net.core.rmem_max=2500000  # Sometimes bacalhau downloads require higher rmem
$ docker build -t bacalhau .
$ docker run --name bacalhau -v bacalhauvol:/bacalhau-main -dt bacalhau
```

To shut down the container
```
$ docker stop bacalhau
$ docker container rm bacalhau
```

2) (Optional) Make Sure Bacalhau Connection Works
```
$ docker exec -it bacalhau ./bacalhau docker run ubuntu echo hello
```

You should see an output similiar to below
```
Job successfully submitted. Job ID: df0aed15-c930-4b1f-bedb-c2baeb6092eb
Checking job status... (Enter Ctrl+C to exit at any time, your job will continue running):

               Creating job for submission ... done ✅
               Finding node(s) for the job ... done ✅
                     Node accepted the job ... done ✅
           Job finished, verifying results ... done ✅
              Results accepted, publishing ... Job Results By Node:

To download the results, execute:
  bacalhau get df0aed15-c930-4b1f-bedb-c2baeb6092eb

To get more details about the run, execute:
  bacalhau describe df0aed15-c930-4b1f-bedb-c2baeb6092eb
```

Run the following to download results onto to local filesytem (replace id with your job id)
```
$ docker exec -it bacalhau ./bacalhau get df0aed15-c930-4b1f-bedb-c2baeb6092eb
$ docker cp bacalhau:/go/bacalhau-main/job-79ec2e3d $PWD/tmp/
```

## Run a Molecular Simulation in Bacalhau
```
$ docker exec -it bacalhau ./bacalhau docker run --gpu=1 -o output:/code/output openzyme/compbio:a0.2 python workflows/simulate-protein.py
$ docker exec -it bacalhau ./bacalhau get <job_id>
```

## Next Steps
* Change structure-to-trajectory.py 
* Have create-protein-trajectory.py download all result files to output
* Pass in PDB files as input through IPFS
* Pass in params as json file through IPFS
* Add alphafold with defaul weights to container
* Add amino-acid-to-structure.py
* Add amino-acid-to-trajectory.py

## Remote Dev Setup
Recommend using VSCodes SSH tool with an AWS P2 instance

Directions to set up docker for GPUs
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker
