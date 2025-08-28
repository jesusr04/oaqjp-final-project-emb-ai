"""
Emotion Detection Server Module.

This Flask web application provides endpoints for emotion detection analysis.
It uses the EmotionDetection module to analyze text input and return 
emotion scores along with the dominant emotion.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/")
def render_index_page():
    """
    Render the main index page.
    
    Returns:
        str: Rendered HTML template for the index page
    """
    return render_template('index.html')

@app.route("/emotionDetector")
def sent_analyzer():
    """
    Analyze text for emotion detection and return formatted results.
    
    Processes the 'textToAnalyze' query parameter through emotion detection
    and returns a formatted string with emotion scores and dominant emotion.
    
    Returns:
        str: Formatted string containing emotion analysis results
        tuple: Error message and status code (400) for invalid input
    """
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid Text! Please try again!", 400

    response = emotion_detector(text_to_analyze)

    emotions = {k: v for k, v in response.items() if isinstance(v, (int, float))}

    anger = emotions.get('anger', 0)
    disgust = emotions.get('disgust', 0)
    fear = emotions.get('fear', 0)
    joy = emotions.get('joy', 0)
    sadness = emotions.get('sadness', 0)

    dominant_emotion = max(emotions, key=emotions.get)

    output_str = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return output_str

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
