import fiftyone as fo

if __name__ == '__main__':
    dataset_dir = "./videos"
    # Create the dataset
    dataset = fo.Dataset.from_dir(
        dataset_dir, fo.types.VideoClassificationDirectoryTree, name='dataset'
    )
    print(dataset.head())
    # Launch the App and view the dataset
    session = fo.launch_app(dataset)
    # (Perform any additional operations here)

    # Blocks execution until the App is closed
    session.wait()