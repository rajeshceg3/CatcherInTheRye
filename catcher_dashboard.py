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
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&family=Lato:wght@300;400;700;900&display=swap');

        :root {
            /* Color Palette - Refined */
            --primary-color: #8B0000;
            --primary-dark: #600000;
            --secondary-color: #556B2F;
            --accent-blue: #4682B4;
            --bg-paper: #FDFBF7;
            --text-main: #2C2C2C;
            --text-muted: #555555;
            --card-bg: #FFFFFF;

            /* Shadows */
            --shadow-sm: 0 2px 4px rgba(44, 44, 44, 0.05);
            --shadow-md: 0 8px 16px rgba(44, 44, 44, 0.08);
            --shadow-lg: 0 16px 32px rgba(44, 44, 44, 0.12);

            /* Spacing */
            --radius-sm: 8px;
            --radius-md: 16px;
        }

        /* Base Styles */
        .stApp {
            background-color: var(--bg-paper);
            /* Subtle noise texture for paper feel */
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
            font-family: 'Lato', sans-serif;
            color: var(--text-main);
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Merriweather', serif;
            color: var(--primary-color) !important;
            margin-bottom: 0.75rem;
            line-height: 1.3;
        }

        h1 { font-size: clamp(2rem, 5vw, 3.5rem) !important; font-weight: 900 !important; letter-spacing: -0.02em; }
        h2 { font-size: clamp(1.5rem, 4vw, 2.5rem) !important; font-weight: 700 !important; }
        h3 { font-size: clamp(1.2rem, 3vw, 1.8rem) !important; }

        p, li, span, div {
            line-height: 1.7;
            color: var(--text-main);
        }

        /* Cards */
        .card-container {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            border: 1px solid rgba(139, 0, 0, 0.05);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }

        .card-container:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(139, 0, 0, 0.15);
        }

        /* Avatar styling */
        .avatar-img {
            border-radius: 50%;
            border: 4px solid #fff;
            box-shadow: var(--shadow-md);
            transition: transform 0.4s ease;
            width: 120px;
            height: 120px;
            object-fit: cover;
            margin-bottom: 15px;
        }

        .card-container:hover .avatar-img {
            transform: scale(1.08) rotate(3deg);
        }

        /* Glass Panel */
        .glass-panel {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border-radius: var(--radius-md);
            padding: 2.5rem;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        /* Buttons (Streamlit Overrides) */
        div.stButton > button {
            border: none;
            background: white;
            color: var(--text-main);
            box-shadow: var(--shadow-sm);
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }

        div.stButton > button:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
            color: var(--primary-color);
            border-color: rgba(139,0,0,0.1);
        }

        div.stButton > button:active {
            transform: translateY(0);
        }

        /* Badges */
        .badge {
            background-color: var(--secondary-color);
            color: white;
            padding: 0.4em 0.8em;
            border-radius: 50px;
            font-size: 0.85em;
            font-weight: 600;
            box-shadow: var(--shadow-sm);
            display: inline-block;
            margin: 3px;
            transition: all 0.2s;
        }

        .badge:hover { transform: translateY(-1px); box-shadow: var(--shadow-md); }
        .badge.theme { background-color: var(--accent-blue); }

        /* Quote Box */
        .quote-box {
            position: relative;
            background: #fff;
            padding: 2rem;
            padding-left: 3rem;
            border-radius: var(--radius-sm);
            box-shadow: var(--shadow-sm);
            font-family: 'Merriweather', serif;
            font-style: italic;
            color: var(--text-muted);
            border-left: 4px solid var(--primary-color);
            margin: 1.5rem 0;
        }

        .quote-box::before {
            content: "“";
            font-size: 4rem;
            color: rgba(139, 0, 0, 0.1);
            position: absolute;
            top: 0px;
            left: 10px;
        }

        /* Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #F8F4E6;
            border-right: 1px solid rgba(0,0,0,0.05);
        }

        /* Utility Classes */
        .hero-title {
            /* Now handled by general h1 */
        }

        .hero-subtitle {
            font-size: 1.5rem;
            font-weight: 300;
            color: #555;
            margin-bottom: 30px;
        }

        /* Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translate3d(0, 20px, 0); }
            to { opacity: 1; transform: translate3d(0, 0, 0); }
        }

        .animate-enter {
            animation: fadeInUp 0.6s ease-out forwards;
        }

        /* Mobile Optimizations */
        @media (max-width: 768px) {
            .stApp { padding-top: 1rem; }
            .card-container { padding: 1.5rem; }
            .glass-panel { padding: 1.5rem; }

            /* Full width buttons on mobile */
            div.stButton > button {
                width: 100%;
                min-height: 48px; /* Touch target */
            }

            .avatar-img {
                width: 90px;
                height: 90px;
            }
        }

        /* Desktop Optimizations */
        @media (min-width: 1200px) {
            .block-container {
                max-width: 1100px;
                padding-top: 3rem;
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
    # Hero Section with Animation
    st.markdown("""
    <div class="animate-enter" style='text-align: center; padding: 4rem 0;'>
        <h1>The Catcher in the Rye</h1>
        <h3 class="hero-subtitle">An Interactive Explorer into Holden's World</h3>
        <div style='width: 80px; height: 6px; background-color: var(--primary-color); margin: 0 auto 2rem auto; border-radius: 4px;'></div>
    </div>
    """, unsafe_allow_html=True)

    # Introduction
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("""
        <div class="glass-panel animate-enter" style="height: 100%; display: flex; flex-direction: column; justify-content: center; animation-delay: 0.1s;">
            <p style='font-size: 1.25em; margin-bottom: 1.5rem; font-family: Merriweather, serif; font-style: italic; border-left: 3px solid var(--primary-color); padding-left: 1rem;'>
                "If you really want to hear about it, the first thing you'll probably want to know is where I was born, and what my lousy childhood was like..."
            </p>
            <p>
                Dive into the complex mind of Holden Caulfield. Explore the characters who shaped his journey and the recurring themes that define J.D. Salinger's masterpiece.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="animate-enter" style="border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-md); height: 100%; animation-delay: 0.2s;">
            <img src="https://images.pexels.com/photos/1631677/pexels-photo-1631677.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                 style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Rye Field">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True) # Spacer

    st.markdown("<h3 class='animate-enter' style='text-align: center; margin-bottom: 2rem; animation-delay: 0.3s;'>Start Your Journey</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
        <div class="card-container animate-enter" style="align-items: flex-start; text-align: left; min-height: 220px; animation-delay: 0.4s;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🎭</div>
            <h3>Characters</h3>
            <p>Unpack the psyche of Holden, Phoebe, Allie, and others. Discover their hidden motivations and relationships.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Characters", use_container_width=True):
            navigate_to("Characters")

    with col2:
        st.markdown("""
        <div class="card-container animate-enter" style="align-items: flex-start; text-align: left; min-height: 220px; animation-delay: 0.5s;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">📚</div>
            <h3>Themes</h3>
            <p>Analyze the core motifs: The pain of growing up, the search for identity, and the pervasive nature of phoniness.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Themes", use_container_width=True):
            navigate_to("Themes")

def show_characters_grid():
    st.markdown("""
    <div class="animate-enter" style='text-align: center; margin-bottom: 3rem;'>
        <h1>Meet the Characters</h1>
        <p class='hero-subtitle'>The voices of Pencey Prep and New York</p>
    </div>
    """, unsafe_allow_html=True)

    # Responsive Grid: 4 columns on desktop
    cols = st.columns(4)
    for i, char in enumerate(characters_data):
        with cols[i % 4]:
            delay = (i * 0.05) % 0.5 # Staggered animation
            st.markdown(f"""
            <div class="card-container animate-enter" style="align-items: center; text-align: center; padding-top: 2rem; animation-delay: {delay}s;">
                <img src="{char['image_url']}" class="avatar-img" alt="{char['name']}">
                <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">{char['name']}</h4>
                <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.4;">{char['traits'][0] if char['traits'] else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View Profile", key=f"btn_{char['name']}", use_container_width=True):
                select_char(char)

def show_character_detail(char):
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Characters", key="back_char"):
        navigate_to("Characters")

    # Enhanced Header with Glassmorphism
    st.markdown(f"""
    <div class="glass-panel animate-enter" style="display: flex; flex-wrap: wrap; align-items: center; gap: 2rem; margin-bottom: 2rem;">
        <img src="{char['image_url']}" class="avatar-img" style='width: 160px; height: 160px; margin: 0;'>
        <div style="flex: 1; min-width: 280px;">
            <h1 style='margin: 0;'>{char['name']}</h1>
            <p style='font-style: italic; font-size: 1.1em; color: var(--text-muted); margin-top: 10px; border-left: 3px solid var(--primary-color); padding-left: 15px;'>{char['significance']}</p>
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
        <div class="animate-enter" style='background-color: #fff; padding: 2rem; border-radius: var(--radius-md); border-left: 5px solid var(--secondary-color); box-shadow: var(--shadow-sm); font-size: 1.1em; animation-delay: 0.1s;'>
            {char['first_appearance_context']}
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Connections")
        if char['relationships']:
            for i, (name, desc) in enumerate(char['relationships'].items()):
                delay = (i * 0.05) % 0.5
                st.markdown(f"""
                <div class="animate-enter" style="background: white; padding: 1.5rem; border-radius: var(--radius-sm); margin-bottom: 1rem; box-shadow: var(--shadow-sm); animation-delay: {delay}s;">
                    <strong style="color: var(--primary-color); font-size: 1.2em;">{name}</strong>
                    <p style="margin-top: 0.5rem; color: var(--text-main);">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific relationships noted.")

    with tab3:
        st.markdown("### Memorable Quotes")
        if char['quotes']:
            for i, q in enumerate(char['quotes']):
                delay = (i * 0.1) % 0.5
                st.markdown(f"<div class='quote-box animate-enter' style='animation-delay: {delay}s;'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with tab4:
        st.markdown("### Thematic Resonance")
        if char['associated_themes']:
            st.markdown(" ".join([f"<span class='badge theme' style='font-size: 1em; padding: 10px 15px;'>{t}</span>" for t in char['associated_themes']]), unsafe_allow_html=True)
        else:
            st.info("No themes associated.")

def show_themes_grid():
    st.markdown("""
    <div class="animate-enter" style='text-align: center; margin-bottom: 3rem;'>
        <h1>Literary Themes</h1>
        <p class='hero-subtitle'>The Deeper Meanings</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, theme in enumerate(themes_data):
        with cols[i % 3]:
            delay = (i * 0.1) % 0.5
            st.markdown(f"""
            <div class="card-container animate-enter" style="justify-content: flex-start; text-align: left; padding: 2.5rem; animation-delay: {delay}s;">
                <h3 style='margin-bottom: 1rem; color: var(--primary-color); border-bottom: 2px solid rgba(0,0,0,0.05); padding-bottom: 0.5rem; width: 100%;'>{theme['name']}</h3>
                <p style='font-size: 1rem; color: var(--text-muted);'>{theme['description'][:140]}...</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Theme", key=f"btn_{theme['name']}", use_container_width=True):
                select_theme(theme)

def show_theme_detail(theme):
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Themes", key="back_theme"):
        navigate_to("Themes")

    # Header
    st.markdown(f"""
    <div class="glass-panel animate-enter" style="margin-bottom: 2rem; border-left: 6px solid var(--primary-color);">
        <h1 style='margin-bottom: 1rem;'>{theme['name']}</h1>
        <p style='font-size: 1.2em; line-height: 1.8; color: var(--text-main); font-family: Lato, sans-serif;'>{theme['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("<h3 style='margin-bottom: 1rem;'>Illustrative Quotes</h3>", unsafe_allow_html=True)
        if theme['related_quotes']:
            for i, q in enumerate(theme['related_quotes']):
                delay = (i * 0.1) % 0.5
                st.markdown(f"<div class='quote-box animate-enter' style='animation-delay: {delay}s;'>“{q}”</div>", unsafe_allow_html=True)
        else:
            st.info("No quotes available.")

    with c2:
        st.markdown("<h3 style='margin-bottom: 1rem;'>Key Characters</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="animate-enter" style="background: white; padding: 2rem; border-radius: var(--radius-md); box-shadow: var(--shadow-sm); animation-delay: 0.2s;">
            <p style="margin-bottom: 1rem; color: var(--text-muted);">These characters embody or grapple with the theme of <strong>{}</strong>:</p>
            {}
        </div>
        """.format(theme['name'], " ".join([f"<span class='badge' style='font-size: 1em; padding: 8px 12px; margin: 4px;'>{char}</span>" for char in theme['characters_associated']])), unsafe_allow_html=True)

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
