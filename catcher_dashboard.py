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
            --primary-light: #A52A2A;
            --secondary-color: #556B2F; /* Olive Green */
            --bg-color: #FDFBF7; /* Warm Paper */
            --text-color: #2C2C2C;
            --card-bg: #FFFFFF;
            --accent-blue: #4682B4;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 8px rgba(0,0,0,0.1);
            --shadow-lg: 0 8px 16px rgba(0,0,0,0.15);
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
            margin-bottom: 0.5em;
        }

        p, li, span, div {
            line-height: 1.6;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #F0EAD6;
            border-right: 1px solid #DCDCDC;
        }

        section[data-testid="stSidebar"] h2 {
            font-size: 1.5rem;
            margin-top: 1rem;
        }

        /* Cards */
        .card-container {
            background-color: var(--card-bg);
            padding: 24px;
            border-radius: 16px;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
            margin-bottom: 20px;
            text-align: center;
            border: 1px solid rgba(0,0,0,0.05);
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            position: relative;
            overflow: hidden;
        }

        .card-container:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(139, 0, 0, 0.2);
        }

        .card-container h3, .card-container h4 {
            margin-top: 10px;
            margin-bottom: 8px;
        }

        .avatar-img {
            border-radius: 50%;
            margin-bottom: 15px;
            border: 4px solid var(--bg-color);
            box-shadow: var(--shadow-md);
            width: 120px;
            height: 120px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .card-container:hover .avatar-img {
            transform: scale(1.05);
        }

        /* Utility Classes */
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.02em;
        }

        .hero-subtitle {
            font-size: 1.5rem;
            font-weight: 300;
            color: #555;
            margin-bottom: 30px;
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 30px;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(255,255,255,0.5);
        }

        /* Custom Badges */
        .badge {
            display: inline-block;
            padding: 0.5em 1em;
            font-size: 0.85em;
            font-weight: 600;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 50px;
            color: #fff;
            background-color: var(--secondary-color);
            margin: 4px;
            box-shadow: var(--shadow-sm);
            transition: transform 0.2s;
        }

        .badge:hover {
            transform: translateY(-2px);
        }

        .badge.theme {
            background-color: var(--accent-blue);
        }

        /* Quote Box */
        .quote-box {
            border-left: 4px solid var(--primary-color);
            background-color: #FFF;
            padding: 24px;
            font-style: italic;
            font-family: 'Merriweather', serif;
            font-size: 1.2em;
            line-height: 1.8;
            margin: 20px 0;
            border-radius: 0 12px 12px 0;
            box-shadow: var(--shadow-sm);
            color: #444;
        }

        .quote-box::before {
            content: "“";
            font-size: 3em;
            color: rgba(139, 0, 0, 0.1);
            position: absolute;
            margin-top: -30px;
            margin-left: -10px;
        }

        /* Navigation Buttons */
        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border: 1px solid transparent;
            background-color: white;
            color: var(--text-color);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }
        div.stButton > button:active {
            transform: translateY(0);
        }

        /* Mobile Optimizations */
        @media (max-width: 768px) {
            .hero-title { font-size: 2.2rem !important; }
            .hero-subtitle { font-size: 1.2rem !important; }

            .card-container {
                padding: 16px;
                margin-bottom: 12px;
            }

            .avatar-img {
                width: 90px;
                height: 90px;
            }

            /* Stack columns on mobile if not already handled by Streamlit */
            .mobile-stack {
                flex-direction: column !important;
            }

            .badge {
                padding: 0.3em 0.6em;
                font-size: 0.8em;
            }
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
    <div style='text-align: center; padding: 40px 0;'>
        <h1 class="hero-title">The Catcher in the Rye</h1>
        <h3 class="hero-subtitle">An Interactive Explorer into Holden's World</h3>
        <div style='width: 60px; height: 4px; background-color: var(--primary-color); margin: 0 auto 30px auto; border-radius: 2px;'></div>
    </div>
    """, unsafe_allow_html=True)

    # Introduction with more visual appeal
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("""
        <div class="glass-panel" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <p style='font-size: 1.3em; margin-bottom: 20px; font-family: Merriweather, serif;'>
                "If you really want to hear about it, the first thing you'll probably want to know is where I was born, and what my lousy childhood was like..."
            </p>
            <p style='font-size: 1.1em; color: #555;'>
                Dive into the complex mind of Holden Caulfield. Explore the characters who shaped his journey and the recurring themes that define J.D. Salinger's masterpiece.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Using a slightly different styling for the image container
        st.markdown("""
        <div style="border-radius: 12px; overflow: hidden; box-shadow: var(--shadow-md); height: 100%;">
            <img src="https://images.pexels.com/photos/1631677/pexels-photo-1631677.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                 style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Rye Field">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Start Your Journey</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
        <div class="card-container" style="align-items: flex-start; text-align: left; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎭</div>
            <h3>Characters</h3>
            <p>Unpack the psyche of Holden, Phoebe, Allie, and others. Discover their hidden motivations and relationships.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Characters", use_container_width=True):
            navigate_to("Characters")

    with col2:
        st.markdown("""
        <div class="card-container" style="align-items: flex-start; text-align: left; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📚</div>
            <h3>Themes</h3>
            <p>Analyze the core motifs: The pain of growing up, the search for identity, and the pervasive nature of phoniness.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Themes", use_container_width=True):
            navigate_to("Themes")

def show_characters_grid():
    st.markdown("<div style='text-align: center; margin-bottom: 40px;'><h1 class='hero-title' style='font-size: 2.5rem;'>Meet the Characters</h1><p class='hero-subtitle' style='font-size: 1.2rem;'>The voices of Pencey Prep and New York</p></div>", unsafe_allow_html=True)

    # Responsive Grid: 4 columns on desktop
    cols = st.columns(4)
    for i, char in enumerate(characters_data):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="card-container" style="justify-content: center; padding-top: 30px;">
                <img src="{char['image_url']}" class="avatar-img" alt="{char['name']}">
                <h4 style="margin-top: 15px;">{char['name']}</h4>
                <p style="font-size: 0.8rem; color: #666; margin-top: 5px;">{char['traits'][0] if char['traits'] else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View Profile", key=f"btn_{char['name']}", use_container_width=True):
                select_char(char)

def show_character_detail(char):
    if st.button("← Back to Characters", key="back_char"):
        navigate_to("Characters")

    # Enhanced Header with Glassmorphism
    st.markdown(f"""
    <div class="glass-panel" style="display: flex; align-items: center; margin-bottom: 30px; flex-wrap: wrap;">
        <img src="{char['image_url']}" style='border-radius: 50%; width: 150px; height: 150px; margin-right: 30px; border: 5px solid white; box-shadow: var(--shadow-md); object-fit: cover;'>
        <div style="flex: 1; min-width: 250px;">
            <h1 style='margin: 0; font-size: 3rem;'>{char['name']}</h1>
            <p style='font-style: italic; font-size: 1.2em; color: #555; margin-top: 10px; border-left: 3px solid var(--primary-color); padding-left: 15px;'>{char['significance']}</p>
            <div style="margin-top: 15px;">
                {' '.join([f"<span class='badge'>{t}</span>" for t in char['traits']])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Content in Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🤝 Relationships", "💬 Quotes", "🎨 Themes"])

    with tab1:
        st.markdown("### First Appearance")
        st.markdown(f"""
        <div style='background-color: #fff; padding: 25px; border-radius: 12px; border-left: 5px solid var(--secondary-color); box-shadow: var(--shadow-sm); font-size: 1.1em;'>
            {char['first_appearance_context']}
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Connections")
        if char['relationships']:
            for name, desc in char['relationships'].items():
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: var(--shadow-sm);">
                    <strong style="color: var(--primary-color); font-size: 1.1em;">{name}</strong>
                    <p style="margin-top: 5px; color: #444;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific relationships noted.")

    with tab3:
        st.markdown("### Memorable Quotes")
        if char['quotes']:
            for q in char['quotes']:
                st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with tab4:
        st.markdown("### Thematic Resonance")
        if char['associated_themes']:
            st.markdown(" ".join([f"<span class='badge theme' style='font-size: 1em; padding: 10px 15px;'>{t}</span>" for t in char['associated_themes']]), unsafe_allow_html=True)
        else:
            st.info("No themes associated.")

def show_themes_grid():
    st.markdown("<div style='text-align: center; margin-bottom: 40px;'><h1 class='hero-title' style='font-size: 2.5rem;'>Literary Themes</h1><p class='hero-subtitle' style='font-size: 1.2rem;'>The Deeper Meanings</p></div>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, theme in enumerate(themes_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card-container" style="justify-content: flex-start; text-align: left; padding: 30px;">
                <h3 style='margin-bottom: 15px; color: var(--primary-color); border-bottom: 2px solid #EEE; padding-bottom: 10px; width: 100%;'>{theme['name']}</h3>
                <p style='font-size: 0.95em; color: #555; line-height: 1.6;'>{theme['description'][:140]}...</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Theme", key=f"btn_{theme['name']}", use_container_width=True):
                select_theme(theme)

def show_theme_detail(theme):
    if st.button("← Back to Themes", key="back_theme"):
        navigate_to("Themes")

    # Header
    st.markdown(f"""
    <div class="glass-panel" style="margin-bottom: 30px; border-left: 6px solid var(--primary-color);">
        <h1 class='hero-title' style='margin-bottom: 20px; font-size: 3.5rem;'>{theme['name']}</h1>
        <p style='font-size: 1.3em; line-height: 1.8; color: #444; font-family: Lato, sans-serif;'>{theme['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("<h3 style='margin-bottom: 20px;'>Illustrative Quotes</h3>", unsafe_allow_html=True)
        if theme['related_quotes']:
            for q in theme['related_quotes']:
                st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with c2:
        st.markdown("<h3 style='margin-bottom: 20px;'>Key Characters</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: var(--shadow-sm);">
            <p style="margin-bottom: 15px; color: #666;">These characters embody or grapple with the theme of <strong>{}</strong>:</p>
            {}
        </div>
        """.format(theme['name'], " ".join([f"<span class='badge' style='font-size: 1.1em; padding: 10px 15px; margin: 5px;'>{char}</span>" for char in theme['characters_associated']])), unsafe_allow_html=True)

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
