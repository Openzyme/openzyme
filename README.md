# Barge
### Shipping Containerized Workflows for DeSci

## Compbio Local Dev
1) Build compbio image
```
$ docker build -t compbio -f ./compbio/Dockerfile ./compbio/
```

2) Optional Check if GPU Platform is available
```
$ docker run compbio python -m openmm.testInstallation
```

## Bacalhau Jobs
1) Build Dockerized Bacalhau Connection
```
$ sysctl -w net.core.rmem_max=2500000  # Sometimes bacalhau downloads require higher rmem
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

## Remote Dev Setup
Recommend using VSCodes SSH tool with an AWS P2 instance

Directions to set up docker for GPUs
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker
