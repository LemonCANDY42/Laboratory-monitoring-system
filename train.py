import torch
import os

import flash
from flash.core.data.utils import download_data
from flash.video import VideoClassificationData, VideoClassifier
from flash.core.classification import FiftyOneLabels
from flash.core.integrations.fiftyone import visualize

import fiftyone as fo

from typing import Callable, List
import kornia.augmentation as K

from pytorchvideo.transforms import ApplyTransformToKey, RandomShortSideScale, UniformTemporalSubsample
from torch.utils.data.sampler import RandomSampler
from torchvision.transforms import CenterCrop, Compose, RandomCrop, RandomHorizontalFlip

from func import all_path

# 2. Specify transforms to be used during training.
# Flash helps you to place your transform exactly where you want.
# Learn more at https://lightning-flash.readthedocs.io/en/latest/general/data.html#flash.data.process.Preprocess
post_tensor_transform = [UniformTemporalSubsample(8), RandomShortSideScale(min_size=256, max_size=320)]
per_batch_transform_on_device = [K.Normalize(torch.tensor([0.45, 0.45, 0.45]), torch.tensor([0.225, 0.225, 0.225]))]

train_post_tensor_transform = post_tensor_transform + [RandomCrop(244), RandomHorizontalFlip(p=0.5)]
val_post_tensor_transform = post_tensor_transform + [CenterCrop(244)]
train_per_batch_transform_on_device = per_batch_transform_on_device
def make_transform(
    post_tensor_transform: List[Callable] = post_tensor_transform,
    per_batch_transform_on_device: List[Callable] = per_batch_transform_on_device
):
    return {
        "post_tensor_transform": Compose([
            ApplyTransformToKey(
                key="video",
                transform=Compose(post_tensor_transform),
            ),
        ]),
        "per_batch_transform_on_device": Compose([
            ApplyTransformToKey(
                key="video",
                transform=K.VideoSequential(
                    *per_batch_transform_on_device, data_format="BCTHW", same_on_frame=False
                )
            ),
        ]),
    }

from visualize_video import dataset
train_dataset = dataset
datamodule = VideoClassificationData.from_fiftyone(
    train_dataset=train_dataset,
    # val_dataset=train_dataset,
    clip_sampler="uniform",
    clip_duration=2,
    video_sampler=RandomSampler,
    decode_audio=False,
    train_transform=make_transform(train_post_tensor_transform),
    val_transform=make_transform(val_post_tensor_transform),
    test_transform=make_transform(val_post_tensor_transform),
    predict_transform=make_transform(val_post_tensor_transform),
)



# datamodule = VideoClassificationData.from_folders(
#     train_folder="./videos/train",
#     val_folder="./videos/train",
#     clip_sampler="uniform",
#     clip_duration=2,
#     video_sampler=RandomSampler,
#     decode_audio=False,
#     train_transform=make_transform(train_post_tensor_transform),
#     val_transform=make_transform(val_post_tensor_transform),
#     test_transform=make_transform(val_post_tensor_transform),
#     predict_transform=make_transform(val_post_tensor_transform),
# )

# 0. List the available models
print(VideoClassifier.available_backbones())
# out: ['efficient_x3d_s', 'efficient_x3d_xs', ... ,slowfast_r50', 'x3d_m', 'x3d_s', 'x3d_xs']
print(VideoClassifier.get_backbone_details("x3d_xs"))

# # 2. Build the task
# model = VideoClassifier(backbone="x3d_xs", num_classes=datamodule.num_classes, pretrained=True)

model = VideoClassifier.load_from_checkpoint("video_classification.pt")
# 3. Create the trainer and finetune the model
trainer = flash.Trainer(max_epochs=5, gpus=torch.cuda.device_count())
trainer.finetune(model, datamodule=datamodule, strategy="no_freeze")#no_freeze
# trainer.fit(model, datamodule=datamodule)
filepaths = all_path("/home/kenny/github/Laboratory-monitoring-system/videos/1")
predictions = model.predict(filepaths)
print(predictions)
# 5. Save the model!
trainer.save_checkpoint("video_classification.pt")


# classifier = VideoClassifier.load_from_checkpoint("video_classification.pt")
# classifier.serializer = FiftyOneLabels(return_filepath=True)
# trainer = flash.Trainer(gpus=1)

# # filepaths = ["/home/kenny/github/Laboratory-monitoring-system/videos/train/stop/停止状态.mp4","/home/kenny/github/Laboratory-monitoring-system/videos/train/other/干扰.mp4","/home/kenny/github/Laboratory-monitoring-system/videos/train/work/Working.mp4"]
# filepaths = all_path("/home/kenny/github/Laboratory-monitoring-system/videos/1")
# predictions = classifier.predict(filepaths)
# print(predictions)

session = visualize(predictions, filepaths=filepaths) # Launch FiftyOne
session.wait()