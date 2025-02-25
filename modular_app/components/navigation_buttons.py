# components/navigation_buttons.py - Component for navigation buttons
import streamlit as st
from state import navigate_to


def render_navigation_buttons(prev_page=None, next_page=None, next_is_primary=True):
    """Render navigation buttons for moving between pages"""
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        if prev_page:
            if st.button(f"Back to {prev_page.title()}", use_container_width=True):
                navigate_to(prev_page)

    with col2:
        if next_page:
            button_type = "primary" if next_is_primary else "secondary"
            if st.button(
                f"Continue to {next_page.title()}",
                type=button_type,
                use_container_width=True,
            ):
                navigate_to(next_page)
