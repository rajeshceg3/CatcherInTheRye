# The Catcher in the Rye - Character Explorer Dashboard

This project is a simple interactive dashboard built with Python and Streamlit to explore characters from J.D. Salinger's novel, *The Catcher in the Rye*.

## Features

*   Displays a list of major characters from the novel.
*   For each selected character, shows:
    *   Significance to the story
    *   Key personality traits
    *   Relationships with other characters
    *   Memorable quotes (where available)
    *   Context of their first appearance
*   User-friendly interface with a sidebar for character selection.
*   Wide layout for better readability.

## Project Structure

*   `catcher_dashboard.py`: The main Streamlit application script.
*   `characters.py`: Contains the data for the characters in a Python list of dictionaries.
*   `requirements.txt`: Lists the Python packages required to run the dashboard.
*   `README.md`: This file.

## Requirements

*   Python 3.7+
*   Streamlit

## Setup and Running

1.  **Clone the repository (or ensure files are in the same directory):**
    ```bash
    # If you have git installed
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run catcher_dashboard.py
    ```

    This will typically open the dashboard in your default web browser.

## Data Source

The character information compiled in `characters.py` is based on general knowledge and summaries of the novel, primarily informed by the Wikipedia page for *The Catcher in the Rye*.

## Contributing

Feel free to fork this repository and add more characters, details, or features.
