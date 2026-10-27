import os 
import requests
from . import settings 

def download_raw():
    os.mkdir("data/raw", exist_ok=True)
    url = settings.PARQUET_URL
    out_path = settings.LOCAL_RAW
    print("Downloaded ")

    with requests.get(url, stream=True, timeout=120) as r:     #timeout if running more than 120s - terminate
        r.raise_for_status()

        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return out_path
