import os
from pytube import YouTube
import pytube
from stqdm import stqdm
import pandas as pd
from youtubesearchpython import Video, ResultMode, Channel
import streamlit as st
import scrapetube
from categoryPredictor import predictCategoryFor
import pandas as pd
import traceback

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def get_channel_id(url):
    """Extract channel ID from a YouTube URL or return the URL if it's already a channel ID."""
    try:
        # First try to get video info and extract channel ID
        try:
            video_info = Video.getInfo(url, mode=ResultMode.json)
            return video_info["channel"]["id"]
        except:
            # If it's not a video URL, try to extract channel ID directly
            if "/channel/" in url:
                return url.split("/channel/")[1].split("/")[0]
            elif "/c/" in url or "/user/" in url or "@" in url:
                # For custom URLs, we need to fetch the channel info
                channel_info = Channel.get(url)
                return channel_info["id"]
            else:
                # Assume it's already a channel ID
                return url
    except Exception as e:
        st.error(f"Error extracting channel ID: {str(e)}")
        return None

def generate_channel_video_data(of_channel, with_number_of_videos):
    try:
        # Get channel ID
        c_id = get_channel_id(of_channel)
        if not c_id:
            st.error("Could not extract channel ID. Please enter a valid YouTube channel or video URL.")
            return
        
        st.info(f"Fetching videos for channel ID: {c_id}")
        
        # Get videos from channel
        try:
            videos = scrapetube.get_channel(c_id)
            video_urls = []
            i = 0
            
            # Create a progress bar for fetching videos
            progress_text = "Fetching videos..."
            video_progress = st.progress(0, text=progress_text)
            
            for video in videos:
                video_id = str(video.get('videoId', ''))
                if video_id:
                    video_urls.append(f"https://www.youtube.com/watch?v={video_id}")
                    i += 1
                    video_progress.progress(min(i / with_number_of_videos, 1.0), 
                                           text=f"{progress_text} {i}/{with_number_of_videos}")
                    if i >= with_number_of_videos:
                        break
            
            video_progress.empty()
            
            if not video_urls:
                st.warning("No videos found for this channel.")
                return
                
            st.success(f"Found {len(video_urls)} videos. Analyzing content...")
            
        except Exception as e:
            st.error(f"Error fetching videos: {str(e)}")
            return

        # Prepare data structure
        data = {
            "Title": [],
            "URL": [],
            "Category": [],
            "Is Educational?": [],
            "Beyond Exams Category": [],
        }

        # Create a progress bar for analysis
        analysis_progress = st.progress(0, text="Analyzing videos...")
        
        # Analyze each video
        for i, video_url in enumerate(video_urls):
            try:
                v = Video.getInfo(video_url, mode=ResultMode.json)
                t = v.get("title", "No title")
                c = v.get("category", "Unknown")
                
                isEdu, isCat, cat_array, sub_array = predictCategoryFor(video_url)
                
                data["Title"].append(t)
                data["URL"].append(video_url)
                data["Category"].append(c)
                data["Is Educational?"].append(isEdu)
                data["Beyond Exams Category"].append(isCat)
                
                # Update progress
                analysis_progress.progress((i + 1) / len(video_urls), 
                                         text=f"Analyzing videos... {i+1}/{len(video_urls)}")
                
            except Exception as e:
                st.warning(f"Error analyzing video {video_url}: {str(e)}")
                continue
        
        analysis_progress.empty()

        # Create and display dataframe
        if data["Title"]:
            df = pd.DataFrame(data)
            st.dataframe(df)
            
            # Add download button
            csv = convert_df(df)
            st.download_button(
                "Download this dataframe",
                csv,
                "channel_analysis.csv",
                "text/csv",
                key='download-csv'
            )
            
            # Show summary statistics
            st.subheader("Channel Summary")
            total_videos = len(df)
            edu_videos = sum(1 for status in df["Is Educational?"] if status == "Educational")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Videos Analyzed", total_videos)
            with col2:
                st.metric("Educational Videos", f"{edu_videos} ({int(edu_videos/total_videos*100)}%)")
                
            # Show category distribution
            if edu_videos > 0:
                st.subheader("Category Distribution")
                category_counts = df[df["Is Educational?"] == "Educational"]["Beyond Exams Category"].value_counts()
                st.bar_chart(category_counts)
        else:
            st.warning("No videos could be analyzed successfully.")
            
    except Exception as e:
        st.error(f"ERROR: {str(e)}")
        st.error("Please enter a correct YouTube channel URL or video URL.")
        traceback.print_exc()

# Example usage:
# generate_channel_video_data(of_channel="https://www.youtube.com/channel/UCgHn1lIrwR5AqmqDN-m8wXA", with_number_of_videos=10)