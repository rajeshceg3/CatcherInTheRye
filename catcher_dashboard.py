import streamlit as st
from characters import characters_data # Assuming characters.py is in the same directory

# Page configuration
# This should be the first Streamlit command in your script, and it can only be set once.
st.set_page_config(
    page_title="Catcher Character Explorer",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_character_info(character):
    """
    Displays the detailed information for the selected character in the main area of the dashboard.
    Args:
        character (dict): A dictionary containing the data for a single character.
    """
    st.header(character["name"]) # Character's name as a main header
    st.divider()

    # Display Significance
    st.subheader("🌟 Significance")
    st.markdown(character["significance"])
    st.divider()

    # Display Key Traits
    st.subheader("✨ Key Traits")
    if character["traits"]:
        # For a more "tag-like" feel with markdown, we can try this:
        # traits_md = " ".join([f"**`{trait}`**" for trait in character["traits"]])
        # Or a slightly simpler bold list:
        # traits_md = ""
        # for trait in character["traits"]:
        #    traits_md += f"- **{trait}**\n"
        # Let's go with the simpler bold list for now for broader compatibility and readability.
        st.markdown("""<style>
                       .trait-badge {
                           background-color: #f0f2f6;
                           border-radius: 5px;
                           padding: 0.2em 0.6em;
                           margin: 0.2em 0.3em;
                           display: inline-block;
                           font-weight: normal;
                           border: 1px solid #e0e0e0;
                       }
                       </style>""", unsafe_allow_html=True)
        traits_html = "".join([f'<span class="trait-badge">{trait}</span>' for trait in character["traits"]])
        st.markdown(traits_html, unsafe_allow_html=True)
    else:
        st.markdown("No specific traits noted.")
    st.divider()

    # Display Relationships
    st.subheader("🤝 Relationships")
    if character["relationships"]:
        for name, description in character["relationships"].items():
            with st.expander(f"**{name}**"): # Use expander for each relationship
                st.markdown(description)
    else:
        st.markdown("No specific relationships noted.")
    st.divider()

    # Display Memorable Quotes
    st.subheader("💬 Memorable Quotes")
    if character["quotes"]:
        st.markdown("""<style>
                       .custom-quote {
                           border-left: 5px solid #007bff; /* Blue left border */
                           background-color: #f9f9f9; /* Light grey background */
                           padding: 10px 20px;
                           margin: 10px 0px;
                           font-style: italic;
                           color: #333;
                       }
                       .custom-quote p {
                           margin: 0;
                       }
                       </style>""", unsafe_allow_html=True)
        for i, quote in enumerate(character["quotes"]):
            # Using a more robust way to ensure paragraph styling within the quote
            st.markdown(f'<div class="custom-quote"><p>"{quote}"</p></div>', unsafe_allow_html=True)
            # Removed the <br> as margins on .custom-quote should handle spacing
    else:
        st.markdown("No specific quotes noted for this character.")
    st.divider()

    # Display First Appearance Context
    st.subheader("🗺️ First Appearance Context")
    st.markdown(character["first_appearance_context"])
    # No divider after the last section typically

# --- Main Dashboard App ---

# Set the main title of the dashboard
st.title("The Catcher in the Rye: Character Explorer")

# Introductory text for the dashboard
intro_col1, intro_col2 = st.columns([3, 1]) # Give more space to text

with intro_col1:
    st.markdown("""
    ## Welcome to Holden's World!

    Dive deep into J.D. Salinger's classic novel, *The Catcher in the Rye*, with this interactive Character Explorer.
    Select a character from the sidebar to uncover their significance, unique traits, complex relationships, and memorable quotes.
    This tool is designed to help you connect with the characters and understand their pivotal roles within this iconic story. Let the exploration begin!
    """)

with intro_col2:
    st.markdown("") # Placeholder for potential image or extra info
    st.markdown(
        """
        *"I'm the most terrific liar you ever saw in your life."*


- Holden Caulfield
        """
    )
    st.caption("Explore the characters to find more truths (or lies!).")

# Data Preparation: Create a list of character names for the selectbox
# This makes it easy to populate the dropdown and refer back to the main data list.
character_names = [char["name"] for char in characters_data]

# Sidebar for character selection
st.sidebar.header("Meet the Characters 🎭") # Header for the sidebar section
st.sidebar.markdown("Choose a name from the list below to see their story unfold.")
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

# Ensure this is outside the display_character_info function, at the end of the script's main flow.

st.divider() # Visual separator before the footer
st.caption("Holden Caulfield's journey, character by character. An exploration of *The Catcher in the Rye*. Inspired by J.D. Salinger's timeless novel.")
# Alternatively, a more direct footer:
# st.caption("Character Explorer for The Catcher in the Rye | Built with Streamlit")
# Let's go with the more thematic one.

# Sidebar Footer Information
st.sidebar.divider() # Using st.divider() if available and preferred over markdown "---"
st.sidebar.caption("Dive into the world of *The Catcher in the Rye*. Data from `characters.py`.")
# Changed to st.caption for a slightly different style, can revert to st.info if caption is too small.
# Using st.divider() for a modern look. If it causes issues (e.g. older streamlit version), revert to st.sidebar.markdown("---")
```
