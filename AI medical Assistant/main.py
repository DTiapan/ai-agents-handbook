import streamlit as st
from openai import OpenAI
from mem0 import Memory
import os
from datetime import datetime, timedelta
import asyncio
from typing import Optional
import re

from dotenv import load_dotenv
load_dotenv()


# Initialize session state if not already initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#for now lets use dummy username and password, we can implement a more secure way to store this later
USERNAME = "admin"
PASSWORD = "admin"


def login():
    """Function to handle login and session management."""
    
    if st.session_state.logged_in:
        return True
    

    st.markdown(
    "<h1 style='font-size:24px;'>Please Login to start</h1>",
    unsafe_allow_html=True
    )
    
    st.write("")
    st.write("")
    st.write("")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")
            
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    return False

# Module: App Setup
def setup_app():
    st.title("🏥AI Medical History Assistant🏥")
    st.caption("**Chat with a medical assistant who remembers your patients history.**")
    

# Module: MedicalHistoryAgent
class MedicalHistoryAgent:
    def __init__(self):
        try:
            config = {
                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "collection_name": "test",
                        "host": "localhost",
                        "port": 6333,
                    }
                },
            }
            self.memory = Memory.from_config(config)
            self.client = OpenAI()
            self.app_id = "medical-history-assistant"
        except Exception as e:
            st.error(f"Failed to initialize agent: {str(e)}")
            raise

    async def add_to_memory_async(self, query, answer, patient_id):
        """Add data to memory asynchronously."""
        await asyncio.to_thread(self.memory.add, query, user_id=patient_id, metadata={"app_id": self.app_id, "role": "user"})
        await asyncio.to_thread(self.memory.add, answer, user_id=patient_id, metadata={"app_id": self.app_id, "role": "assistant"})

    def validate_patient_id(self, patient_id: str) -> Optional[str]:
            """Validate patient ID format and return cleaned ID."""
            if not patient_id:
                return None
            
            # Remove whitespace and convert to uppercase
            patient_id = patient_id.strip().upper()
            
            # Example: Require format PAT-XXXXX where X is alphanumeric
            pattern = r'^PAT-[A-Z0-9]{5}$'
            if not re.match(pattern, patient_id):
                raise ValueError("Invalid patient ID format. Must be PAT-XXXXX")
                
            return patient_id
    
    
    
    async def handle_query(self, query: str, patient_id: str) -> str:
        """Handle patient query with retries and error handling."""
        try:
            patient_id = self.validate_patient_id(patient_id)
            if not patient_id:
                return "Error: Invalid patient ID"

            relevant_memories = self.memory.search(query=query, user_id=patient_id)
            context = "Relevant past medical history:\n"
            
            full_prompt = f"{context} {relevant_memories}\nPatient: {query}\nMedical Assistant:"
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fixed model name
                messages=[
                    {"role": "system", "content": "You are a medical history assistant."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            answer = response.choices[0].message.content
            asyncio.create_task(self.add_to_memory_async(query, answer, patient_id))
            return answer

        except ValueError as e:
            st.error(str(e))
            return f"Validation error: {str(e)}"
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."

    def generate_synthetic_data(self, patient_id):
        today = datetime.now()
        last_visit_date = (today - timedelta(days=30)).strftime("%B %d, %Y")
        next_appointment_date = (today + timedelta(days=30)).strftime("%B %d, %Y")

        prompt = f"""Generate a detailed patient profile and medical history for a patient with ID {patient_id}. Include:
        1. Patient name, age, and basic info
        2. Last visit date ({last_visit_date}) and purpose
        3. Next scheduled appointment ({next_appointment_date})
        4. List of ongoing medications and dosages
        5. Medical conditions diagnosed in the past year
        6. Any allergies and emergency contacts
        7. Brief summary of the patient's lifestyle and habits
        8. Any additional relevant information
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data generation AI that creates realistic patient profiles and medical histories."},
                {"role": "user", "content": prompt}
            ]
        )

        patient_data = response.choices[0].message.content
        print("Patient Data:", patient_data)  # Debugging line
        self.memory.add(patient_data, user_id=patient_id, metadata={"app_id": self.app_id, "role": "system"})

        return patient_data

# Module: Sidebar Management

async def manage_sidebar(agent, session_state):
    """Manage the sidebar and patient profile logic."""
        
    if 'patient_data' not in session_state:
        session_state.patient_data = None
        
    st.sidebar.title("Enter your Patient ID:")
    patient_id = st.sidebar.text_input("Enter your Patient ID (Format: PAT-XXXXX)")
    
    try:
        if patient_id:
            validated_id = agent.validate_patient_id(patient_id)
            if validated_id != patient_id:
                st.sidebar.error("Please use format PAT-XXXXX (e.g., PAT-12345)")
                return None
    except ValueError as e:
        st.sidebar.error(str(e))
        return None
    
    
    # Enable/Disable the 'View Patient Profile' button based on patient_id
    view_patient_profile_enabled = bool(patient_id)


    if st.sidebar.button("Generate Synthetic Data"):
        if patient_id:
            with st.spinner("Generating patient data..."):
                session_state.patient_data = agent.generate_synthetic_data(patient_id)
            st.sidebar.success("Synthetic data generated successfully!")
        else:
            st.sidebar.error("Please enter a patient ID first.")

      # Enable 'View Patient Profile' only if patient_id is provided
    view_patient_button = st.sidebar.button("View Patient Profile", disabled=not view_patient_profile_enabled)


    if view_patient_button:
        if session_state.patient_data:
            st.markdown("### Patient Profile:")
            st.markdown(session_state.patient_data)
            
        else:
            # Fetch data from memory if not in session_state
            print(f"Fetching data from memory for patient ID: {patient_id}")  # Debugging line
            relevant_memories = agent.memory.search(query="*", user_id=patient_id)  # Fetch all memories
            print(relevant_memories)
            # Check if there are results in the relevant_memories
            if relevant_memories and isinstance(relevant_memories, list):
                # Extract memory information from each item
                
                query = "Provide the Summary of patient profile"
                await get_model_output(agent, patient_id, session_state, query)
                
                
            else:
                st.sidebar.warning(f"Patient ID {patient_id} does not exist. Please check the ID or create a new one.")
        
    return patient_id


# Module: Chat Interface
async def chat_interface(agent, patient_id, session_state):
    if "messages" not in session_state:
        session_state.messages = []

    for message in session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("How can I assist you today?")

    await get_model_output(agent, patient_id, session_state, query)

async def get_model_output(agent, patient_id, session_state, query):
    if query and patient_id:
        session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        answer = await agent.handle_query(query, patient_id=patient_id)
        session_state.messages.append({"role": "assistant", "content": answer})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for char in answer:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                await asyncio.sleep(0.01)
            message_placeholder.markdown(full_response)
    elif not patient_id:
        st.error("Please enter a patient ID to start the chat.")

# Main Execution
if __name__ == "__main__":
    # First check if user is logged in
    if not st.session_state.logged_in:
        # If not logged in, only show the login form
        login()
    else:
        # If logged in, show the main application
        setup_app()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
            medical_agent = MedicalHistoryAgent()
            patient_id = asyncio.run(manage_sidebar(medical_agent, st.session_state))
            asyncio.run(chat_interface(medical_agent, patient_id, st.session_state))
        else:
            st.warning("Please set the OpenAI API key in your environment.")

    
