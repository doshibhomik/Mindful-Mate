import openai
import streamlit as st
import googlemaps
from PIL import Image
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="Mindful Mate", page_icon=":robot:")

openai.api_key = "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"
# # And the root-level secrets are also accessible as environment variables:
# os.environ["openai_secret_key"] == st.secrets["openai_secret_key"]

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
 
# Sidebar contents
with st.sidebar:
    # st.title('Beshie')

    image = Image.open('Mindful Mate.jpg')
    st.image(image, width=280)
    st.markdown("<h2 style='text-align: center; color: white;'> Mental Health Chatbot </h2>", unsafe_allow_html= True)

    st.markdown("<h1 style='text-align: left; color: white;'> About </h1>", unsafe_allow_html= True)
    st.markdown("""
    <p style='text-align: left; color: white;'> Mindful Mate is your empathetic AI friend, here to provide a listening ear, encouragement, 
    and tools to help you care for your mental wellbeing. 
    As your personal mental health companion, I'm available anytime you need a check-in, want to talk through worries, 
    or could use help practicing mindfulness and self-care.</p><br><br>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:white;'> Made with 💚 by <a href='https://github.com/doshibhomik/' style='color:white;'>Capstone Project</a> </p>", unsafe_allow_html=True)



# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Hello Friends, how may I help you?']
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi']

# Layout of input/response containers
# colored_header(label='', description='', color_name="green-70")
response_container = st.container()
input_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    text = st.text_input("You: ", "", key="input")
    return text

def clear_text():
    st.session_state["input"] = ""

## Applying the user input box
with input_container:
    user_input = get_text()
    st.button("Clear Text", on_click=clear_text)
 

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
