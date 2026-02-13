import sys
from unittest.mock import MagicMock
import types

# Create a mock streamlit module
streamlit_mock = MagicMock()
sys.modules['streamlit'] = streamlit_mock

# Mock session state
streamlit_mock.session_state = {}

# Import tour to verify no syntax/runtime errors at module level
try:
    import tour
    print("tour.py imported successfully.")
except Exception as e:
    print(f"Error importing tour.py: {e}")
    sys.exit(1)

# Check if TourManager exists
if hasattr(tour, 'TourManager'):
    print("TourManager class found.")
else:
    print("TourManager class NOT found.")
    sys.exit(1)
