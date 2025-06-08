import os
import re
import pandas as pd
from tqdm import tqdm
import yt_dlp

FOLDER = "data/video"  # Save directly to the 'video' folder

def download_video(name, video_id, start_time, duration_time):
    """
    Downloads a specific segment of a YouTube video directly to the video folder
    with a lowercase filename based on the 'name' from the CSV,
    only if it doesn't already exist.

    Args:
        name (str): The desired name for the downloaded video segment (from CSV).
        video_id (str): The ID of the YouTube video.
        start_time (str): The start time of the segment (hh:mm:ss).
        duration_time (str): The duration of the segment (hh:mm:ss).
    """
    output_filename = f"{name.lower()}.mp4"
    output_path = os.path.join(FOLDER, output_filename)

    if os.path.exists(output_path):
        print(f"Video for '{name}' (ID: {video_id}) already exists at: {output_path}")
        return

    print(f"Downloading video for '{name}' (ID: {video_id}) from YouTube...")

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
            temp_file_name = re.sub(r"[.;:,?!]", "", info_dict['title']) + ".mp4"
            temp_file_path = os.path.join(FOLDER, temp_file_name)

            # Check if the full video was downloaded (might happen if start/end are invalid)
            if start_time == "" or duration_time == "":
                os.rename(temp_file_path, output_path)
                print(f"Successfully downloaded full video for '{name}' (ID: {video_id}) to: {output_path}")
            else:
                try:
                    os.system(
                        f'ffmpeg -hide_banner -loglevel error -ss {start_time} -i "{temp_file_path}" -to {duration_time} -c copy "{output_path}"'
                    )
                    print(f"Successfully downloaded video segment for '{name}' (ID: {video_id}) to: {output_path}")
                except Exception as e:
                    print(f"Error processing video segment for '{name}' (ID: {video_id}): {e}")
                finally:
                    # Clean up the temporary full video file
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

    except Exception as e:
        print(f"Error fetching video with ID {video_id}: {e}")
        return

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

# Delete any remaining temporary full video files
for file in os.listdir(FOLDER):
    if file.endswith(".mp4") and "temp_" in file:
        os.remove(os.path.join(FOLDER, file))

print("\nVideo downloading process completed.\n")