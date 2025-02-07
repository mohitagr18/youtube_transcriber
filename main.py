# Import Libraries

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from a .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Get transcript from YouTube video
def get_youtube_transcript(video_url):
    video_id = video_url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([item['text'] for item in transcript])
    return transcript_text

# Get thumbnail from YouTube video
def get_youtube_thumbnail(video_url):
    video_id = video_url.split("v=")[-1]
    print(video_id)
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    return thumbnail_url

# Load model and get response
model = genai.GenerativeModel("gemini-1.5-flash-002")
def get_response(transcript_text, prompt):
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Prompt Template
input_prompt = """
You are an expert video transcriber. Given the transcript of a YouTube video, provide a concise and informative summary of the video in approximately 250 words.
Export the response in the following format:

**Video Topic:**
[Insert video topic here]

**Detailed Summary:**
[Insert detailed summary here]

**Key Points:**
1. [Key point 1]
2. [Key point 2]
3. [Key point 3]
"""

# Initialize query count    
if "query_count" not in st.session_state:
    st.session_state['query_count'] = 0
    st.session_state['submit_disabled'] = False

# Manage query count
def manage_query_count():
    if st.session_state['query_count'] >= 5:
        st.warning("You have reached the limit of 5 queries. Please try again later.")
        st.session_state['submit_disabled'] = True
    else:
        st.session_state['query_count'] += 1
        st.session_state['submit_disabled'] = False

# Write the main function to run the app
def main():
    # Set the title of the app
    st.set_page_config(page_title="YouTube Transcriber", page_icon="🎥")
    st.title("YouTube Transcriber")
    st.write("")
    st.markdown("Unlock the secrets of YouTube...without actually watching! This app uses the power of Google Gemini to provide transcripts, summaries, and key points – saving you from endless cat videos (probably)")
    st.write("")
    
    youtube_link = st.text_input("Enter the YouTube video URL:", help="Paste the full URL of the YouTube video you want to transcribe.")
    submit = st.button("Transcribe", disabled=st.session_state['submit_disabled'])
    if youtube_link:
        thumbnail_url = get_youtube_thumbnail(youtube_link)
        st.image(thumbnail_url, use_container_width=True)
        if submit:
            manage_query_count()
            if not st.session_state['submit_disabled']:
                try:
                    transcript_text = get_youtube_transcript(youtube_link)
                    print(transcript_text)
                    response = get_response(transcript_text, input_prompt)
                    st.subheader("Response:")
                    st.write(response)
                except Exception as e:
                    st.write("An error occurred:", e)
    elif youtube_link == "":
        pass
    else:
        st.warning("Please paste a YouTube video link")

# Run the app
if __name__ == "__main__":
    main()
