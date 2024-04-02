import openai
import streamlit as st
from PIL import Image
import os
from streamlit_chat import message
import googlemaps
import random
import numpy as np
from streamlit_option_menu import option_menu

# Set Streamlit page configuration
st.set_page_config(
    page_title="Mindful Mate",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Set OpenAI API key
openai.api_key = "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"
googlemaps_api_key = "AIzaSyDHhQL4h-K7sER8Z9bZ41dWR6jowTNM-2A"

# Initialize Google Maps client
gmaps = googlemaps.Client(key=googlemaps_api_key)

# Custom CSS styles
styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF; /* White text */
}

.sidebar .sidebar-content {
    background-color: #1F2833; /* Dark blue background */
    padding: 2rem 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.sidebar .sidebar-content .sidebar-item {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    transition: background-color 0.3s ease;
    background-color: #FFFFFF; /* White background for sidebar items */
    color: #1F2833; /* Dark blue text for sidebar items */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

.sidebar .sidebar-content .sidebar-item:hover {
    background-color: #D9E2EC;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    transform: translateY(-2px);
}

.sidebar .sidebar-content .sidebar-item-icon {
    margin-right: 1rem;
    font-size: 1.25rem;
    color: #1F2833; /* Dark blue icon color */
}

.sidebar .sidebar-content .sidebar-item-label {
    font-size: 1rem;
    font-weight: 500;
    color: #1F2833; /* Dark blue text color */
}

.sidebar .sidebar-content .sidebar-item-label:hover {
    color: #1F2833; /* Dark blue text color */
}

.streamlit-container {
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.stButton button {
    background-color: #1F2833; /* Dark blue button background */
    color: #FFFFFF; /* White button text */
    border: none;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

.stButton button:hover {
    background-color: #2C5F56;
    transform: translateY(-2px);
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

.stButton button:active {
    background-color: #1F2833; /* Dark blue button background */
    transform: translateY(0);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

.stTextInput input {
    border: 1px solid #D9E2EC;
    border-radius: 0.25rem;
    padding: 0.5rem;
    font-size: 1rem;
    font-weight: 400;
    transition: all 0.3s ease;
    color: #FFFFFF; /* White text color for input */
}

.stTextInput input:focus {
    outline: none;
    border-color: #1F2833; /* Dark blue border color */
    box-shadow: 0 0 0 2px rgba(31, 40, 51, 0.2); /* Dark blue border shadow */
}

/* Sidebar styles */
.sidebar .sidebar-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #FFFFFF; /* White text */
    text-align: center;
    margin-bottom: 1rem;
}

.sidebar .sidebar-navigation {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

.sidebar .sidebar-navigation li {
    margin-bottom: 0.5rem;
}

.sidebar .sidebar-navigation a {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    text-decoration: none;
    color: #FFFFFF; /* White text */
    background-color: #1F2833; /* Dark blue background */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    transition: all 0.3s ease;
}

.sidebar .sidebar-navigation a:hover {
    background-color: #2C5F56;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    transform: translateY(-2px);
}

.sidebar .sidebar-navigation a .icon {
    margin-right: 1rem;
    font-size: 1.25rem;
    color: #FFFFFF; /* White icon color */
}

.sidebar .sidebar-navigation a.active {
    background-color: #2C5F56;
    color: #FFFFFF; /* White text */
}
</style>
"""
st.markdown(styles, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    # Add logo with circular border
    st.sidebar.image("Mindful Mate.jpg", width=100, caption="", use_column_width=False, output_format="JPEG")
    
    # Add menu options
    selected = option_menu(
        menu_title=None,
        options=["Homepage", "Chatbot", "Nearby Hospital", "Game"],
        icons=["house", "robot", "hospital", "joystick"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#2C5F56"},  # Dark green background for sidebar
            "icon": {"color": "#FCFCFC", "font-size": "18px"},  # White icon color
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#FCFCFC",  # White text color
                "font-family": "inherit",  # Use the same font as the selected link
                "--hover-color": "#eee",  # Light gray hover color
            },
            "nav-link-selected": {"background-color": "#1F423F", "color": "#FCFCFC", "font-family": "inherit"},  # Dark blue selected item background and white text
        },
    )

# Define functions for each page

# Page 1: Homepage
def homepage():
    st.title("Mindful Mate")
    st.image("Mindful Mate.jpg", width=300, use_column_width=False)
    st.write("""
        Welcome to Mindful Mate, your AI companion for emotional wellbeing.
Feeling stressed, anxious, or just need someone to talk to? Mindful Mate is here to lend a caring ear and provide tools to help you navigate life's challenges with greater ease.
As your empathetic AI friend, I'm available 24/7 to listen without judgment, offer encouragement, and guide you through simple mindfulness practices. Whether you need a check-in, want to talk through worries, or could use help unwinding, I'm here to support your mental health journey.
In addition to being your supportive companion, I can also:
🏥 Locate nearby hospitals and mental health resources with our easy locator tool.
✂️ Take a break and have some fun with a quick game of rock, paper, scissors.
My role is to be your ally, not to replace professional care. However, I'm always a message away when you need a friendly voice or extra support between appointments.
Let's walk the path of wellbeing together. I'm here to listen, anytime.
    """)

# Page 2: Chatbot
def chatbot():
    st.title("Mental Health Chatbot")

    # Generate empty lists for generated and past.
    ## generated stores AI generated responses
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ['Hello Friends, how may I help you?']
    ## past stores User's questions
    if 'past' not in st.session_state:
        st.session_state['past'] = ['Hi']

    # Layout of input/response containers
    response_container = st.container()
    input_container = st.container()

    # User input
    ## Function for taking user provided prompt as input
    def get_text():
        text = st.text_input("You: ", "", key="input", on_change=submit_on_enter)
        return text

    ## Callback to clear input field on Enter key press
    def submit_on_enter():
        text = st.session_state["input"]
        if text:
            user_input = text
            response = CustomChatGPT(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
            st.session_state["input"] = ""

    ## Applying the user input box
    with input_container:
        user_input = get_text()

    messages = [{"role": "system", "content": "You are a friendly mental health adviser providing mental health support and service."}]

    def CustomChatGPT(user_input):
        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        return ChatGPT_reply

    ## Conditional display of AI generated responses as a function of user provided prompts
    with response_container:
        if user_input:
            response = CustomChatGPT(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
            
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

# Page 3: Nearby Hospital
def nearby_hospital():
    st.title("Find Nearby Hospital if you're feeling low")
    postal_code = st.text_input("Enter your postal code:", key="postal code hospital")
    if st.button("Search"):
        if postal_code:
            # Function to find 5 highest-rated hospitals based on postal code
            def find_top_hospitals(postal_code):
                # Use Google Maps API to geocode the postal code
                geocode_result = gmaps.geocode(postal_code)
                if geocode_result:
                    location = geocode_result[0]['geometry']['location']
                    # Use Google Maps Places API to find nearby hospitals
                    hospitals = gmaps.places_nearby(location, radius=5000, type='hospital', keyword='mental health')
                    if hospitals:
                        # Sort hospitals by rating
                        hospitals_sorted = sorted(hospitals['results'], key=lambda x: x.get('rating', 0), reverse=True)
                        # Take the top 5 hospitals based on rating                
                        top_hospitals = hospitals_sorted[:5]
                        return top_hospitals
                return None

            hospitals = find_top_hospitals(postal_code)
            if hospitals:
                # Display top 5 hospitals information
                for hospital in hospitals:
                    st.write(hospital['name'], hospital['vicinity'])
            else:
                st.write("No hospitals found nearby or unable to retrieve data.")
        else:
            st.warning("Please enter a valid postal code.")

# Page 4: Game - Rock, Paper, Scissors
def game():
    st.title('Rock, Paper, Scissors Game')
    st.write("Choose Rock, Paper, or Scissors and see if you can beat the computer!")

    def play_game(user_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)

        if user_choice == computer_choice:
            return "It's a tie! The computer also chose " + computer_choice
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Paper" and computer_choice == "Rock") or \
             (user_choice == "Scissors" and computer_choice == "Paper"):
            return "You win! The computer chose " + computer_choice
        else:
            return "You lose! The computer chose " + computer_choice

    user_choice = st.radio("Choose your option:", ["Rock", "Paper", "Scissors"])

    if st.button("Play"):
        result = play_game(user_choice)
        st.success(result)

# Display selected page
if selected == "Homepage":
    homepage()
elif selected == "Chatbot":
    chatbot()
elif selected == "Nearby Hospital":
    nearby_hospital()
elif selected == "Game":
    game()