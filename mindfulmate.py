import openai
import streamlit as st
import googlemaps
from PIL import Image
import os
from streamlit_chat import message
import random
from streamlit_extras.colored_header import colored_header

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
if page_selection == 'Homepage':
    homepage()
elif page_selection == 'Chatbot':
    chatbot()
elif page_selection == 'Nearby Hospital':
    nearby_hospital()
elif page_selection == 'Game':
    game()
 
                

# Function to fetch nearby mental health clinics

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyAj3Bdt1SvD-6kM6vrN6F7p_GDaeXOH8OQ')

def find_mental_health_facilities(postal_code, radius=10000):
    # Geocode the postal code to get its latitude and longitude
    geocode_result = gmaps.geocode(postal_code)
    if not geocode_result:
        print(f"Postal code {postal_code} not found.")
        return

    location = geocode_result[0]['geometry']['location']
    lat, lng = location['lat'], location['lng']

    # Search for mental health clinics and hospitals nearby
    places_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        type='hospital',
        keyword='mental health clinic'
    )

    return places_result['results'] if 'results' in places_result else None

        #print("No mental health clinics or hospitals found nearby.")
        
# Streamlit UI
def main():
    st.title("Find Nearest Mental Health Clinic and Hospital")
    postal_code = st.text_input("Enter your postal code:")
    if st.button("Search"):
        if postal_code:
            facilities = find_mental_health_facilities(postal_code)
            if facilities:
                st.header('Results:')
                for place in facilities:
                    name = place['name']
                    address = place['vicinity']
                    st.write(f"- {name}: {address}")
            else:
                st.error("No mental health clinics or hospitals found nearby.")
        else:
            st.warning("Please enter a valid postal code.")

if __name__ == "__main__":
    main()
