from google import genai
import streamlit as st

client = genai.Client(api_key=st.secrets["OPENROUTER_API_KEY"])

def run_agents(claim):

    agents = {
        "Extractor Agent": f"Extract important claim information from this: {claim}",
        "Validator Agent": f"Check policy validity and missing fields: {claim}",
        "Fraud Agent": f"Detect fraud indicators in this claim: {claim}",
        "Decision Agent": f"Should this claim be approved or investigated? {claim}"
    }

    responses = {}

    for name, prompt in agents.items():

        r = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        responses[name] = r.text

    return responses