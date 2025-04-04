from geofox_client import GtiClient
import json
import os
from pathlib import Path

file_dir = Path(__file__).resolve(strict=True).parent
data_dir = file_dir / "data_geofox"

def get_stations(client, loadFromDisk=False , doSave=True):
    if loadFromDisk:
        # load json from folder "data_geofox"
        with open(os.path.join(data_dir, "stations.json"), "r") as f:
            res = json.load(f)
        return res

    endpoint = 'listStations' 
    request = {
    "language": "de",
    "version": 59
    }

    res = client.send(endpoint, request)

    if doSave:
        # saving json to folder "data_geofox"
        with open(os.path.join(data_dir, "stations.json"), "w") as f:
            json.dump(res, f, indent=4)

    return res