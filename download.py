import requests
import tarfile
import os
import argparse


def download_extract(url, output_path):
    file_name = url.split('/')[-1]

    # Download
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)

    # Extract
    tar = tarfile.open(file_name)
    tar.extractall(path=output_path)
    tar.close()

    # delete archive
    os.remove(file_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download Deep 6 dof dataset')
    parser.add_argument('-o', '--output', help="Output path", action="store", default="data")
    parser.add_argument('--skip_models', help="Skip 3D model downloads", action="store_true")
    parser.add_argument('--skip_raw', help="Skip Raw training data", action="store_true")
    parser.add_argument('--skip_sequences', help="Skip Sequence data", action="store_true")
    parser.add_argument('--skip_occlusion', help="Skip Occlusion data", action="store_true")

    arguments = parser.parse_args()
    skip_models = arguments.skip_models
    skip_raw = arguments.skip_raw
    skip_sequences = arguments.skip_sequences
    skip_occlusion = arguments.skip_occlusion
    output_path = arguments.output

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if not skip_models:
        print("Download 3D models...")
        url = "http://rachmaninoff.gel.ulaval.ca/static/deeptracking/3dmodels.tar.gz"
        download_extract(url, output_path)

    if not skip_raw:
        print("Download Raw Training")
        url = "http://rachmaninoff.gel.ulaval.ca/static/deeptracking/raw_training.tar.gz"
        download_extract(url, output_path)

    if not skip_sequences:
        print("Download Sequences")
        url = "http://rachmaninoff.gel.ulaval.ca/static/deeptracking/sequences.tar.gz"
        download_extract(url, output_path)

    if not skip_occlusion:
        print("Download Occlusion sequences")
        url = "http://rachmaninoff.gel.ulaval.ca/static/deeptracking/occlusion.tar.gz"
        download_extract(url, output_path)