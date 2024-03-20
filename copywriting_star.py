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
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
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

def sidebar():
    st.sidebar.title("Situation-Task-Action-Result")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for STAR Copywriting Formula")
    with st.expander("What is **STAR Copywriting Formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's STAR Copywriting Formula, and How to use this AI generator 🗣️
            ---
            #### STAR Copywriting Formula

            STAR is an acronym for Situation-Task-Action-Result. It's a copywriting framework that focuses on guiding the audience through different stages:

            1. **Situation**: Setting the context or background for the problem or need.
            2. **Task**: Describing the specific challenge or objective to be addressed.
            3. **Action**: Explaining the actions taken to solve the problem or achieve the objective.
            4. **Result**: Highlighting the outcome or benefits achieved from the actions.

            The STAR formula helps in creating clear and concise copy that effectively communicates the value proposition.

            #### STAR Copywriting Formula: Simple Example

            - **Situation**: "In a fast-paced business environment..."
            - **Task**: "Our team needed a solution to streamline communication..."
            - **Action**: "We implemented a new collaboration tool..."
            - **Result**: "Resulting in improved productivity and efficiency."

            ---
        ''')


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
                        st.subheader('**👩🔬👩🔬 Your STAR Copy**')
                        st.markdown(star_copy)
                    else:
                        st.error("💥 **Failed to generate STAR copy. Please try again!**")
            else:
                st.error("All fields are required!")

    page_bottom()


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
    return openai_chatgpt(prompt)


def page_bottom():
    """Display the bottom section of the web app."""
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using STAR Copywriting Formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Situation:
    In a fast-paced business environment...

    ### Task:
    Our team needed a solution to streamline communication...

    ### Action:
    We implemented a new collaboration tool...

    ### Result:
    Resulting in improved productivity and efficiency.
    """)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=3):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()

