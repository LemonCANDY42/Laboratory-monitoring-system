import torch
from torchvision.transforms import Compose, Lambda
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
from pytorchvideo.transforms import (
    ApplyTransformToKey,
    ShortSideScale,
    UniformTemporalSubsample
) 

import fiftyone as fo

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Load pre-trained model 
model = torch.hub.load('facebookresearch/pytorchvideo:main', 'x3d_xs', pretrained=True)
model.to(device)

# Create an id to label name mapping
kinetics_id_to_classname = {v:k for v,k in enumerate(dataset.default_classes)} 

side_size = 256
mean = [0.45, 0.45, 0.45]
std = [0.225, 0.225, 0.225]
crop_size = 256
num_frames = 8
# Note that this transform is specific to the slow_R50 model.
# If you want to try another of the torch hub models you will need to modify this transform
transform =  ApplyTransformToKey(
    key="video",
    transform=Compose(
        [
            UniformTemporalSubsample(num_frames),
            Lambda(lambda x: x/255.0),
            NormalizeVideo(mean, std),
            ShortSideScale(
                size=side_size
            ),
            CenterCropVideo(crop_size=(crop_size, crop_size))
        ]
    ),
) 

#  load and run our model on them with PyTorchVideo
from pytorchvideo.data.encoded_video import EncodedVideo
import fiftyone.core.utils as fouo
def parse_predictions(preds, kinetics_id_to_classname, k=3):
    preds_topk = preds.topk(k=k)
    pred_classes = preds_topk.indices[0]
    pred_scores = preds_topk.values[0]
    preds_top1 = preds.topk(k=1)
    pred_class = preds_top1.indices[0]
    pred_score = preds_top1.values[0]
    # Map the predicted classes to the label names
    pred_class_names = [kinetics_id_to_classname[int(i)] for i in pred_classes]
    pred_class_name = kinetics_id_to_classname[int(pred_class)]
    prediction_top_1 = fo.Classification(
        label=pred_class_name,
        confidence=pred_score,
    )
    predictions_top_k = []
    for l, c in zip(pred_class_names, pred_scores):
        cls = fo.Classification(label=l, confidence=c)
        predictions_top_k.append(cls)
    predictions_top_k = fo.Classifications(classifications=predictions_top_k)
    return prediction_top_1, predictions_top_k 

# Train the model
with torch.no_grad():
    with fouo.ProgressBar() as pb:
        for sample in pb(dataset):
            video_path = sample.filepath
            # Initialize an EncodedVideo helper class
            video = EncodedVideo.from_path(video_path)
            # Select the duration of the clip to load by specifying the start and end duration
            # The start_sec should correspond to where the action occurs in the video
            start_sec = 0
            clip_duration = int(video.duration)
            end_sec = start_sec + clip_duration    
            # Load the desired clip
            video_data = video.get_clip(start_sec=start_sec, end_sec=end_sec)
            # Apply a transform to normalize the video input
            video_data = transform(video_data)
            # Move the inputs to the desired device
            inputs = video_data["video"]
            inputs = inputs.to(device)
            # Pass the input clip through the model
            preds_pre_act = model(inputs[None, ...])
            # Get the predicted classes
            post_act = torch.nn.Softmax(dim=1)
            preds = post_act(preds_pre_act)
            # Generate FiftyOne labels from predictions
            prediction_top_1, predictions_top_5 = parse_predictions(preds, kinetics_id_to_classname, k=3)
            # Add FiftyOne label fields to Sample
            sample["predictions"] = prediction_top_1
            sample["predictions_top_5"] = predictions_top_5
            sample.save() 

session = fo.launch_app(dataset)
session.freeze()