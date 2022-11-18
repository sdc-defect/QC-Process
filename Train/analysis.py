import datetime
import importlib
import json
import math
import os
import time
from glob import glob
import traceback

import markdown
import pandas as pd
import yaml
from bs4 import BeautifulSoup as bs


def log_to_md(user, case):
    path = os.path.join('train', user, case)
    title = f"{user}-{case}-LabNote"

    # config
    file_yaml = open(os.path.join(path, f'{case}.yaml'), 'r', encoding='utf-8')
    config = yaml.load(file_yaml, yaml.FullLoader)
    module_name = user + '.' + '.'.join(config['module'].split('.')[-2:])
    cls = config['class']

    # train log
    csvs = glob(os.path.join(path, '*.csv'))
    if len(csvs) == 0:
        print(path, "is empty folder !!!")
        return
    file_train = pd.read_csv(csvs[0])
    file_best = open(os.path.join(path, "best_model.txt"), "r")
    best = file_best.readline().split(' ')[-2]
    best = int(best)
    row = file_train[file_train['epoch'] == best].values[0]

    # test log
    file_test = open(os.path.join(path, 'test_log.json'), 'r')
    test_log = json.load(file_test)

    # model summary
    isModel = True
    try:
        module = importlib.import_module(f"train.{user}.{config['module']}")
        model = getattr(module, config['class'])()
        model.build(input_shape=(None, 300, 300, 3))
        with open(f'LabNote/model/{user}-{case}-model.txt', 'w') as model_txt:
            model.summary(print_fn=lambda x: model_txt.write(x + "\n"))
    except Exception as er:
        print(er)
        isModel = False

    with open("LabNote/template.md", "r", encoding='utf-8') as f:
        md = markdown.markdown(f.read())
        soup = bs(md, "html.parser")
        soup.select_one('#title').string = title

        ts = file_train['timestamp']
        mi = time.mktime(datetime.datetime.strptime(ts.min(), "%Y-%m-%d %H:%M:%S.%f").timetuple())
        ma = time.mktime(datetime.datetime.strptime(ts.max(), "%Y-%m-%d %H:%M:%S.%f").timetuple())
        mean_time = (ma - mi) / (len(ts) - 1)
        total = math.ceil((mean_time * (len(ts))))
        soup.select_one('#date').string = datetime.datetime.fromtimestamp(mi - mean_time).strftime("%Y-%m-%d %H:%M:%S")
        soup.select_one('#time-cost').string = f'{str(int(total / 60)).zfill(2)}m {str(int(total % 60)).zfill(2)}s'

        soup.select_one('#module').string = str(module_name)
        soup.select_one('#class').string = str(cls)
        if isModel:
            with open(f"LabNote/model/{user}-{case}-model.txt", "r") as model_txt:
                lines = model_txt.readlines()
                for l in lines:
                    split = l.split(': ')
                    if split[0] == 'Total params':
                        soup.select_one('#total-params').string = split[1].split('\n')[0]
                    elif split[0] == 'Trainable params':
                        soup.select_one('#trainable-params').string = split[1].split('\n')[0]
                    elif split[0] == 'Non-trainable params':
                        soup.select_one('#non-trainable-params').string = split[1].split('\n')[0]

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


def get_cases():
    paths = glob('train/**/*.yaml', recursive=True)

    result = {}
    for path in paths:
        with open(path, "r", encoding='utf-8') as f:
            config: dict = yaml.load(f, yaml.FullLoader)
            if 'root_dir' in config.keys():
                del config['root_dir']
            if 'save_dir' in config.keys():
                del config['save_dir']
            if 'user' in config.keys():
                config['module'] = config['user'] + '.' + config['module']
                del config['user']
            if 'save' in config.keys():
                del config['save']
            config['module'] = config['module'].replace("train.", '').replace('.model', '')
            config['class'] = config['module'] + '.' + config['class']
            config['class'] = config['class']
            del config['module']

            for key in config.keys():
                if key not in result:
                    result[key] = {}
                if config[key] not in result[key]:
                    result[key][config[key]] = 1
                else:
                    result[key][config[key]] += 1

    with open('case_analysis.json', 'w') as f:
        json.dump(result, f)


if __name__ == "__main__":
    # Generate LabNote
    for u in ['hsd', 'jjh', 'jsh', 'kmy', 'ksh', 'rjh']:
        for c in os.listdir(f'train/{u}'):
            print(u, c)
            if not c.startswith('case'):
                continue
            try:
                log_to_md(u, c)
            except Exception as e:
                print('-' * 50)
                print(os.path.join(u, c), traceback.format_exc())
                print('-' * 50)

    # Get All Train Time
    get_train_time()

    # Get analysis of yaml file
    get_cases()
