"""
Main application entry point for ATK Classifier.
Implements sidebar navigation and routes to appropriate pages.
"""
import streamlit as st

from app.config import settings
from app.components.predictor import PredictionEngine
from app.pages import home, predict, dashboard, model_management


# Page configuration
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state() -> None:
    """Initialize session state variables."""
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Home"


def render_demo_mode_indicator(is_demo: bool) -> None:
    """
    Render demo mode indicator in sidebar.
    
    Args:
        is_demo: Whether running in demo mode
    """
    if is_demo:
        st.sidebar.warning(
            "🔔 **Demo Mode**\n\n"
            "No trained model found. "
            "Predictions are simulated."
        )
    else:
        st.sidebar.success(
            "✅ **Production Mode**\n\n"
            "Model loaded successfully."
        )


def render_sidebar_navigation() -> str:
    """
    Render sidebar navigation menu.
    
    Returns:
        Selected page name
    """
    st.sidebar.title(f"🏷️ {settings.APP_NAME}")
    st.sidebar.markdown(f"*v{settings.APP_VERSION}*")
    st.sidebar.markdown("---")
    
    # Navigation menu
    pages = {
        "Home": "🏠",
        "Predict": "🎯",
        "Dashboard": "📊",
        "Model Management": "🔧"
    }

    # Get current page from session state
    current_page = st.session_state.get("nav_page", "Home")
    
    # Create navigation buttons
    st.sidebar.markdown("### Navigation")
    
    for page_name, icon in pages.items():
        # Highlight active page
        if page_name == current_page:
            button_type = "primary"
        else:
            button_type = "secondary"
        
        if st.sidebar.button(
            f"{icon} {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type=button_type
        ):
            st.session_state.nav_page = page_name
            st.rerun()
    
    return current_page


def render_sidebar_info() -> None:
    """Render additional sidebar information."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown(f"""
    {settings.APP_DESCRIPTION}
    
    **Supported Classes:**
    """)
    
    # Display class names in compact format
    for class_name in settings.CLASS_NAMES:
        st.sidebar.markdown(f"- {class_name}")


def route_to_page(page_name: str) -> None:
    """
    Route to the appropriate page based on selection.
    
    Args:
        page_name: Name of the page to render
    """
    page_map = {
        "Home": home.render,
        "Predict": predict.render,
        "Dashboard": dashboard.render,
        "Model Management": model_management.render
    }
    
    render_func = page_map.get(page_name, home.render)
    render_func()


def main() -> None:
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Check demo mode
    engine = PredictionEngine()
    is_demo = engine.is_demo_mode()
    
    # Render sidebar
    selected_page = render_sidebar_navigation()
    render_demo_mode_indicator(is_demo)
    render_sidebar_info()
    
    # Route to selected page
    route_to_page(selected_page)


if __name__ == "__main__":
    main()
