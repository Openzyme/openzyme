import argparse
import os
import shutil
import sys
import tempfile
import uuid

import boto3


S3_BUCKET = 'openmm'


def fetch_and_run_script(script_s3_filename, protein_s3_filename):
    s3 = boto3.client('s3')
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f'created temp directory {tmpdirname}')
        os.chdir(tmpdirname)
        os.mkdir('results')

        protein_filepath = f'{tmpdirname}/results/{protein_s3_filename}'
        print(f'downloading {protein_s3_filename} to {protein_filepath}')
        s3.download_file(S3_BUCKET, protein_s3_filename, protein_filepath)

        script_filepath = f'{tmpdirname}/results/{script_s3_filename}'
        print(f'downloading {script_s3_filename} to {script_filepath}')
        s3.download_file(S3_BUCKET, script_s3_filename, script_filepath)

        os.chdir(f'{tmpdirname}/results')
        print('running inputted script')
        cmd = f'python {script_filepath}'
        os.system(cmd)

        os.chdir(tmpdirname)
        output_filename = str(uuid.uuid4())
        print(f'creating {output_filename}.zip')
        shutil.make_archive(output_filename, 'zip', f'{tmpdirname}/results')
        output_s3_path = f'results/{output_filename}.zip'
        print(f'uploading {output_filename} to {output_s3_path}')
        s3.upload_file(f'{output_filename}.zip', S3_BUCKET, output_s3_path)
    print('done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--script_s3_filename", type=str)
    parser.add_argument("-p", "--protein_s3_filename", type=str)
    args = parser.parse_args()
    print(f'starting fetch_and_run_script with args {args.script_s3_filename} and {args.protein_s3_filename}')
    fetch_and_run_script(args.script_s3_filename, args.protein_s3_filename)
