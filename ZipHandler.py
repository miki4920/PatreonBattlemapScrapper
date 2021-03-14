import zipfile

path = zipfile.Path("maps/Abandoned Mine Entrance [33x21] - $5 Rewards.zip")
print(list(path.iterdir()))