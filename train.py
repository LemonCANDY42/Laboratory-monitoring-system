import torch

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
# from visualize_video import dataset
# train_dataset = dataset
# datamodule = VideoClassificationData.from_fiftyone(
# train_dataset=train_dataset,
# val_dataset=train_dataset,
# )

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

datamodule = VideoClassificationData.from_folders(
    train_folder="./videos",
    val_folder="./videos",
    clip_sampler="uniform",
    clip_duration=2,
    decode_audio=False,
    train_transform=make_transform(train_post_tensor_transform),
    val_transform=make_transform(val_post_tensor_transform),
    test_transform=make_transform(val_post_tensor_transform),
    predict_transform=make_transform(val_post_tensor_transform),
)


# 2. Build the task
model = VideoClassifier(backbone="x3d_xs", num_classes=datamodule.num_classes, pretrained=True)

# 3. Create the trainer and finetune the model
trainer = flash.Trainer(max_epochs=3, gpus=torch.cuda.device_count())
trainer.finetune(model, datamodule=datamodule, strategy="freeze")
# trainer.fit(model, datamodule=datamodule)


# # 4. Make a prediction
# predictions = model.predict("data/kinetics/predict")
# print(predictions)

model.serializer = FiftyOneLabels(return_filepath=True)
# predictions = trainer.predict(model, datamodule=datamodule)
# session = visualize(predictions) # Launch FiftyOne

# 5. Save the model!
trainer.save_checkpoint("video_classification.pt")

predictions = model.predict("./videos/A")
print(predictions)

# # Option 2: Generate predictions from model using filepaths
# filepaths = ["list", "of", "filepaths"]
# predictions = model.predict(filepaths)
# model.serializer = FiftyOneLabels()
# session = visualize(predictions, filepaths=filepaths) # Launch FiftyOne



# session.wait()