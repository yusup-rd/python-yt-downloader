import os
import shutil
from google.colab import drive
from pytube import YouTube
from youtubesearchpython import VideosSearch
from colorama import Fore, Style

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to your Google Drive folder where you want to save the video
google_drive_path = "/content/drive/My Drive"

# Function to search for videos and allow the user to select one
def search_and_select_video(query):
    try:
        # Perform a YouTube video search using the query
        search = VideosSearch(query)
        results = search.result()
    except Exception as e:
        # Handle any errors that occur during the search
        print(Fore.RED + "An error occurred while searching:", str(e))
        print(Style.RESET_ALL)
        return None

    if not results:
        # If no results were found, inform the user
        print(Fore.YELLOW + "No videos found for the given query.")
        print(Style.RESET_ALL)
        return None

    # Display search results to the user
    print("\n" + Fore.CYAN + "Search results:")
    print(Style.RESET_ALL)
    for i, result in enumerate(results['result'], start=1):
        print(f"{i}. {result['title']}")

    try:
        # Ask the user to select a video by number
        choice = int(input("Enter the number of the video you want to download: "))
        if 1 <= choice <= len(results['result']):
            return results['result'][choice - 1]['link']
        else:
            print(Fore.RED + "Invalid choice. Please enter a valid number.")
            print(Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid number.")
        print(Style.RESET_ALL)

# Function to download a video with progress indication
def download_video_with_progress(url, download_path):
    try:
        # Create a YouTube object for the selected video
        yt = YouTube(url, on_progress_callback=on_progress)
        print("\n" + Fore.MAGENTA + "Video Details:")
        print(Style.RESET_ALL)
        print("Title:", yt.title)
        print("Views:", yt.views)

        # Get the highest resolution stream for the video
        yd = yt.streams.get_highest_resolution()

        # Define the output file path on Colab
        output_path = os.path.join(download_path, yt.title + ".mp4")

        print("\n" + Fore.YELLOW + "Downloading...")
        yd.download(output_path)
        print("\n" + Fore.GREEN + "Video downloaded successfully.")
        print(Style.RESET_ALL)

        # Move the downloaded video to Google Drive
        shutil.move(output_path, os.path.join(google_drive_path, yt.title + ".mp4"))
        print("\n" + Fore.BLUE + "Video moved to Google Drive.")
        print(Style.RESET_ALL)
    except Exception as e:
        print("\n" + Fore.RED + "An error occurred:", str(e))
        print(Style.RESET_ALL)

# Callback function to display download progress
def on_progress(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    print(Fore.CYAN + f"Downloading... {percentage:.1f}% completed", end="\r")
    print(Style.RESET_ALL, end="")

# Main function for the program
def main():
    print(Fore.GREEN + "Welcome to the YouTube Video Downloader!")
    print(Style.RESET_ALL)
    while True:
        search_query = input("Enter the name of the video you want to download (or 'exit' to quit): ")
        if search_query.lower() == 'exit':
            break

        selected_video_link = search_and_select_video(search_query)

        if selected_video_link:
            download_video_with_progress(selected_video_link, "/content")

if __name__ == "__main__":
    main()
