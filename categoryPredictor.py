from youtubesearchpython import Video, ResultMode
from colors import colorOf, dataset

import numpy as np
import matplotlib.pyplot as plt
import requests
import pickle
import warnings
import os
import sys
warnings.filterwarnings("ignore")

# Cache for loaded models to avoid reloading them for each prediction
_model_cache = {}

def load_model(model_path):
    """Load a model from cache or disk with error handling"""
    if model_path in _model_cache:
        return _model_cache[model_path]
    
    try:
        model = pickle.load(open(model_path, "rb"))
        _model_cache[model_path] = model
        return model
    except Exception as e:
        raise Exception(f"Error loading model from {model_path}: {str(e)}")

def predictCategoryFor(url):
    """
    Predict the educational category for a YouTube video.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Tuple of (educational status, category, subcategories, subcategory probabilities)
    """
    try:
        # Get the absolute path to the models directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(current_dir, "models")
        
        # Get video info
        video = Video.getInfo(url, mode=ResultMode.json)
        
        # Extract text for prediction
        text = [video["title"] + " " + video["description"]]
        categories = sorted(list(dataset.keys()))
        
        # Load and apply education model
        education_model_path = os.path.join(models_dir, "educated_model.pkl")
        education_model = load_model(education_model_path)
        education_prediction = education_model.predict(text)[0]

        if education_prediction == 0:
            # Educational content - get category
            category_model_path = os.path.join(models_dir, "cat_model.pkl")
            category_classifier = load_model(category_model_path)
            
            category_idx = category_classifier.predict(text)[0]
            category_prediction = categories[category_idx]
            
            # Get subcategory probabilities
            sub_cat_model_path = os.path.join(models_dir, f"{category_prediction.lower().replace(' ', '_')}_model.pkl")
            sub_cat_clf = load_model(sub_cat_model_path)
            
            sub_cat_pred = sub_cat_clf.predict_proba(text)[0]
            sub_cat_pred *= 100
            subs = sorted(dataset[category_prediction])

            return ("Educational", category_prediction, subs, sub_cat_pred)
        else:
            return ("Non Educational", "", [], [])
    
    except Exception as e:
        import traceback
        return ("There must be an error in getting the title and description of the video.", "", [], [])


# print(predictCategoryFor(url="https://www.youtube.com/watch?v=bdCX8Nb_2Mg"))

