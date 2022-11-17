# Barge
### We ship containerized workflows for DeSci

## Local Dev (GPU needed for best results)
1) Run Local Bacalhau cluster
```
$ docker build -t bacalhau .

$ docker run --name bacalhau -d bacalhau

$ export BACALHAU_API_HOST=127.0.0.1
$ export BACALHAU_API_PORT=20000
```

2) (Optional) Make Sure Cluster is Running
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
$ docker cp bacalhau:/go/bacalhau-main/job-df0aed15 $PWD/tmp/
```
