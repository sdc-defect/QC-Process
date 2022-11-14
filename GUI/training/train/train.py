import argparse

import math
import os.path
from keras.optimizers.schedules.learning_rate_schedule import CosineDecayRestarts
from keras.optimizers.optimizer_v2.adam import Adam
from keras.losses import CategoricalCrossentropy

from utils.util import model_to_onnx, train, test, load_onnx
from utils import make_folder, load_config_json, batch
from utils.dataset import get_dataset_from_config
from utils.dto import TrainResult
from utils.model import MyModel
from utils.record import MyRecorder

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--json',
                        required=True)
    args = parser.parse_args()
    config = load_config_json(args.json)

    # config.json = TrainConfig(save_path=".", train_path=["temp/def", "temp/ok"],
    #                      test_path=None, test_per=0.5, val_path=None, val_per=0.1,
    #                      flip=True, spin=True, shift=True, mixup=True,
    #                      epoch=50, batch_size=16, lr=0.001, decay=1000)

    model = MyModel()
    loss_func = CategoricalCrossentropy()
    schedular = CosineDecayRestarts(config.lr, config.decay)
    optimizer = Adam(schedular)

    train_dataset, val_dataset, test_dataset = get_dataset_from_config(config)
    recorder = MyRecorder()

    # Train
    train_batch_size = math.ceil(len(train_dataset) / config.batch_size)
    val_batch_size = math.ceil(len(val_dataset) / config.batch_size)
    for e in range(1, config.epoch + 1):
        recorder.reset()

        # Train
        for b, (img, label) in enumerate(batch(train_dataset, config.batch_size)):
            loss, prob = train(img, label, model, loss_func, optimizer)
            recorder.train.record(loss, prob, label)
            result = TrainResult(confusionmatrix=recorder.train.get_confusion_matrix(), loss=float(loss.numpy()),
                                 header="train", epoch=f"{e}/{config.epoch}", batch=f"{b + 1}/{train_batch_size}")
            print(result)

        # Validate
        for b, (img, label) in enumerate(batch(val_dataset, config.batch_size)):
            loss, prob = test(img, label, model, loss_func)
            recorder.val.record(loss, prob, label)
            result = TrainResult(confusionmatrix=recorder.val.get_confusion_matrix(), loss=float(loss.numpy()),
                                 header="val", epoch=f"{e}/{config.epoch}", batch=f"{b + 1}/{val_batch_size}")
            print(result)

        # Save
        if recorder.check_best_score():
            make_folder(config.save_path)
            print('saving...', os.path.join(config.save_path, "model.onnx"))
            model_to_onnx(model, os.path.join(config.save_path, "model.onnx"))

    # Test
    runtime = load_onnx(os.path.join(config.save_path, "model.onnx"))
    test_batch_size = math.ceil(len(test_dataset) / config.batch_size)
    for b, (img, label) in enumerate(batch(test_dataset, config.batch_size)):
        prob = runtime.runtime.run(None, {'input_1': img})[0]
        loss = loss_func(label, prob)
        recorder.test.record(loss, prob, label)
        result = TrainResult(confusionmatrix=recorder.val.get_confusion_matrix(), loss=float(loss.numpy()),
                             header="test", epoch=None, batch=f"{b + 1}/{test_batch_size}")
        print(result)
