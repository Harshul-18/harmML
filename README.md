# HARM YouTube API Bot

Checkout YouTube Video for Explanation

[![HARM YouTube API Bot Explanation](https://img.youtube.com/vi/1l_yfh6nHic/0.jpg)](https://www.youtube.com/watch?v=1l_yfh6nHic)

A machine learning application that analyzes YouTube videos to determine if they are educational, categorizes them, and provides statistics.

## Features

- **Category Predictor**: Determines if a video is educational and categorizes it
- **Channel Stats Viewer**: Analyzes multiple videos from a channel
- **Search Videos**: Search for videos and analyze them
- **Playlist Videos Predictor**: Analyze all videos in a playlist
- **Educational Content Analyzer**: Determine the percentage of educational content in a video

## Installation

1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## Deployment Options

### Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Select the repository and branch
5. Set the main file path to `app.py`
6. Deploy!

### Heroku

1. Create a Heroku account
2. Install the Heroku CLI
3. Login to Heroku:
   ```
   heroku login
   ```
4. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```
5. Push to Heroku:
   ```
   git push heroku main
   ```

### Hugging Face Spaces

1. Create a Hugging Face account
2. Create a new Space with Streamlit SDK
3. Upload your files or connect to your GitHub repository
4. The app will automatically deploy

## Environment Variables

No environment variables are required for this application.

## Models

The application uses several machine learning models:
- `educated_model.pkl`: Determines if a video is educational
- `cat_model.pkl`: Categorizes educational videos
- Various category-specific models for subcategorization

## Team

Created by HARM, an intern team:
- Harshul Nanda
- Abhijeet Saroha
- Rishabh Sagar
- Mayank Arora

Checkout HARMML Channel for more Coding Related Content 

[![YouTube Channel](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@harm_/videos)
