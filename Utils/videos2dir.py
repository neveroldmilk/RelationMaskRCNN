import argparse
import os
import pandas as pd

from Utils import create_folder, video_to_frames, download_incidents

__author__ = 'roeiherz'

VIDEO_PATH = "/home/roeiherzig/data/Incidents/Videos"
INDEX_PATH = "/home/roeiherzig/data/Incidents/index.csv"
IMAGE_PATH = "/home/roeiherzig/data/Incidents/Images"


def get_video_links(index_path):
    """
    This function returns the data
    :param output_dir:
    :return:
    """

    df_index = pd.read_csv(index_path)
    video_links = list(df_index['video link'].unique())

    return video_links


if __name__ == "__main__":
    """
    This Script downloads videos and using video2dir code to parse multiple videos to images 
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--local', help='input directory of videos', action='store', default=False)
    parser.add_argument('--download', help='input directory of videos', action='store', default=False)
    parser.add_argument('--video', help='input directory of videos', action='store', default=VIDEO_PATH)
    parser.add_argument('--index', help='index file path', action='store', default=INDEX_PATH)
    parser.add_argument('--image', help='output directory of videos', action='store', default=IMAGE_PATH)
    args = parser.parse_args()

    # Use Local params
    if args.local:
        args.video = "/Users/roeiherzig/Datasets/Incidents/Videos/"
        args.index = "/Users/roeiherzig/Datasets/Incidents/Videos/index.csv"
        args.image = "/Users/roeiherzig/Datasets/Incidents/Images/"

    # Download Incidents
    if args.download:
        download_incidents(input_file=args.index, output_dir=args.input)

    # Check directory exists
    if not os.path.exists(args.video):
        print('Can not find videos directory: {}'.format(args.i))
        exit(-1)

    for split in ['Train', 'Test']:

        # Video Path
        video_path = os.path.join(args.video, split)
        # Image path
        img_path = os.path.join(args.image, split)

        # Get files
        files = os.listdir(video_path)
        # files = ['412563fe-ce68-4c17-92ce-b8770d6fb140.mov']
        print('Number of files: {} from input directory'.format(len(files)))

        for base_name in files:
            try:

                # Process only if its a video
                if '.mov' in base_name or '.mp4' in base_name:

                    # video file
                    in_dir = os.path.join(video_path, base_name)
                    # Without extension
                    out_dir = os.path.join(img_path, os.path.splitext(base_name)[0])

                    if os.path.exists(out_dir):
                        print("Dir {} already exists".format(base_name))
                        continue

                    create_folder(out_dir)
                    print('{} --> {}'.format(video_path, out_dir))
                    video_to_frames(in_dir, out_dir, jump=True)

            except Exception as e:
                print("Error in incident {} with {}".format(base_name, str(e)))