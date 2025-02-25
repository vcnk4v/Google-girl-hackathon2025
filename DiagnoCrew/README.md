# Medical Diagnostic Assistant

A modular Streamlit application designed to assist healthcare professionals in diagnostic processes.

## Features

- Patient information management
- Medical image upload and analysis
- Symptom recording and tracking
- Laboratory results analysis
- AI-assisted diagnostic recommendations

## Installation and Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

## Project Structure

```
medical-diagnostic-assistant/
│
├── app.py                     # Main application entry point
├── config.py                  # Application configuration
├── state.py                   # Session state management
├── constants.py               # Application constants
│
├── components/                # Reusable UI components
│   ├── sidebar.py             # Navigation sidebar
│   ├── patient_info_display.py # Patient info display
│   └── navigation_buttons.py  # Navigation buttons
│
├── pages/                     # Individual application pages
│   ├── home.py                # Home page
│   ├── patient.py             # Patient information page
│   ├── images.py              # Medical image upload page
│   ├── symptoms.py            # Symptoms and lab results page
│   └── results.py             # Diagnostic results page
│
└── utils/                     # Utility functions
    ├── diagnostics.py         # Diagnostic analysis utilities
    └── reporting.py           # Report generation utilities
```

## Extending the Application

To add new functionality:

1. Add new constants to `constants.py`
2. Create new utility functions in the appropriate file in `utils/`
3. Create new UI components in `components/` if needed
4. Modify existing pages or add new pages in `pages/`
5. Update the navigation in `sidebar.py` if needed

## Note

This is a prototype for demonstration purposes only. It is not intended for clinical use.
