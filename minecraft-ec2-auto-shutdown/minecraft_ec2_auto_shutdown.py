from mcipc.query import Client
import boto3
import appdirs
from ec2_metadata import ec2_metadata
import os
from datetime import datetime, timedelta
from pathlib import Path


NAME = 'minecraft-ec2-auto-shutdown'
TIME_THRESHOLD = timedelta(minutes=30)


def check_players_online(host: str, port: int) -> bool:
    with Client(host, port, timeout=1) as client:
        print(client.basic_stats)
        print(f"{client.basic_stats.num_players} player(s) are online")
        return client.basic_stats.num_players > 0
        

def commit_sudoku():    
    session = boto3.Session(        
        region_name=ec2_metadata.region
    )
    ec2 = session.client('ec2')    
    print("Committing sudoku!")
    ec2.stop_instances(InstanceIds=[ec2_metadata.instance_id])    


def save_date(name: str):    
    path = appdirs.user_data_dir(NAME)
    _file = os.path.join(path, name)
    p = Path(_file)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(str(datetime.now().timestamp()))


def load_date(name: str):
    try:
        path = appdirs.user_data_dir(NAME)
        _file = os.path.join(path, name)    
        text = Path(_file).read_text()
        return datetime.fromtimestamp(float(text))
    except:
        return None

def main():
    host = "127.0.0.1"
    port = 25565    

    should_commit_sudoku = False
    last_run = load_date("last_run")
    last_online = load_date("last_online")

    if not last_online: # handle case where player was never seen yet by setting a value to last_online to the current time.
        save_date("last_online")
        last_online = datetime.now()

    now = datetime.now()
    currently_online = check_players_online(host, port)

    if currently_online:
        save_date("last_online")        
    else:        
        should_commit_sudoku = (last_run and last_run + TIME_THRESHOLD >= now) and (last_online + TIME_THRESHOLD < now)
    save_date("last_run")
    
    if should_commit_sudoku:
        commit_sudoku()
    else:
        diff = now - last_online
        mins = diff.total_seconds() // 60
        print(f"Last player was seen {mins} minutes ago. Shutting down in {30 - mins} minutes.")


if __name__ == "__main__":    
    main()
