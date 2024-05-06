import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity Copywriting",
        layout="wide",
        page_icon="img/logo.png"
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


def title_and_description():
    st.title("🧕 Alwrity - AI Generator for STAR Copywriting Formula")


def input_section():
    with st.expander("**PRO-TIP** - Easy Steps to Create Compelling STAR Copy", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('Enter Brand/Company Name',
                               help="Enter the name of your brand or company.")
            situation = st.text_input('**Set the Situation for Your Target Audience**',
                              help="Describe, background for the problem or need.",
                              placeholder="In a busy city, Late Delivery, Unsafe Activities, Unprofessional Service..")
            action = st.text_input(f'**Explain the Actions Taken to Solve the Problem**',
                           help="Describe the specific actions taken to address the challenge or objective.",
                           placeholder="New strategy, launched campaign, better service, New product...")

        with col2:
            task = st.text_input(f'**Describe the Specific Need to be Addressed**',
                         help="Explain the tasks or objectives that needs to be done.",
                         placeholder="Increase website traffic by 30%, improve customer satisfaction, Safe Travels...")
            result = st.text_input(f'**Highlight Benefits Achieved from the Actions**',
                           help="Describe the benefits achieved as a result of the actions.",
                           placeholder="Improved customer engagement, sales revenue, Happy customers, Improved Service X...")

        if st.button('**Get STAR Copy**'):
            if situation.strip() and task.strip() and action.strip() and result.strip():
                with st.spinner("Generating STAR Copy..."):
                    star_copy = generate_star_copy(brand_name, situation, task, action, result)
                    if star_copy:
                        st.subheader('**👩🔬🧕 Your STAR Copy**')
                        st.markdown(star_copy)
                    else:
                        st.error("💥 **Failed to generate STAR copy. Please try again!**")
            else:
                st.error("All fields are required!")


def generate_star_copy(brand_name, situation, task, action, result):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name}. 
        Your task is to use the STAR (Situation-Task-Action-Result) framework to craft 3 compelling copies.
        Here's the breakdown:
        - Situation: {situation}
        - Task: {task}
        - Action: {action}
        - Result: {result}
        Do not provide explanations, provide the final marketing copy.
    """
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

