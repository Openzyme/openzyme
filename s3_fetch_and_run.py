import argparse
import os
import shutil
import sys
import tempfile
import uuid

import boto3


S3_BUCKET = 'openzyme'


def fetch_and_run_script(script_s3_filename, protein_s3_filename):
    s3 = boto3.client('s3')
    with tempfile.TemporaryDirectory() as tmpdirname:
        protein_filepath = f'{tmpdirname}/{protein_s3_filename}'
        s3.download_file(S3_BUCKET, protein_s3_filename, protein_filepath)

        script_filepath = f'{tmpdirname}/{script_s3_filename}'
        s3.download_file(S3_BUCKET, script_s3_filename, script_filepath)

        os.chdir(tmpdirname)
        cmd = f'python {script_filepath}'
        os.system(cmd)

        output_filename = str(uuid.uuid4())
        shutil.make_archive(output_filename, 'zip', tmpdirname)
        output_s3_path = f'results/{output_filename}.zip'
        s3.upload_file(f'{output_filename}.zip', S3_BUCKET, output_s3_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--script_s3_filename", type=str)
    parser.add_argument("-p", "--protein_s3_filename", type=str)
    args = parser.parse_args()
    fetch_and_run_script(args.script_s3_filename, args.protein_s3_filename)
