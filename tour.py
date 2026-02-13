import streamlit as st
from characters import characters_data
from themes import themes_data

# --- Tour Steps Definition ---
TOUR_STEPS = [
    {
        "title": "Welcome",
        "content": "Welcome to the Catcher in the Rye Explorer. This interactive dashboard is designed to immerse you in J.D. Salinger's world. Let me show you around.",
        "target_page": "Home"
    },
    {
        "title": "The Mood",
        "content": "We begin with the mood. The 'Ultrathink' design uses noise textures and deep reds to reflect Holden's complex emotions—passion, anger, and alienation.",
        "target_page": "Home"
    },
    {
        "title": "Navigation",
        "content": "Below, you'll find the two main pillars of our analysis: Characters and Themes. Let's dive into the Characters first.",
        "target_page": "Home"
    },
    {
        "title": "Character Grid",
        "content": "Here is the cast of Pencey Prep and New York. Notice the glass cards—hover over them to see a subtle lift. This 'polished' feel is key to the experience.",
        "target_page": "Characters"
    },
    {
        "title": "Deep Dive: Holden",
        "content": "We've selected Holden. This detail view uses progressive disclosure: we only show high-level info first. Use the tabs below to explore his Relationships, Quotes, and Themes at your own pace.",
        "target_page": "Character Detail",
        "target_char": "Holden Caulfield"
    },
    {
        "title": "Themes Explorer",
        "content": "Finally, the Themes explorer. Here we analyze the deeper meanings—Phoniness, Innocence, Grief. Click any theme to see how it connects back to the characters.",
        "target_page": "Themes"
    },
    {
        "title": "Your Journey Begins",
        "content": "You are now ready to explore on your own. Enjoy the journey.",
        "target_page": "Themes" # Stay on Themes or go back to Home
    }
]

class TourManager:
    @staticmethod
    def start_tour():
        st.session_state.tour_active = True
        st.session_state.tour_step = 0
        st.rerun()

    @staticmethod
    def end_tour():
        st.session_state.tour_active = False
        st.session_state.tour_step = 0
        st.rerun()

    @staticmethod
    def next_step():
        if st.session_state.tour_step < len(TOUR_STEPS) - 1:
            st.session_state.tour_step += 1
            st.rerun()
        else:
            TourManager.end_tour()

    @staticmethod
    def prev_step():
        if st.session_state.tour_step > 0:
            st.session_state.tour_step -= 1
            st.rerun()

    @staticmethod
    def render_tour():
        if 'tour_active' not in st.session_state or not st.session_state.tour_active:
            return

        step_index = st.session_state.tour_step
        if step_index >= len(TOUR_STEPS):
            TourManager.end_tour()
            return

        step = TOUR_STEPS[step_index]

        # --- 1. Navigation Logic ---
        # Ensure we are on the correct page
        if st.session_state.page != step['target_page']:
            st.session_state.page = step['target_page']
            # Special handling for Character Detail
            if step['target_page'] == 'Character Detail' and 'target_char' in step:
                 # Find the character data
                char_data = next((c for c in characters_data if c['name'] == step['target_char']), None)
                if char_data:
                    st.session_state.selected_char = char_data
            st.rerun()

        # Additional check: If on Character Detail but wrong character, fix it
        if step['target_page'] == 'Character Detail' and 'target_char' in step:
            if st.session_state.selected_char['name'] != step['target_char']:
                 char_data = next((c for c in characters_data if c['name'] == step['target_char']), None)
                 if char_data:
                    st.session_state.selected_char = char_data
                    st.rerun()

        # --- 2. Render UI ---
        # We use a container with a specific marker class to anchor our CSS
        with st.container():
            st.markdown('<div class="tour-marker"></div>', unsafe_allow_html=True)

            # Tour Card Content
            # Note: The CSS will position the parent of .tour-marker fixed on screen

            # Progress Indicator
            st.markdown(f"<div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--secondary-color); margin-bottom: 0.5rem;'>Step {step_index + 1} of {len(TOUR_STEPS)}</div>", unsafe_allow_html=True)

            # Title
            st.markdown(f"<h3 style='margin-bottom: 0.5rem; font-size: 1.4rem !important;'>{step['title']}</h3>", unsafe_allow_html=True)

            # Content
            st.markdown(f"<p style='font-size: 1rem; color: var(--text-main); line-height: 1.5;'>{step['content']}</p>", unsafe_allow_html=True)

            # Buttons
            c1, c2, c3 = st.columns([1, 1, 1])

            # Using callbacks to avoid nested rerun issues if possible, but st.button returns bool
            # We need to be careful with unique keys
            with c1:
                if st.button("Previous", key=f"tour_prev_{step_index}", disabled=(step_index == 0)):
                    TourManager.prev_step()

            with c2:
                btn_label = "Finish" if step_index == len(TOUR_STEPS) - 1 else "Next"
                if st.button(btn_label, key=f"tour_next_{step_index}", type="primary"):
                    TourManager.next_step()

            with c3:
                if st.button("End Tour", key=f"tour_end_{step_index}"):
                    TourManager.end_tour()
