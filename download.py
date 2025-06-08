import os
import re
import pandas as pd
from tqdm import tqdm
import yt_dlp

FOLDER = os.path.join("data", "video")

def download_video(name, video_id, start_time, duration_time):
    """
    start_time and duration_time have to be in the format hh:mm:ss
    """
    file_path = os.path.join(FOLDER, name)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    # Set up options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'noplaylist': True,  # Download only single video
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
            file_name = re.sub(r"[.;:,?!]", "", info_dict['title']) + ".mp4"
    except Exception as e:
        print(f"Error fetching video with ID {video_id}: {e}")
        return

    output_file = os.path.join(file_path, name + "-" + video_id + ".mp4")
    if os.path.exists(output_file):
        return

    # Check if start_time and duration_time are valid
    if start_time == "" or duration_time == "":
        os.rename(os.path.join(FOLDER, file_name), output_file)  # Rename the downloaded file
    else:
        original_video = os.path.join(FOLDER, file_name)
        try:
            os.system(
                f'ffmpeg -hide_banner -loglevel error -ss {start_time} -i "{original_video}" -to {duration_time} -c copy "{output_file}"'
            )
        except Exception as e:
            print(f"An error occurred when processing {file_name}: {e}")
            # Delete the videos used to create the clips for the dataset
            for file in os.listdir(FOLDER):
                if file.endswith(".mp4"):
                    os.remove(os.path.join(FOLDER, file))

print("\nDownloading videos of signs from YouTube\n")

# Create the dataset based on yt_links.csv
df_links = pd.read_csv("/Users/blessykancharla/Desktop/Voice_2_sign/data/Yt_links.csv")

# Print the columns to debug
print("Columns in the CSV file:", df_links.columns)

# Strip whitespace from column names
df_links.columns = df_links.columns.str.strip()

# Validate and download videos
for idx, row in tqdm(df_links.iterrows(), total=df_links.shape[0]):
    video_id = row['id'].strip()  # Strip whitespace from video ID
    if pd.isnull(video_id) or len(video_id) != 11:
        print(f"Invalid video ID: {video_id}")
        continue
    download_video(row['name'], video_id, row['start_time'], row['duration_time'])

# Delete the videos used to create the clips for the dataset
for file in os.listdir(FOLDER):
    if file.endswith(".mp4"):
        os.remove(os.path.join(FOLDER, file))