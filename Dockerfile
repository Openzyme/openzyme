# FROM sunhwan/openmm
FROM python

COPY s3_openmm_fetch_and_run.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
