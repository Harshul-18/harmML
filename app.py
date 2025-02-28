from matplotlib import pyplot as plt
from pytube import YouTube
from streamlit_player import st_player
from bokeh.models.widgets import Div
from youtube_dl import YoutubeDL
from stqdm import stqdm
from PIL import Image
from io import BytesIO

from colors import colorOf
from categoryPredictor import predictCategoryFor
from statsViewer import generate_channel_video_data
from eduContentPredictor import eduContentPrediction
from youtubesearchpython import Video, ResultMode, VideosSearch, Playlist, ChannelsSearch

import streamlit as st
import base64
import pandas as pd
import chime
import pytube
import toml
import webbrowser
import numpy as np
import youtube_dl
import os
import sys

# Check if model files exist and download them if needed
def check_models():
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    if not os.path.exists(model_dir):
        st.warning("Model directory not found. Creating it...")
        os.makedirs(model_dir, exist_ok=True)
    
    # Check for at least one essential model file
    essential_model = os.path.join(model_dir, "educated_model.pkl")
    if not os.path.exists(essential_model):
        st.warning("Model files not found. Please download them using the download_models.py script.")
        if st.button("Download Models Now"):
            try:
                import download_models
                download_models.main()
                st.success("Models downloaded successfully! Please refresh the page.")
            except Exception as e:
                st.error(f"Error downloading models: {str(e)}")
                st.info("Please download the models manually and place them in the 'models' directory.")
        return False
    return True

st.set_page_config(page_title="HARM Bot", page_icon=Image.open("./assets/harmLogo.ico"))
# primaryColor = toml.load(".streamlit/config.toml")['theme']['primaryColor']
s = f"""
<style>
body {{ background-colour: #160000; }}
div.stButton > button:first-child {{ border: 1px solid #FFF; border-radius:20px 20px 20px 20px; background: none;}}
div.stButton > button:first-child:hover {{
    background: #E11D48;
    color: white;
}}
<style>
"""
st.markdown(s, unsafe_allow_html=True)

# MARK: hiding the the streamlit footer and main menu for the users
def hide_streamlit_style():
    hideStreamlitStyle = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hideStreamlitStyle, unsafe_allow_html=True)

# MARK: Adding the sidebar menu
def add_sidebar_menu():
    with st.sidebar:

        st.markdown('''
            <p>By <b>HARM</b>, an intern team, aims to expand the world of AI by providing an useful feature.</p>
        ''', True)

        st.markdown("### Team Members ")

        if st.button("Harshul Nanda"):
            webbrowser.open_new_tab("https://www.linkedin.com/in/harshulnanda/")
        if st.button("Abhijeet Saroha"):
            webbrowser.open_new_tab('https://www.linkedin.com/in/abhijeet-saroha-a19031229/')
        if st.button("Rishabh Sagar"):
            webbrowser.open_new_tab('https://www.linkedin.com/in/rishabh-sagar-1b0b74229/')
        if st.button("Mayank Arora"):
            webbrowser.open_new_tab('https://www.linkedin.com/in/mayank-arora-24713322a/')


        st.markdown("### Contact us ")

        if st.button("GitHub"):
            webbrowser.open_new_tab('https://github.com/Harshul-18')
        if st.button("Linked In"):
            webbrowser.open_new_tab('https://www.linkedin.com/company/82157293/admin/')

        # path = "https://www.buymeacoffee.com/widget/page/HARMBOT?description=Support%20me%20on%20Buy%20me%20a%20coffee!&color=%235F7FF"
        # if st.button("Buy us a coffee"):
        #     webbrowser.open_new_tab(path)

        st.markdown("""<a href="https://www.buymeacoffee.com/HARMBOT" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-red.png" alt="Buy Us A Coffee" height="40" width="164" style="border: 1px solid white; border-radius: 16px;"></a>""", unsafe_allow_html=True)
    
    page_bg_img = """
    <style>
    [data-testid="stSidebar"] > div:first-child {
        background-image: url("assets/sidebarBackground.jpg");
        background-position: center;
        background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# MARK: Adding the HARM logo gif
def add_image(with_path):
    file_ = open(with_path, "rb")
        
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<center><img src="data:image/gif;base64,{data_url}" alt="harmLogo" width=300 height=125></center>',
        unsafe_allow_html=True,
    )

# MARK: Adding the title
def add_title_text():
    st.title("Hello, I am a YouTube API Bot!")
    st.text("I am a simple tool, just enter the URL and I will give the statistics.")

# MARK: Adding body for page 1 containing all the fields while the youtube video url text input field is not empty
def bodyOfPage1():
    youtubeVideoUrl = st.text_input("Enter the URL of the Youtube Video", value="", type="default", help="Enter the URL of the Youtube video you want me to show the statistics and predict the category for.")

    try:
        if youtubeVideoUrl:
            # Check if the URL is valid before proceeding
            try:
                video = Video.getInfo(youtubeVideoUrl, mode=ResultMode.json)
                
                with st.expander("Prediction"):
                    try:
                        isEdu, isCat, catArr, probArr = predictCategoryFor(url=youtubeVideoUrl)
                        if isEdu == "Educational":
                            st.markdown(
                                f"<h5>This video comes under the {isCat} category.</h5>",
                                unsafe_allow_html=True,
                            )
                            plt.figure(facecolor="#ffffff")
                            fig, x = plt.subplots(facecolor="#ffffff")
                            p = x.barh([i for i in range(1, len(catArr)+1)], probArr, tick_label=catArr, color="#E11D48")
                            x.set_facecolor("#ffffff")
                            x.spines['bottom'].set_color('black')
                            x.spines['top'].set_color('black') 
                            x.spines['right'].set_color('black')
                            x.spines['left'].set_color('black')
                            x.tick_params(axis='x', colors='black')
                            x.tick_params(axis='y', colors='black')
                            x.bar_label(p, label_type="center", color="black")
                            st.pyplot(fig)
                        else:
                            st.markdown(
                                f"<h5>This is not an educational video.</h5>",
                                unsafe_allow_html=True,
                            )
                    except Exception as e:
                        st.error(f"Error in prediction: {str(e)}")

                with st.expander("View Video"):
                    st_player(youtubeVideoUrl) 
                    
                    try:
                        # Check if video data exists and contains required fields
                        if video and "channel" in video and "name" in video["channel"] and "title" in video and "description" in video:
                            st.markdown("**Author of this video:** " + str(video["channel"]["name"]))
                            st.markdown("**Title of video:** " + str(video["title"]))
                            st.markdown("**Description of video:** " + str(video["description"]))
                            chime.success()
                        else:
                            st.warning("Some video details are not available")
                    except Exception as e:
                        st.error(f"Unable to view the video details: {str(e)}")
                        chime.error()
            except Exception as e:
                st.error(f"Invalid YouTube URL: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}. Please enter a correct YouTube video URL.")

# MARK: Adding body for page 2 containing the fields for channel's statistics
def bodyOfPage2():
    youtubeChannelUrl = st.text_input("Enter the Channel ID to get the stats of that channel", value="", type="default", help="Enter the Channel's ID you want me to show the data of its channel.")
    # youtubeChannelUrl += "/videos"
    number = st.number_input('How many videos to analyse?', min_value=5, step=5, help="Enter the number or click the + or - buttons to increase or decrease the number with step size 5 for getting the data for the number of videos you entered.")
    if len(youtubeChannelUrl) >= 1:
        try:
            with st.expander("View Statistics"):
                generate_channel_video_data(of_channel=youtubeChannelUrl, with_number_of_videos=number)            
        except Exception as e:
            st.markdown(f"{e}, Please enter the correct channel ID")

# MARK: Adding body for page 3 containing the fields for searching a video from youtube
def bodyOfPage3():
    searchFor = st.text_input("Search for videos", value="", type="default", help="Enter a keyword for searching for a youtube video.")
    number = st.number_input('Show search results', min_value=1, step=1, help="Enter the number or click the + or - buttons to increase or decrease the number for getting the number of videos you entered.")

    
    if len(searchFor) >= 1:
        videosSearch = VideosSearch(searchFor, limit=number)

        result = [video['link'] for video in videosSearch.result()['result']]

        for youtubeVideoUrl in stqdm(result):
            
            with st.container():
                st_player(youtubeVideoUrl)
            
            with st.expander("Prediction"):

                isEdu, isCat, catArr, probArr = predictCategoryFor(url=youtubeVideoUrl)
                if isEdu == "Educational":
                    st.markdown(
                        f"<h5>This video comes under the {isCat} category.</h5>",
                        unsafe_allow_html=True,
                    )
                    plt.figure(facecolor="#ffffff")
                    fig, x = plt.subplots(facecolor="#ffffff")
                    p = x.barh([i for i in range(1, len(catArr)+1)], probArr, tick_label=catArr, color="#E11D48")
                    x.set_facecolor("#ffffff")
                    x.spines['bottom'].set_color('black')
                    x.spines['top'].set_color('black') 
                    x.spines['right'].set_color('black')
                    x.spines['left'].set_color('black')
                    x.tick_params(axis='x', colors='black')
                    x.tick_params(axis='y', colors='black')
                    x.bar_label(p, label_type="center", color="black")
                    st.pyplot(fig)
                else:
                    st.markdown(
                        f"<h5>This is not an educational video.</h5>",
                        unsafe_allow_html=True,
                    )

# MARK: Adding body for page 4 containing the field for predicting category for videos in a playlist
def bodyOfPage4():
    playlist = st.text_input("Enter a YouTube playlist url", value="", type="default", help="Enter url of a youtube playlist.")

    if len(playlist) >= 1:
        
        try:
            playlistVideos = Playlist.getVideos(playlist)

            for i in playlistVideos["videos"]:
                url = i["link"].split("list")[0][:-1]
                with st.container():
                    st_player(url)
                
                    with st.expander("Prediction"):

                        isEdu, isCat, catArr, probArr = predictCategoryFor(url=url)
                        if isEdu == "Educational":
                            st.markdown(
                                f"<h5>This video comes under the {isCat} category.</h5>",
                                unsafe_allow_html=True,
                            )
                            plt.figure(facecolor="#ffffff")
                            fig, x = plt.subplots(facecolor="#ffffff")
                            p = x.barh([i for i in range(1, len(catArr)+1)], probArr, tick_label=catArr, color="#E11D48")
                            x.set_facecolor("#ffffff")
                            x.spines['bottom'].set_color('black')
                            x.spines['top'].set_color('black') 
                            x.spines['right'].set_color('black')
                            x.spines['left'].set_color('black')
                            x.tick_params(axis='x', colors='black')
                            x.tick_params(axis='y', colors='black')
                            x.bar_label(p, label_type="center", color="black")
                            st.pyplot(fig)
                        else:
                            st.markdown(
                                f"<h5>This is not an educational video.</h5>",
                                unsafe_allow_html=True,
                            )
        except Exception as e:
            st.markdown(f"Please enter the correct URL")

# MARK: Adding body for page 5 containing the field for predicting the educational content percentage in a video.
def bodyOfPage5():
    youtubeVideoUrl = st.text_input("Enter a Youtube Video URL", value="", type="default", help="Enter a URL of the Youtube Video you want me to tell the educational portion content in the video.")
    try:
        if youtubeVideoUrl:
            st.markdown(f"### {eduContentPrediction(youtubeVideoUrl)}")
    except:
        st.markdown("Please enter a correct YouTube video URL or This video's transcripts are not available.")

# MARK: Adding the footer
def add_footer():
    footer="""<style>
a:link , a:visited{
color: white;
font-weight: bold;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: none;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}

</style>
<div class="footer">
<p>Copyright © <a href="https://www.linkedin.com/company/82157293/admin/">HARM</a>, Designed by <a href="https://harshul-18.github.io/Harshul-Site/">Harshul</a>.</p>
</div>
"""

    st.markdown(footer, True)

if __name__ == "__main__":

    hide_streamlit_style()
    add_image(with_path="./assets/harmLogo.gif")
    add_title_text()
    
    # Check if models exist before proceeding
    models_exist = check_models()
    
    if models_exist:
        page_names_to_funcs = {
            "Category Predictor": bodyOfPage1,
            "Channel Stats Viewer": bodyOfPage2,
            "Search Videos": bodyOfPage3,
            "Playlist Videos Predictor": bodyOfPage4,
            "Educational Content in a Video": bodyOfPage5,
        }
        selected_page = st.sidebar.selectbox("Select the page", page_names_to_funcs.keys())
        page_names_to_funcs[selected_page]()
        add_sidebar_menu()
        add_footer()
    else:
        st.info("Please download the model files to use this application.") 
