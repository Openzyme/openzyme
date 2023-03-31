## Goal: Catalyze computer aided protein design by...

1) Maintaining accessible comp bio infrastructure 
* Hardware intensive requirements for molecular simulation tooling creates a high initial barrier.
  * Openzyme deploys open source and containerized workflows on a decentralized compute cluster to maximize accessibility while minimizing vendor lock-in.

2) Implementing a high level and mockable interface for running comp bio workflows
* Long running time of tasks makes developing workflows slow.
  * Openzyme will implement a mockable interface for all long running async tasks to make iterating pipeline logic as fast as possible.

## Quickstart Example
Requirements: [Docker](https://docs.docker.com/engine/install/ubuntu/#installation-methods)

1) Install the Bacalhau command line interface
```
curl -sL https://get.bacalhau.org/install.sh | bash
```

2) Submit Bacalhau job with input amino acid sequence


Change the following to any amino acid sequence of interest.
```
export sequence="MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
```

```
bacalhau docker --gpu 1 --memory 30gb run openzyme/compbio:a0.3 python ./workflows/fold-protein.py $sequence
```

You should see an output similar to below:
```
Job successfully submitted. Job ID: 3ba00839-b8bf-4558-9e6b-f1ab51badd1e
Checking job status... (Enter Ctrl+C to exit at any time, your job will continue running):

               Creating job for submission ... done ✅
               Finding node(s) for the job ... done ✅
                     Node accepted the job ... done ✅
           Job finished, verifying results ... done ✅
              Results accepted, publishing ... Job Results By Node:

To download the results, execute:
  bacalhau get 3ba00839-b8bf-4558-9e6b-f1ab51badd1e

To get more details about the run, execute:
  bacalhau describe 3ba00839-b8bf-4558-9e6b-f1ab51badd1e
```

3) Download the results locally
```
bacalhau get <job-id>
```

You should see an output similar to below
```
Fetching results of job '8dcb1258-32d0-4cd0-a27f-e4d8910f02a4'...
Results for job '8dcb1258-32d0-4cd0-a27f-e4d8910f02a4' have been written to...
/home/ubuntu/job-8dcb1258
```

If the job fails, run the following for debug information:
```
bacalhau bacalhau describe <job-id>
```

If you recieve a buffer size error try the following:
```
sudo sysctl -w net.core.rmem_max=2500000  # Sometimes Bacalhau result downloads require higher rmem
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
$ docker run --gpus all -v $PWD/compbio/outputs:/outputs compbio python workflows/simulate-protein.py
```

Output files appear in compbio/output after the docker run finishes.

## Deploy Code Changes (requires Dockerhub account)
Change openzyme to your own Dockerhub account to deploy changes.
```
$ docker build -t compbio -f ./compbio/Dockerfile ./compbio/
$ docker tag compbio openzyme/compbio:a0.2
$ docker push openzyme/compbio:a0.2  # change to your own Dockerhub
```
