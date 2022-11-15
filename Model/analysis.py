import datetime
import importlib
import json
import os
import time
from glob import glob

import markdown
import pandas as pd
import yaml
from bs4 import BeautifulSoup as bs


def log_to_md(user, case):
    path = os.path.join('train', user, case)
    title = f"{user}-{case}-LabNote"

    # config
    file_yaml = open(os.path.join(path, f'{case}.yaml'), 'r')
    config = yaml.load(file_yaml, yaml.FullLoader)

    # model summary
    module = importlib.import_module(f"train.{user}.{config['module']}")
    model = getattr(module, config['class'])()
    model.build(input_shape=(None, 300, 300, 3))
    print("case :", case)
    model.summary()
    print()

    # train log
    file_train = pd.read_csv(os.path.join(path, "train_log.csv"))
    file_best = open(os.path.join(path, "best_model.txt"), "r")
    best = int(file_best.readline().split(' ')[0])
    row = file_train[file_train['epoch'] == best].values[0]

    # test log
    file_test = open(os.path.join(path, 'test_log.json'), 'r')
    test_log = json.load(file_test)

    with open("LabNote/template.md", "r", encoding='utf-8') as f:
        md = markdown.markdown(f.read())
        soup = bs(md, "html.parser")
        soup.select_one('#title').string = title
        soup.select_one('#model').attrs['src'] = f'image/{user}-{case}-model.png'
        soup.select_one('#init-lr').string = str(config['init_lr'])
        soup.select_one('#decay-steps').string = str(config['decay_steps'])
        soup.select_one('#batch-size').string = str(config['batch_size'])
        soup.select_one('#epoch').string = str(config['epochs'])
        soup.select_one('#train-loss').string = str(row[2])
        soup.select_one('#test-loss').string = f'{test_log["loss"]:.4f}'
        soup.select_one('#train-score').string = f'{row[3]:.4f} / {row[4]:.4f} / {row[5]:.4f}'
        soup.select_one(
            '#test-score').string = f'{test_log["accuracy"]:.4f} / {test_log["recall"]:.4f} / {test_log["f1"]:.4f}'
        soup.select_one('#val2-cnt').string = str(row[-1])
        soup.select_one('#must-cnt').string = str(test_log['must_cnt'])

        with open(f"LabNote/{title}.md", "w", encoding='utf-8') as sf:
            sf.write(str(soup))
        file_img = open(f"LabNote/image/{user}-{case}-model.png", 'w')
        file_img.close()

    file_yaml.close()
    file_best.close()
    file_test.close()


def get_train_time():
    paths = glob('train/**/*.csv', recursive=True)
    time_sum = 0
    for path in paths:
        file = pd.read_csv(path)
        ts = file['timestamp']
        mi = time.mktime(datetime.datetime.strptime(ts.min(), "%Y-%m-%d %H:%M:%S.%f").timetuple())
        ma = time.mktime(datetime.datetime.strptime(ts.max(), "%Y-%m-%d %H:%M:%S.%f").timetuple())
        total = ((ma - mi) / (len(ts) - 1)) * (len(ts))
        time_sum += total
    print(time_sum / 60)
    print((time_sum / len(paths)) / 60)


if __name__ == "__main__":
    # for c in ['case1', 'case2', 'case4', 'case5', 'case6', 'case7', 'EB0', 'EB1', 'EB2']:
    #     log_to_md('rjh', c)
    get_train_time()
