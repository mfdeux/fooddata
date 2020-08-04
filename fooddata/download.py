import tempfile
import os
import tempfile
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm


def download_data(url: str, save_path: str = None):
    local_filename = url.split('/')[-1]
    local_pathname = local_filename.split('.')[0]

    with requests.get(url, stream=True) as r:
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with tempfile.NamedTemporaryFile() as zip_fh:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                zip_fh.write(data)
            progress_bar.close()

            z = zipfile.ZipFile(zip_fh)

            if not save_path:
                temp_dirpath = tempfile.mkdtemp()
                full_dirpath = os.path.join(temp_dirpath, local_pathname)
            else:
                full_dirpath = os.path.join(save_path, local_pathname)

            Path(full_dirpath).mkdir(parents=True, exist_ok=True)
            z.extractall(full_dirpath)

    return full_dirpath
