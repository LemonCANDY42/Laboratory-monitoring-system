import fiftyone as fo
dataset_dir = "./videos/train"
val_dataset_dir = "./videos/val"
# Create the dataset
train_dataset = fo.Dataset.from_dir(
    dataset_dir, fo.types.VideoClassificationDirectoryTree, name='train_dataset',
)
val_dataset = fo.Dataset.from_dir(
    val_dataset_dir, fo.types.VideoClassificationDirectoryTree, name='val_dataset',
)

if __name__ == '__main__':

    print(dataset.head())
    # Launch the App and view the dataset
    session = fo.launch_app(dataset)
    # (Perform any additional operations here)

    # Blocks execution until the App is closed
    session.wait()