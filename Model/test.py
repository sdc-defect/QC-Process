import json

with open("train/rjh/test/train_must_log.json", "r") as file:
    data: dict = json.load(file)
    print(data['1'])