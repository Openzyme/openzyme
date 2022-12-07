# ![Openzyme](https://user-images.githubusercontent.com/9427089/205163968-380db264-57ef-459f-8d56-051a90b655fd.png)

## Goal: Catalyze computer aided protein design by...

1) Maintaining accessible comp bio infrastructure 
* Hardware intensive requirements for molecular simulation tooling creates a high initial barrier.
  * Openzyme deploys open source and containerized workflows on a decentralized compute cluster to maximize accessibility while minimizing vendor lock-in.

2) Implementing a high level and mockable interface for running comp bio workflows
* Long running time of tasks makes developing workflows slow.
  * Openzyme will implement a mockable interface for all long running async tasks to make iterating pipeline logic as fast as possible.

## Quickstart Example
Requirements: [Docker](https://docs.docker.com/engine/install/ubuntu/#installation-methods)

1) Clone the repository
```
$ git clone git@github.com:Openzyme/openzyme.git
$ cd openzyme
```

2) Start Dockerized Bacalhau interface
```
$ docker run --name bacalhau -v $PWD/bacalhau/results:/go/bacalhau-main/results -dt openzyme/bacalhau:v1.0
```

2) Run Dockerized IPFS service
```
$ docker run -d --name ipfs_host -v $PWD/ipfs/staging/:/export -v $PWD/ipfs/data:/data/ipfs -p 4001:4001 -p 4001:4001/udp -p 127.0.0.1:8080:8080 -p 127.0.0.1:5001:5001 ipfs/kubo:latest
```

3) Create input JSON file
```
$ export sequence="MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
$ echo {\"sequence\":\"$sequence\"} > ./ipfs/staging/inputs/inputs.json
```

4) Pin input to IPFS
```
docker exec ipfs_host ipfs add -r export/inputs/
```

You should see an about similar to below:
```
254 B / 254 B  100.00%
added Qmcm8XNvNrXfyp7nAjdBmBV5NhMNKzjctVvmmKmkRxrNsY inputs/inputs.json
added QmNjgY8xXJ1ZiFe8iMkJ21PWcdJj63zn8L2hcGFW5XMPTk inputs
254 B / 254 B  100.00%
```

The second CID for the directory is used as an input in the next step.

5) Use Bacalhau to run job on IPFS input
Change ```inputcid``` to match the content identifier (CID) output from the step above. Make sure to use the directory CID and not the file CID.
This step can take a couple minutes to calculate. To, utilize the best perk of computer science and take a break as the computer works.
```
$ export inputcid=QmNjgY8xXJ1ZiFe8iMkJ21PWcdJj63zn8L2hcGFW5XMPTk
$ docker exec -it bacalhau ./bacalhau docker --gpu 1 --memory 30gb run --inputs $inputcid openzyme/compbio:a0.3 python ./workflows/fold-protein.py
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
  ./bacalhau get 3ba00839-b8bf-4558-9e6b-f1ab51badd1e

To get more details about the run, execute:
  ./bacalhau describe 3ba00839-b8bf-4558-9e6b-f1ab51badd1e
```

6) Download the results locally
```
$ export jobid=3ba00839-b8bf-4558-9e6b-f1ab51badd1e  # change to match your job id output
$ mkdir ./bacalhau/results/$jobid
$ docker exec -it bacalhau ./bacalhau get --output-dir results/$jobid $jobid
```
Result data is now in /bacalhau/results/$jobid

If you get an error about not enough connection memory try the below command:
```
$ sudo sysctl -w net.core.rmem_max=2500000  # Sometimes Bacalhau result downloads require higher rmem
```

If the job fails, run the following for debug logs:
```
docker exec -it bacalhau ./bacalhau describe $jobid
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