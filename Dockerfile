FROM sunhwan/openmm

COPY s3_fetch_and_run.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
