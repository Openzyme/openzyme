import argparse
import os
import shutil
import sys
import tempfile
import uuid

import boto3


S3_BUCKET = 'openzyme'


def fetch_and_run_script(input_s3_filename):
    s3 = boto3.client('s3')
    with tempfile.TemporaryDirectory() as tmpdirname:
        input_script_filepath = f'{tmpdirname}/{input_s3_filename}'
        input_s3_path = f'input_scripts/{input_s3_filename}'
        s3.download_file(S3_BUCKET, input_s3_path, input_script_filepath)
        os.chdir(tmpdirname)
        cmd = f'python {input_script_filepath}'
        os.system(cmd)
        output_filename = str(uuid.uuid4())
        shutil.make_archive(output_filename, 'zip', tmpdirname)
        output_s3_path = f'results/{output_filename}.zip'
        s3.upload_file(f'{output_filename}.zip', S3_BUCKET, output_s3_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_s3_file", type=str)
    args = parser.parse_args()
    fetch_and_run_script(args.input_s3_file)
