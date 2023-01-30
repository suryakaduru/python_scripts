import streamlit as st
import os
import time
import csv


def extract_frames(video_path, export_path):
    start_time = time.time()
    total_patients = len(os.listdir(video_path))
    st.write("Total number of sets in the current batch:", total_patients)
    
    st.sidebar.title("Progress")
    # Create a CSV file to store the processed patients and videos
    with open("processed_vids.csv", "w") as csv_file:
        fieldnames = ["patient_set", "videos"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for idx, patient in enumerate(os.listdir(video_path)):
            # Update the progress in the sidebar
            st.sidebar.write(f"Processing patient_Set: {patient}")
            videos = []
            for jdx, crop in enumerate(os.listdir(f"{video_path}/{patient}")):
                st.sidebar.write(f"Processing video: {crop}")
                crop_video = f"{video_path}/{patient}/{crop}"
                extracted_png = f"{export_path}/{patient}_{jdx}/frame%04d.png"
                os.mkdir(f"{export_path}/{patient}_{jdx}")
                os.system(f"ffmpeg -i {crop_video} {extracted_png}")
                videos.append(crop)
            writer.writerow({"patient_set": patient, "videos": ",".join(videos)})
            # Display a tick mark after each patient is processed
            st.sidebar.markdown("&#10004;")
    end_time = time.time()
    elapsed_time = end_time - start_time
    # Calculate the elapsed time in minutes and seconds
    elapsed_minutes = int(elapsed_time / 60)
    elapsed_seconds = int(elapsed_time % 60)
    # Display the elapsed time in minutes and seconds
    st.write(f"Elapsed time: {elapsed_minutes} minutes {elapsed_seconds} seconds")
    
def analyze_videos(export_path):
    total_patients = len(os.listdir(export_path))
    st.write("Total number of sets in the current batch:", total_patients)
    for idx, crop in enumerate(os.listdir(export_path)):
        num_frames = len(os.listdir(f"{export_path}/{crop}"))
        st.write(f"Number of frames extracted in {crop}: {num_frames}")
    print("Videos analyzed successfully!")




def main():
    #st.image("logo.png", width=200)
    st.title("Frame Extractor")
    st.markdown(
        """
        This tool allows you to extract frames from a batch of videos and analyze them.
        To get started, enter the path to the directory containing the videos and the path to the directory where you want to save the extracted frames.
        Then, click the "Extract Frames" button to begin the process. 
        """
    )
    video_path = st.text_input("Enter the path to the directory containing the videos:")
    export_path = st.text_input("Enter the path to the directory where you want to save the extracted frames:")
    if st.button("Extract Frames"):
        with st.spinner("Extracting frames..."):
            st.write("Please wait for a moment...")
            extract_frames(video_path, export_path)
        st.success("Frames extracted successfully!")
    st.sidebar.title("Navigation")
    if st.sidebar.button("Analysis"):
        with st.spinner("Analyzing videos..."):
            analyze_videos(export_path)
        st.success("Videos analyzed successfully!")


if __name__ == "__main__":
    main()
