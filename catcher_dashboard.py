import streamlit as st
from characters import characters_data # Assuming characters.py is in the same directory

# Page configuration
# This should be the first Streamlit command in your script, and it can only be set once.
st.set_page_config(
    page_title="Catcher Character Explorer", # Sets the title of the browser tab
    page_icon="📖", # Sets the favicon of the browser tab (can be an emoji or URL)
    layout="wide" # Uses the full width of the page
)

def display_character_info(character):
    """
    Displays the detailed information for the selected character in the main area of the dashboard.
    Args:
        character (dict): A dictionary containing the data for a single character.
    """
    st.header(character["name"]) # Character's name as a main header

    # Display Significance
    st.subheader("Significance")
    st.markdown(character["significance"]) # Using markdown for potentially rich text

    # Display Key Traits
    st.subheader("Key Traits")
    for trait in character["traits"]:
        st.markdown(f"- {trait}") # Display as a bulleted list

    # Display Relationships
    st.subheader("Relationships")
    if character["relationships"]:
        for name, description in character["relationships"].items():
            st.markdown(f"**{name}:** {description}") # Bold name, then description
    else:
        st.markdown("No specific relationships noted.")

    # Display Memorable Quotes
    st.subheader("Memorable Quotes")
    if character["quotes"]:
        for quote in character["quotes"]:
            st.info(f'"{quote}"') # Using st.info for a visually distinct quote block
    else:
        st.markdown("No specific quotes noted for this character.")

    # Display First Appearance Context
    st.subheader("First Appearance Context")
    st.markdown(character["first_appearance_context"])

# --- Main Dashboard App ---

# Set the main title of the dashboard
st.title("The Catcher in the Rye: Character Explorer")

# Introductory text for the dashboard
st.markdown("""
Welcome to the Character Explorer for J.D. Salinger's classic novel, *The Catcher in the Rye*.
Select a character from the dropdown menu to learn more about their significance, traits, relationships, and notable quotes.
This tool helps in understanding the key figures and their roles within the story.
""")

# Data Preparation: Create a list of character names for the selectbox
# This makes it easy to populate the dropdown and refer back to the main data list.
character_names = [char["name"] for char in characters_data]

# Sidebar for character selection
st.sidebar.header("Select a Character") # Header for the sidebar section
selected_character_name = st.sidebar.selectbox(
    "Choose a character:", # Label for the selectbox
    options=character_names, # List of options to choose from
    index=0 # Default to the first character in the list (Holden Caulfield)
)

# Data Retrieval: Find the selected character's data from the characters_data list
selected_character_data = None # Initialize as None
for char_data in characters_data:
    if char_data["name"] == selected_character_name:
        selected_character_data = char_data
        break # Exit loop once character is found

# Display Logic: Show the selected character's information or an error if not found
if selected_character_data:
    display_character_info(selected_character_data) # Call function to display data
else:
    # This error should ideally not be reached if character_names is derived from characters_data
    st.error("Character data not found. Please check the data source (`characters.py`).")

# Sidebar Footer Information
st.sidebar.markdown("---") # Visual separator
st.sidebar.info(
    "This dashboard provides information based on common interpretations and summaries of the novel. "
    "The data is primarily sourced from `characters.py`."
)
```
