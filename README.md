# ![Openzyme](https://user-images.githubusercontent.com/9427089/205163968-380db264-57ef-459f-8d56-051a90b655fd.png)

## Goal: Catalyze computer aided protein design by...

1) Maintaining accessible comp bio infrastructure 
* Hardware intensive requirements for molecular simulation tooling creates a high initial barrier
  * Openzyme deploys open source and containerized workflows on a decentralized compute cluster to maximize accessibility while minimizing vendor lock-in

2) Implementing a high level and mockable interface for running comp bio workflows
* Long running time of tasks makes developing workflows slow
  * Openzyme will implement a mockable interface for all long running async tasks to make iterating pipeline logic as fast as possible

## Running workflows (Requires Docker)

1) Build Dockerized Bacalhau connection
```
$ sudo sysctl -w net.core.rmem_max=2500000  # Sometimes Bacalhau result downloads require higher rmem
$ docker build -t bacalhau .
$ docker run --name bacalhau -v bacalhauvol:/bacalhau-main -dt bacalhau
```

2) Use Bacalhau container to submit workflows
```
$ docker exec -it bacalhau ./bacalhau docker run --gpu=1 -o output:/code/output openzyme/compbio:a0.2 python workflows/simulate-protein.py
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

3) Download results to local file sytem
```
$ docker exec -it bacalhau ./bacalhau get <job-id>
$ docker cp bacalhau:/go/bacalhau-main/<short-job-id> $PWD/tmp/
```

## Compbio Local Dev (Requires GPU and Docker Nvidia)
1) Build compbio image
```
$ docker build -t compbio -f ./compbio/Dockerfile ./compbio/
```

2) Check that GPU platform is available
```
$ docker run --gpus all compbio python -m openmm.testInstallation
```

3) Run a molecular simulation locally
```
$ docker run --gpus all -v $PWD/compbio/output:/code/output compbio python workflows/simulate-protein.py
```

Output files appear in compbio/output after the docker run finishes
