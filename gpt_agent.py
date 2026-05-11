from google import genai
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def investigate_claim(text):

    prompt = f"""
    You are an insurance fraud investigator AI.

    Analyze the following claim and tell:
    - fraud risk
    - suspicious indicators
    - recommendation

    Claim:
    {text}
    """

    r = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return r.text