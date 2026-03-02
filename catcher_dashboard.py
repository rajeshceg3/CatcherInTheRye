import streamlit as st
import graphviz
from characters import characters_data
from themes import themes_data
from tour import TourManager

# --- Page Config ---
st.set_page_config(
    page_title="Catcher in the Rye Explorer",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with more screen real estate
)

import random

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
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&family=Lato:wght@300;400;700;900&display=swap');

        :root {
            /* --- Ultrathink Palette --- */
            --primary-color: #8B0000;       /* Deep Red */
            --primary-light: #A52A2A;
            --primary-dark: #600000;
            --secondary-color: #556B2F;     /* Olive Green */
            --accent-gold: #D4AF37;         /* Classic Gold */
            --accent-blue: #4682B4;         /* Steel Blue */

            --bg-paper: #FDFBF7;            /* Warm Paper */
            --surface-white: #FFFFFF;
            --surface-glass: rgba(255, 255, 255, 0.75);

            --text-main: #1A1A1A;           /* Near Black */
            --text-muted: #555555;
            --text-light: #888888;

            /* --- Spacing System --- */
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 32px;
            --space-xl: 64px;

            /* --- Radius --- */
            --radius-sm: 8px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --radius-pill: 999px;

            /* --- Shadows (Layered for Depth) --- */
            --shadow-subtle: 0 2px 4px rgba(0, 0, 0, 0.03);
            --shadow-card: 0 4px 12px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-float: 0 12px 24px rgba(139, 0, 0, 0.08), 0 4px 8px rgba(0, 0, 0, 0.04);
            --shadow-inner: inset 0 2px 4px rgba(0,0,0,0.02);

            /* --- Transitions --- */
            --ease-out-quart: cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        /* --- Global Reset & Base --- */
        .stApp {
            background-color: var(--bg-paper);
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
            font-family: 'Lato', sans-serif;
            color: var(--text-main);
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Merriweather', serif;
            color: var(--primary-color) !important;
            margin-bottom: var(--space-md);
            line-height: 1.25;
        }

        h1 { font-weight: 900 !important; letter-spacing: -0.03em; font-size: clamp(2.2rem, 5vw, 3.5rem) !important; }
        h2 { font-weight: 700 !important; letter-spacing: -0.01em; font-size: clamp(1.75rem, 4vw, 2.5rem) !important; }
        h3 { font-size: clamp(1.35rem, 3vw, 1.75rem) !important; }

        p {
            line-height: 1.7;
            margin-bottom: var(--space-md);
        }

        /* --- Components --- */

        /* Card Container */
        .card-container {
            background: var(--surface-white);
            border-radius: var(--radius-md);
            padding: var(--space-lg);
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(139, 0, 0, 0.05);
            transition: all 0.4s var(--ease-out-quart);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        /* Glass Panel */
        .glass-panel {
            background: var(--surface-glass);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        /* Avatars */
        .avatar-img {
            border-radius: 50%;
            border: 4px solid #fff;
            box-shadow: var(--shadow-card);
            transition: transform 0.5s var(--ease-out-quart);
            object-fit: cover;
        }

        /* Badges/Tags */
        .badge {
            background-color: var(--secondary-color);
            color: white;
            padding: 0.35em 0.85em;
            border-radius: var(--radius-pill);
            font-size: 0.8em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: var(--shadow-subtle);
            display: inline-block;
            margin: 2px;
            transition: transform 0.2s ease;
        }
        .badge.theme { background-color: var(--accent-blue); }

        /* Quote Box */
        .quote-box {
            position: relative;
            background: var(--surface-white);
            padding: 2rem;
            padding-left: 3.5rem;
            border-radius: var(--radius-sm);
            box-shadow: var(--shadow-subtle);
            font-family: 'Merriweather', serif;
            font-style: italic;
            color: var(--text-muted);
            border-left: 4px solid var(--primary-color);
            margin: 1.5rem 0;
            transition: all 0.3s var(--ease-out-quart);
        }
        .quote-box::before {
            content: "“";
            font-size: 5rem;
            color: rgba(139, 0, 0, 0.08);
            position: absolute;
            top: -10px;
            left: 10px;
            font-family: serif;
        }

        /* Streamlit Button Overrides */
        div.stButton > button {
            border: 1px solid rgba(139,0,0,0.1);
            background: white;
            color: var(--text-main);
            box-shadow: var(--shadow-subtle);
            border-radius: var(--radius-md);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-family: 'Lato', sans-serif;
            transition: all 0.3s var(--ease-out-quart);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #F8F4E6;
            border-right: 1px solid rgba(139,0,0,0.05);
        }

        /* Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translate3d(0, 30px, 0); }
            to { opacity: 1; transform: translate3d(0, 0, 0); }
        }
        .animate-enter {
            animation: fadeInUp 0.8s var(--ease-out-quart) forwards;
            opacity: 0; /* Start hidden */
        }

        /* --- MOBILE HYPER-OPTIMIZATION (< 768px) --- */
        @media (max-width: 768px) {
            h1 { margin-bottom: 1rem; }

            /* Spacing */
            .stApp { padding-top: 0.5rem; }
            .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }

            /* Components */
            .card-container {
                padding: 1.25rem;
                margin-bottom: 1rem;
                border-radius: var(--radius-md);
                box-shadow: var(--shadow-subtle); /* Flatter on mobile for performance/cleanliness */
            }

            .glass-panel {
                padding: 1.25rem;
                backdrop-filter: blur(12px); /* Slightly less blur for perf */
            }

            /* Touch Targets */
            div.stButton > button {
                width: 100%;
                min-height: 52px; /* Large safe touch target */
                font-size: 1rem;
                margin-bottom: 0.5rem;
            }

            /* Avatars */
            .avatar-img {
                width: 100px;
                height: 100px;
                margin-bottom: 10px;
            }

            /* Navigation/Layout */
            /* Force single column behavior where needed via CSS if logic doesn't catch it */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
                min-width: 100% !important;
            }
        }

        /* --- DESKTOP HYPER-OPTIMIZATION (> 1024px) --- */
        @media (min-width: 1024px) {
            /* Max width for readability */
            .block-container {
                max-width: 1000px;
                padding-top: 4rem;
                padding-bottom: 5rem;
            }

            /* Hover Effects - Only on desktop */
            .card-container:hover {
                transform: translateY(-8px) scale(1.01);
                box-shadow: var(--shadow-float);
                border-color: rgba(139, 0, 0, 0.2);
            }

            .avatar-img:hover {
                transform: scale(1.1) rotate(2deg);
                box-shadow: var(--shadow-float);
            }

            div.stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-card);
                color: var(--primary-color);
                border-color: var(--primary-color);
                background-color: #FFFAFA;
            }

            .quote-box:hover {
                transform: translateX(8px);
                border-left-color: var(--accent-gold);
                color: var(--text-main);
                box-shadow: var(--shadow-card);
            }

            .badge:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-card);
                cursor: default;
            }
        }

        /* --- TOUR COMPONENT STYLES --- */

        /* The container targeting strategy: Find the vertical block containing our marker */
        div[data-testid="stVerticalBlock"]:has(.tour-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.tour-marker) > div[data-testid="stVerticalBlock"] {
            position: fixed !important;
            bottom: 3rem;
            right: 3rem;
            width: 420px;
            z-index: 999999;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border-radius: var(--radius-lg);
            padding: 2rem;
            box-shadow: 0 24px 48px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.8) inset;
            border: 1px solid rgba(139, 0, 0, 0.1);
            animation: slideInUp 0.6s cubic-bezier(0.19, 1, 0.22, 1) forwards;
        }

        /* Mobile Tour Card */
        @media (max-width: 768px) {
            div[data-testid="stVerticalBlock"]:has(.tour-marker),
            div[data-testid="stVerticalBlockBorderWrapper"]:has(.tour-marker) > div[data-testid="stVerticalBlock"] {
                bottom: 0;
                left: 0;
                right: 0;
                width: 100%;
                border-radius: 24px 24px 0 0;
                padding: 1.5rem;
                padding-bottom: 2rem; /* Safe area */
                animation: slideInUpMobile 0.5s cubic-bezier(0.19, 1, 0.22, 1) forwards;
            }
        }

        @keyframes slideInUp {
            from { opacity: 0; transform: translate3d(0, 40px, 0) scale(0.95); }
            to { opacity: 1; transform: translate3d(0, 0, 0) scale(1); }
        }

        @keyframes slideInUpMobile {
            from { opacity: 0; transform: translate3d(0, 100%, 0); }
            to { opacity: 1; transform: translate3d(0, 0, 0); }
        }

    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
    st.session_state.home_visited = False
if 'selected_char' not in st.session_state:
    st.session_state.selected_char = None
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = None
if 'network_visited' not in st.session_state:
    st.session_state.network_visited = False

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
    if not st.session_state.get('home_visited'):
        st.toast("Welcome to the Catcher in the Rye Explorer! 🧭", icon="👋")
        st.session_state.home_visited = True

    # Hero Section
    st.markdown("""
    <div class="animate-enter" style='text-align: center; padding: 6vh 0 4vh 0;'>
        <h1>The Catcher in the Rye</h1>
        <p style="font-size: 1.25rem; color: var(--text-muted); font-weight: 300; max-width: 600px; margin: 0 auto;">
            An interactive exploration into the mind of Holden Caulfield and the world he rejects.
        </p>
        <div style='width: 60px; height: 4px; background-color: var(--primary-color); margin: 2rem auto; border-radius: 4px; opacity: 0.6;'></div>
    </div>
    """, unsafe_allow_html=True)

    # Featured Content
    c1, c2 = st.columns([1.2, 0.8], gap="large")

    with c1:
        st.markdown("""
        <div class="glass-panel animate-enter" style="height: 100%; display: flex; flex-direction: column; justify-content: center; animation-delay: 0.1s;">
            <p style='font-size: 1.5em; margin-bottom: 2rem; font-family: Merriweather, serif; font-style: italic; color: var(--primary-color);'>
                "If you really want to hear about it..."
            </p>
            <p style='font-size: 1.1em; color: var(--text-main); margin-bottom: 1.5rem;'>
                J.D. Salinger’s masterpiece is more than just a story of teenage angst. It’s a profound look at grief, innocence, and the struggle to find authenticity in a "phony" world.
            </p>
            <p style='font-size: 1em; color: var(--text-muted);'>
                Use this dashboard to dissect the complex relationships and recurring motifs that define Holden's journey.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Decorative Image with polished styling
        st.markdown("""
        <div class="animate-enter" style="border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-float); height: 100%; min-height: 300px; animation-delay: 0.2s; position: relative;">
            <div style="position: absolute; inset: 0; background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.2)); z-index: 1;"></div>
            <img src="https://images.pexels.com/photos/1631677/pexels-photo-1631677.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                 style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Rye Field">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)

    # Navigation Cards
    st.markdown("<h3 class='animate-enter' style='text-align: center; margin-bottom: 3rem; animation-delay: 0.3s;'>Begin Exploration</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
        <div class="card-container animate-enter" style="animation-delay: 0.4s;">
            <div style="font-size: 3rem; margin-bottom: 1.5rem; background: var(--bg-paper); width: fit-content; padding: 10px; border-radius: 50%;">🎭</div>
            <h2 style="font-size: 1.8rem !important;">Characters</h2>
            <p>Meet the cast of Pencey Prep and New York. Discover the people who confuse, anger, and occasionally comfort Holden.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Characters", use_container_width=True):
            navigate_to("Characters")

    with col2:
        st.markdown("""
        <div class="card-container animate-enter" style="animation-delay: 0.5s;">
            <div style="font-size: 3rem; margin-bottom: 1.5rem; background: var(--bg-paper); width: fit-content; padding: 10px; border-radius: 50%;">📚</div>
            <h2 style="font-size: 1.8rem !important;">Themes</h2>
            <p>Analyze the deeper meanings: The preservation of innocence, the pain of growing up, and the isolation of the individual.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Themes", use_container_width=True):
            navigate_to("Themes")

def show_characters_grid():
    st.markdown("""
    <div class="animate-enter" style='text-align: center; margin-bottom: 2rem; padding-top: 2rem;'>
        <h1>Meet the Characters</h1>
        <p style='font-size: 1.2rem; color: var(--text-muted);'>The voices of Pencey Prep and New York</p>
    </div>
    """, unsafe_allow_html=True)

    # Search Bar
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        search_query = st.text_input("🔍 Search characters by name or trait", "", help="Type to filter characters")

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    filtered_chars = []
    for char in characters_data:
        q = search_query.lower()
        if q in char['name'].lower() or any(q in t.lower() for t in char.get('traits', [])):
            filtered_chars.append(char)

    if not filtered_chars:
        st.info(f"No characters found matching '{search_query}'.")

    # Responsive Grid: 4 columns on desktop, auto-stack on mobile via CSS
    cols = st.columns(4)
    for i, char in enumerate(filtered_chars):
        with cols[i % 4]:
            delay = (i * 0.05) % 0.5
            # Card content
            st.markdown(f"""
            <div class="card-container animate-enter" style="align-items: center; text-align: center; padding-top: 3rem; animation-delay: {delay}s;">
                <img src="{char['image_url']}" class="avatar-img" alt="{char['name']}">
                <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.3rem !important;">{char['name']}</h3>
                <p style="font-size: 0.9rem; color: var(--text-light); line-height: 1.4; margin-bottom: 1.5rem;">{char['traits'][0] if char['traits'] else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            # Button (separated from markdown to function correctly)
            if st.button(f"View Profile", key=f"btn_{char['name']}", use_container_width=True):
                select_char(char)

def show_character_detail(char):
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Characters", key="back_char"):
        navigate_to("Characters")

    # Header
    st.markdown(f"""
    <div class="glass-panel animate-enter" style="display: flex; flex-wrap: wrap; align-items: center; gap: 3rem; margin-bottom: 3rem; margin-top: 1rem;">
        <img src="{char['image_url']}" class="avatar-img" style='width: 180px; height: 180px; margin: 0;'>
        <div style="flex: 1; min-width: 300px;">
            <h1 style='margin-bottom: 0.5rem;'>{char['name']}</h1>
            <p style='font-family: Merriweather, serif; font-style: italic; font-size: 1.15em; color: var(--text-muted); margin-bottom: 1.5rem; border-left: 4px solid var(--primary-color); padding-left: 20px;'>
                {char['significance']}
            </p>
            <div>
                {' '.join([f"<span class='badge'>{t}</span>" for t in char['traits']])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Content in Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🤝 Relationships", "💬 Quotes", "🎨 Themes"])

    with tab1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        c_left, c_right = st.columns([1, 1], gap="large")
        with c_left:
            st.markdown("### First Appearance")
            st.markdown(f"""
            <div class="card-container animate-enter" style="border-left: 6px solid var(--secondary-color); animation-delay: 0.1s;">
                <p style="font-size: 1.1rem;">{char['first_appearance_context']}</p>
            </div>
            """, unsafe_allow_html=True)

        with c_right:
            st.markdown("### Phoniness Meter")
            # Calculate Phoniness score dynamically
            score = 50
            themes = char.get('associated_themes', [])
            if "Phoniness" in themes:
                score += 30
            if "Innocence" in themes:
                score -= 30

            score = max(0, min(100, score))

            st.markdown(f"""
            <div class="card-container animate-enter" style="animation-delay: 0.2s; padding: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.5rem;">
                    <span style="font-weight: bold; font-size: 1.1rem; color: var(--text-main);">Phoniness Rating</span>
                    <span style="font-size: 1.5rem; font-weight: 900; color: var(--primary-color); font-family: 'Merriweather', serif;">{score}/100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(score, text="Score based on thematic associations")

    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("### Connections")
        if char['relationships']:
            for i, (name, desc) in enumerate(char['relationships'].items()):
                delay = (i * 0.05) % 0.5
                st.markdown(f"""
                <div class="card-container animate-enter" style="margin-bottom: 1rem; padding: 1.5rem; animation-delay: {delay}s; flex-direction: row; align-items: flex-start; gap: 1rem;">
                    <div style="flex: 1;">
                        <strong style="color: var(--primary-color); font-size: 1.1em; display: block; margin-bottom: 0.25rem;">{name}</strong>
                        <span style="color: var(--text-main); font-size: 0.95em;">{desc}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific relationships noted.")

    with tab3:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("### Memorable Quotes")
        if char['quotes']:
            for i, q in enumerate(char['quotes']):
                delay = (i * 0.1) % 0.5
                st.markdown(f"<div class='quote-box animate-enter' style='animation-delay: {delay}s;'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with tab4:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("### Thematic Resonance")
        if char['associated_themes']:
            st.markdown("""
            <div class="card-container animate-enter" style="animation-delay: 0.1s;">
                <p style="margin-bottom: 1rem;">Key themes associated with {}:</p>
                <div>
                    {}
                </div>
            </div>
            """.format(char['name'], " ".join([f"<span class='badge theme' style='font-size: 1rem; padding: 12px 20px; margin: 6px;'>{t}</span>" for t in char['associated_themes']])), unsafe_allow_html=True)
        else:
            st.info("No themes associated.")

def show_themes_grid():
    st.markdown("""
    <div class="animate-enter" style='text-align: center; margin-bottom: 4rem; padding-top: 2rem;'>
        <h1>Literary Themes</h1>
        <p style='font-size: 1.2rem; color: var(--text-muted);'>The deeper meanings behind the story</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, theme in enumerate(themes_data):
        with cols[i % 3]:
            delay = (i * 0.1) % 0.5
            st.markdown(f"""
            <div class="card-container animate-enter" style="justify-content: flex-start; text-align: left; padding: 2rem; animation-delay: {delay}s;">
                <h3 style='margin-bottom: 1rem; color: var(--primary-color); border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 1rem; width: 100%; font-size: 1.5rem !important;'>{theme['name']}</h3>
                <p style='font-size: 1rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 2rem;'>{theme['description'][:140]}...</p>
            </div>
            """, unsafe_allow_html=True)
            # Button (outside card container for proper click)
            if st.button(f"Explore Theme", key=f"btn_{theme['name']}", use_container_width=True):
                select_theme(theme)

def show_theme_detail(theme):
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Themes", key="back_theme"):
        navigate_to("Themes")

    # Header
    st.markdown(f"""
    <div class="glass-panel animate-enter" style="margin-bottom: 3rem; margin-top: 1rem; border-left: 6px solid var(--primary-color);">
        <h1 style='margin-bottom: 1rem;'>{theme['name']}</h1>
        <p style='font-size: 1.25em; line-height: 1.8; color: var(--text-main); font-weight: 300;'>{theme['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Content Grid
    c1, c2 = st.columns([1.2, 0.8], gap="large")
    with c1:
        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Illustrative Quotes</h3>", unsafe_allow_html=True)
        if theme['related_quotes']:
            for i, q in enumerate(theme['related_quotes']):
                delay = (i * 0.1) % 0.5
                st.markdown(f"<div class='quote-box animate-enter' style='animation-delay: {delay}s;'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with c2:
        st.markdown("<h3 style='margin-bottom: 1.5rem;'>Key Characters</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card-container animate-enter" style="animation-delay: 0.2s;">
            <p style="margin-bottom: 1.5rem; color: var(--text-muted); font-size: 1.05rem;">
                Characters who grapple with <strong>{}</strong>:
            </p>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                {}
            </div>
        </div>
        """.format(theme['name'], "".join([f"<span class='badge' style='font-size: 0.95em; padding: 8px 14px;'>{char}</span>" for char in theme['characters_associated']])), unsafe_allow_html=True)


def show_character_network():
    if not st.session_state.get('network_visited'):
        st.toast("Hover over character nodes and links to explore their relationships.", icon="🕸️")
        st.session_state.network_visited = True

    st.markdown("""
    <div class="animate-enter" style='text-align: center; margin-bottom: 4rem; padding-top: 2rem;'>
        <h1>Character Network</h1>
        <p style='font-size: 1.2rem; color: var(--text-muted);'>A visual map of connections in Holden's world</p>
    </div>
    """, unsafe_allow_html=True)

    graph = graphviz.Digraph(engine='neato')
    graph.attr(bgcolor='transparent')
    graph.attr('node', shape='circle', style='filled', fillcolor='#FDFBF7', color='#8B0000', fontname='Lato', fontcolor='#1A1A1A', penwidth='2')
    graph.attr('edge', color='#A52A2A', penwidth='1.5')

    # Add all nodes first
    for char in characters_data:
        tooltip_text = f"{char['name']}: {char['significance']}"
        graph.node(char['name'], tooltip=tooltip_text)

    # Add edges
    for char in characters_data:
        if 'relationships' in char:
            for rel_name, rel_desc in char['relationships'].items():
                # only add edge if rel_name is in our characters to avoid dangling nodes
                if any(c['name'] == rel_name for c in characters_data):
                    graph.edge(char['name'], rel_name, tooltip=rel_desc)

    st.markdown("""
    <div class="card-container animate-enter" style="align-items: center; justify-content: center; overflow: hidden; animation-delay: 0.1s;">
    """, unsafe_allow_html=True)
    st.graphviz_chart(graph, use_container_width=True)
    st.markdown("""
        <p style='margin-top: 1rem; color: var(--text-light); font-size: 0.9em; text-align: center;'>Arrows indicate a relationship or interaction originating from the character.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Application Execution ---

local_css()

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    if st.button("🏠 Home", use_container_width=True):
        navigate_to("Home")
    if st.button("🎭 Character Explorer", use_container_width=True):
        navigate_to("Characters")
    if st.button("🕸️ Character Network", use_container_width=True):
        navigate_to("Character Network")
    if st.button("📚 Theme Explorer", use_container_width=True):
        navigate_to("Themes")

    if st.button("🏳️ Start Guided Tour", use_container_width=True, type="primary"):
        TourManager.start_tour()

    st.divider()
    if st.button("🎲 Get a Random Quote", use_container_width=True):
        all_quotes = []
        for c in characters_data:
            for q in c.get('quotes', []):
                all_quotes.append((q, c['name']))
        if all_quotes:
            q, name = random.choice(all_quotes)
            st.toast(f"**{name}**: *\"{q}\"*", icon="💬")

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
elif st.session_state.page == 'Character Network':
    show_character_network()
elif st.session_state.page == 'Themes':
    show_themes_grid()
elif st.session_state.page == 'Theme Detail':
    if st.session_state.selected_theme:
        show_theme_detail(st.session_state.selected_theme)
    else:
        navigate_to("Themes")

# --- Guided Tour Overlay ---
TourManager.render_tour()
