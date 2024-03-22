import openai
import streamlit as st
from PIL import Image
import os
from streamlit_chat import message
import googlemaps
import random

# Set Streamlit page configuration
st.set_page_config(page_title="Mindful Mate", page_icon=":robot:")

# Set OpenAI API key
openai.api_key = "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"
googlemaps_api_key = "AIzaSyDHhQL4h-K7sER8Z9bZ41dWR6jowTNM-2A"

# Initialize Google Maps client
gmaps = googlemaps.Client(key=googlemaps_api_key)

# Define page background styling
page_bg = f"""
<style>
[data-testid="stSidebar"] {{
background-color:#1F423F;
}}

[data-testid="stToolbar"] {{
background-color:#FCFCFC;
}}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)
 
# Sidebar contents for navigation
with st.sidebar:
    st.title('Navigation')
    page_selection = st.radio('Go to', ['Homepage', 'Chatbot', 'Nearby Hospital', 'Game'])

# Define functions for each page

# Page 1: Homepage
def homepage():
    st.title('Mindful Mate')
    st.write("""
        
    Mindful Mate is your empathetic AI friend, here to provide a listening ear, encouragement, 
    and tools to help you care for your mental wellbeing. 
    As your personal mental health companion, I'm available anytime you need a check-in, want to talk through worries, 
    or could use help practicing mindfulness and self-care.
    """)

# Page 2: Chatbot
def chatbot():
    st.title('Mental Health Chatbot')

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
            model = "gpt-3.5-turbo",
            messages = messages,
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
    st.title('Find Nearby Hospital if youre feeling low ')
    postal_code = st.text_input("Enter your postal code:")
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

# Page 4: Game
def game():
    st.title('Car Racing Game')
    st.write("Use the left and right arrow keys to move the car and avoid the obstacles!")

    # Define the canvas size and car position
    canvas_width = 600
    canvas_height = 400
    car_width = 50
    car_height = 80
    car_x = canvas_width // 2
    car_y = canvas_height - car_height - 20

    # Define the obstacle properties
    obstacle_width = 100
    obstacle_height = 20
    obstacle_speed = 5
    obstacle_x = random.randint(0, canvas_width - obstacle_width)
    obstacle_y = -obstacle_height

    # Function to draw the car
    def draw_car():
        st.image('car.png', width=car_width)

    # Function to draw the obstacle
    def draw_obstacle():
        st.image('obstacle.png', width=obstacle_width)

    # Function to move the car
    def move_car(direction):
        nonlocal car_x
        if direction == 'left':
            car_x -= 10
        elif direction == 'right':
            car_x += 10

    # Function to update the obstacle position
    def update_obstacle():
        nonlocal obstacle_y
        obstacle_y += obstacle_speed
        if obstacle_y > canvas_height:
            reset_obstacle()

    # Function to reset the obstacle position
    def reset_obstacle():
        nonlocal obstacle_x, obstacle_y
        obstacle_x = random.randint(0, canvas_width - obstacle_width)
        obstacle_y = -obstacle_height

    # Main game loop
    while True:
        st.image('background.png', width=canvas_width, height=canvas_height)
        draw_car()
        draw_obstacle()
        update_obstacle()
        st.write("Score: 0")
        st.write("Time: 0s")
        st.write("High Score: 0")
        st.write("Time Spent: 0s")

# Display selected page
if page_selection == 'Homepage':
    homepage()
elif page_selection == 'Chatbot':
    chatbot()
elif page_selection == 'Nearby Hospital':
    nearby_hospital()
elif page_selection == 'Game':
    game()
