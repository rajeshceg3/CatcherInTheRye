import streamlit as st
from characters import characters_data
from themes import themes_data

# --- Page Config ---
st.set_page_config(
    page_title="Catcher in the Rye Explorer",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with more screen real estate
)

# --- State Management Helper ---
def rerun():
    """Helper to handle reruns across Streamlit versions."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# --- CSS Injection ---
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Lato:wght@300;400;700&display=swap');

        /* Global Vars */
        :root {
            --primary-color: #8B0000; /* Deep Red */
            --secondary-color: #556B2F; /* Olive Green */
            --bg-color: #FDFBF7; /* Warm Paper */
            --text-color: #2C2C2C;
            --card-bg: #FFFFFF;
            --accent-blue: #4682B4;
        }

        /* General Body */
        .stApp {
            background-color: var(--bg-color);
            font-family: 'Lato', sans-serif;
            color: var(--text-color);
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Merriweather', serif;
            color: var(--primary-color) !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #F0EAD6;
            border-right: 1px solid #DCDCDC;
        }

        /* Cards */
        .card-container {
            background-color: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            margin-bottom: 15px;
            text-align: center;
            border: 1px solid #EEE;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .card-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.1);
            border-color: var(--primary-color);
        }

        .avatar-img {
            border-radius: 50%;
            margin-bottom: 15px;
            border: 3px solid var(--bg-color);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            width: 100px;
            height: 100px;
            object-fit: cover;
        }

        /* Custom Badges */
        .badge {
            display: inline-block;
            padding: 0.4em 0.8em;
            font-size: 0.85em;
            font-weight: 600;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 20px;
            color: #fff;
            background-color: var(--secondary-color);
            margin: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .badge.theme {
            background-color: var(--accent-blue);
        }

        /* Quote Box */
        .quote-box {
            border-left: 5px solid var(--primary-color);
            background-color: #FFF;
            padding: 20px;
            font-style: italic;
            font-family: 'Merriweather', serif;
            font-size: 1.1em;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Navigation Buttons */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }
        div.stButton > button:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        /* Mobile Optimizations */
        @media (max-width: 600px) {
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.5rem !important; }
            .card-container { padding: 15px; }
            .avatar-img { width: 80px; height: 80px; }
        }

    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'selected_char' not in st.session_state:
    st.session_state.selected_char = None
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = None

def navigate_to(page):
    st.session_state.page = page
    rerun()

def select_char(char):
    st.session_state.selected_char = char
    st.session_state.page = 'Character Detail'
    rerun()

def select_theme(theme):
    st.session_state.selected_theme = theme
    st.session_state.page = 'Theme Detail'
    rerun()

# --- Views ---

def show_home():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <h1 style='font-size: 3.5em; margin-bottom: 10px;'>The Catcher in the Rye</h1>
        <h3 style='color: #555 !important; font-weight: 300;'>An Interactive Explorer</h3>
        <hr style='width: 50%; margin: 20px auto; border-color: #8B0000;'>
    </div>
    """, unsafe_allow_html=True)

    # Introduction
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        <div style='background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
            <p style='font-size: 1.2em; line-height: 1.8;'>
                Welcome to Holden Caulfield's world. This interactive dashboard allows you to explore the complex characters
                and enduring themes of J.D. Salinger's masterpiece.
                <br><br>
                Use the navigation to dive into detailed profiles, uncover hidden connections, and reflect on the
                struggles of innocence and growing up.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.image("https://images.pexels.com/photos/1631677/pexels-photo-1631677.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", use_container_width=True, caption="The Rye Field")

    st.markdown("### Quick Access")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card-container" style="align-items: flex-start; text-align: left;">
            <h3>🎭 Characters</h3>
            <p>Meet Holden, Phoebe, Allie, and the rest. Discover their traits, relationships, and significance.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Characters", use_container_width=True):
            navigate_to("Characters")

    with col2:
        st.markdown("""
        <div class="card-container" style="align-items: flex-start; text-align: left;">
            <h3>📚 Themes</h3>
            <p>Analyze the core motifs: Phoniness, Alienation, Innocence, and the Fear of Change.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Themes", use_container_width=True):
            navigate_to("Themes")

def show_characters_grid():
    st.markdown("<h1 style='text-align: center;'>Meet the Characters</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Select a character to view their full profile.</p>", unsafe_allow_html=True)

    # Responsive Grid: 4 columns on desktop
    cols = st.columns(4)
    for i, char in enumerate(characters_data):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="card-container">
                <img src="{char['image_url']}" class="avatar-img" alt="{char['name']}">
                <h4>{char['name']}</h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View Profile", key=f"btn_{char['name']}", use_container_width=True):
                select_char(char)

def show_character_detail(char):
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Back"):
            navigate_to("Characters")

    st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <img src="{char['image_url']}" style='border-radius: 50%; width: 120px; height: 120px; margin-right: 20px; border: 4px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <div>
            <h1 style='margin: 0;'>{char['name']}</h1>
            <p style='font-style: italic; font-size: 1.1em; color: #666;'>{char['significance']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Traits
    st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in char['traits']]), unsafe_allow_html=True)

    st.divider()

    # Detailed Content in Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🤝 Relationships", "💬 Quotes", "🎨 Themes"])

    with tab1:
        st.subheader("First Appearance")
        st.markdown(f"""
        <div style='background-color: #fff; padding: 20px; border-radius: 8px; border-left: 4px solid #556B2F;'>
            {char['first_appearance_context']}
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        if char['relationships']:
            for name, desc in char['relationships'].items():
                with st.expander(f"**{name}**"):
                    st.write(desc)
        else:
            st.info("No specific relationships noted.")

    with tab3:
        if char['quotes']:
            for q in char['quotes']:
                st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with tab4:
        if char['associated_themes']:
            st.markdown(" ".join([f"<span class='badge theme'>{t}</span>" for t in char['associated_themes']]), unsafe_allow_html=True)
        else:
            st.info("No themes associated.")

def show_themes_grid():
    st.markdown("<h1 style='text-align: center;'>Literary Themes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Explore the deeper meanings behind the story.</p>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, theme in enumerate(themes_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card-container">
                <h3 style='margin-bottom: 10px;'>{theme['name']}</h3>
                <p style='font-size: 0.9em; color: #555;'>{theme['description'][:120]}...</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Theme", key=f"btn_{theme['name']}", use_container_width=True):
                select_theme(theme)

def show_theme_detail(theme):
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Back"):
            navigate_to("Themes")

    st.title(theme['name'])
    st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 8px; font-size: 1.1em; line-height: 1.6;'>{theme['description']}</div>", unsafe_allow_html=True)

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💬 Illustrative Quotes")
        for q in theme['related_quotes']:
            st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)

    with c2:
        st.subheader("👥 Associated Characters")
        st.markdown(" ".join([f"<span class='badge'>{char}</span>" for char in theme['characters_associated']]), unsafe_allow_html=True)

# --- Main Application Execution ---

local_css()

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    if st.button("🏠 Home", use_container_width=True):
        navigate_to("Home")
    if st.button("🎭 Character Explorer", use_container_width=True):
        navigate_to("Characters")
    if st.button("📚 Theme Explorer", use_container_width=True):
        navigate_to("Themes")

    st.divider()
    st.caption("The Catcher in the Rye Explorer")
    st.caption("v2.0 • Ultrathink UX")

# Routing Logic
if st.session_state.page == 'Home':
    show_home()
elif st.session_state.page == 'Characters':
    show_characters_grid()
elif st.session_state.page == 'Character Detail':
    if st.session_state.selected_char:
        show_character_detail(st.session_state.selected_char)
    else:
        navigate_to("Characters")
elif st.session_state.page == 'Themes':
    show_themes_grid()
elif st.session_state.page == 'Theme Detail':
    if st.session_state.selected_theme:
        show_theme_detail(st.session_state.selected_theme)
    else:
        navigate_to("Themes")
