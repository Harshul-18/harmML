from youtubesearchpython import Transcript, Video, ResultMode
import pickle
from stqdm import stqdm
import os
import traceback
from categoryPredictor import load_model

def eduContentPrediction(url):
    """
    Predict the educational content percentage in a YouTube video.
    
    Args:
        url: YouTube video URL
        
    Returns:
        String describing the educational content percentage
    """
    try:
        # Get the absolute path to the models directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(current_dir, "models")
        
        # Try to get transcript
        segments = Transcript.get(url)["segments"]
        E = 0
        NonE = 0
        
        # Load education model
        education_model_path = os.path.join(models_dir, "educated_model.pkl")
        education_model = load_model(education_model_path)

        timer = stqdm(segments)

        for segment in timer:
            timer.set_description("☕️ Have a coffee, while we apply our model on the video transcript.  ")
            text = [str(segment["text"])]
            text_prediction = education_model.predict(text)[0]
            if text_prediction == 0:
                E += 1
            else:
                NonE += 1

        # Avoid division by zero
        if E + NonE == 0:
            return "Could not analyze the educational content of this video."
            
        return "The {:.2f}% portion of this video is educational.".format(E*100/(E+NonE))
    except Exception as e:
        # Fallback to title and description if transcript is not available
        try:
            video = Video.getInfo(url, mode=ResultMode.json)
            title = video.get("title", "")
            description = video.get("description", "")
            
            # Load education model
            education_model_path = os.path.join(models_dir, "educated_model.pkl")
            education_model = load_model(education_model_path)
            
            text = [title + " " + description]
            prediction = education_model.predict(text)[0]
            
            if prediction == 0:
                return "This video appears to be educational based on its title and description."
            else:
                return "This video does not appear to be educational based on its title and description."
        except Exception as e:
            return "Error analyzing video. This may be because the video doesn't have transcripts available."

# print(eduContentPrediction("https://www.youtube.com/watch?v=OTuph9pJWU4"))