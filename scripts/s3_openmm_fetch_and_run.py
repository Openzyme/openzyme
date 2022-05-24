import argparse
import os
import sys

import boto3


S3_BUCKET = 'openzyme'


def fetch_and_run_script(input_s3_filename, output_s3_path):
    s3 = boto3.client('s3')

    openmm_script_filename = 'openmm_run_simulation.py'
    input_s3_path = f'openmm_scripts/{input_s3_filename}'
    s3.download_file(S3_BUCKET, input_s3_path, openmm_script_filename)

    cmd = f'python {openmm_script_filename}'
    os.system(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_s3_file", type=str)
    parser.add_argument("-o", "--output_s3_file", type=str)

    args = parser.parse_args()
    fetch_and_run_script(args.input_s3_file, args.output_s3_file)
