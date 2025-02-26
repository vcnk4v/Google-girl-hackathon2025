# DiagnoCrew - Medical Diagnostic Assistant

DiagnoCrew is a medical diagnostic assistant powered by AI agents. It uses a crew of agents to analyze patient symptoms, medical history, and lab results to provide a comprehensive diagnostic report.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
   - [Clone the Repository](#clone-the-repository)
   - [Create a Virtual Environment](#create-a-virtual-environment)
   - [Install Dependencies](#install-dependencies)
3. [Running the Application](#running-the-application)
4. [Project Structure](#project-structure)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Streamlit**: Will be installed as part of the dependencies.

---

## Setup

### Clone the Repository

1. Open a terminal or command prompt.
2. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/DiagnoCrew.git
   ```

3. Navigate to the project directory:

   ```bash
   cd DiagnoCrew
   ```

---

### Create a Virtual Environment

1. Create a virtual environment in the project directory:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:

   - **On Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

   You should see `(.venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

3. Go into medical_assistants directory and run

   ```
   crewai install
   ```

4. Return to DiagnoCrew directory

5. Add your GEMINI API key to .env files by adding `GEMINI_API_KEY=<your_api_key>` or run on the terminal: `export GEMINI_API_KEY=<your_api_key>`.

---

### Install Dependencies

1. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the dependencies listed in the `requirements.txt` file, including Streamlit and the `crewai` library.

---

## Running the Application

1. Ensure you are in the `DiagnoCrew` directory and the virtual environment is activated.
2. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

3. The app will start, and a local server will be launched. You should see a message like this in your terminal:

   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

4. Open your web browser and navigate to the provided URL (e.g., `http://localhost:8501`).

---

## Project Structure

Here’s an overview of the project structure:

```
.
├── brain_mri_ViT.ipynb          # Jupyter Notebook for Brain MRI analysis
├── data/                        # Data files
│   └── normal_ultrasound.jpeg   # Sample ultrasound image
├── demo.webm                    # Demo video
├── DiagnoCrew/                  # Main project directory
│   ├── app.py                   # Streamlit app entry point (duplicate, can be removed)
│   ├── components/              # Reusable UI components
│   │   ├── navigation_buttons.py
│   │   ├── patient_info_display.py
│   │   └── sidebar.py
│   ├── config.py                # Configuration settings
│   ├── constants.py             # Constants used in the app
│   ├── diagnostic_data/         # Diagnostic data and reports
│   │   └── CASE_20250226_110959_a/
│   │       ├── data_package.json
│   │       └── diagnosis.json
│   ├── diagnostic_report.json   # Sample diagnostic report
│   ├── docs/                    # Documentation and diagrams
│   │   ├── diagram.png
│   │   ├── diagram.wsd
│   │   ├── workflow.png
│   │   └── workflow.wsd
│   ├── medical_assistants/      # AI agents and backend logic
│   │   ├── backend_services.py  # Backend services for the app
│   │   ├── knowledge/           # Knowledge base for the AI
│   │   │   ├── file.txt
│   │   │   └── questions_and_answers.json
│   │   ├── pyproject.toml       # Python project configuration
│   │   ├── README.md            # Documentation for medical_assistants
│   │   ├── src/                 # Source code for medical assistants
│   │   │   └── medical_assistants/
│   │   │       ├── config/      # Configuration files for agents and tasks
│   │   │       │   ├── agents.yaml
│   │   │       │   └── tasks.yaml
│   │   │       ├── crew.py      # Crew definition and setup
│   │   │       ├── __init__.py  # Package initialization
│   │   │       └── main.py      # Main logic for running the crew
│   │   ├── tests/               # Unit tests (currently empty)
│   │   ├── trained_agents_data.pkl  # Trained agents data
│   │   ├── training_data.pkl    # Training data for agents
│   │   └── uv.lock              # Dependency lock file
│   ├── pages/                   # Streamlit pages
│   │   ├── Diagnostic_Results.py
│   │   ├── Home.py
│   │   ├── Patient_Information.py
│   │   ├── Symptoms_Lab_Results.py
│   │   └── Upload_Images.py
│   ├── README.md
│   ├── requirements.txt         # Python dependencies
│   ├── state.py                 # State management for the app
│   └── utils/                   # Utility functions
│       ├── diagnostics.py       # Diagnostic utilities
│       └── reporting.py         # Reporting utilities
└── README.md                    # Main README file for the project
```

---

## Troubleshooting

### 1. **Virtual Environment Issues**

- If you encounter issues activating the virtual environment, ensure you are using the correct command for your operating system.
- If the virtual environment is not recognized, recreate it using `python -m venv .venv`.

### 2. **Dependency Installation Issues**

- If `pip install -r requirements.txt` fails, ensure you have the latest version of `pip`:
  ```bash
  pip install --upgrade pip
  ```
- If you still encounter issues, try installing the dependencies one by one:
  ```bash
  pip install streamlit crewai crewai-tools
  ```

### 3. **Streamlit App Not Running**

- Ensure you are in the `DiagnoCrew` directory before running `streamlit run app.py`.
- If the app does not open in your browser, manually navigate to `http://localhost:8501`.

## Features

- Patient information management
- Medical image upload and analysis
- Symptom recording and tracking
- Laboratory results analysis
- AI-assisted diagnostic recommendations

## Note

This is a prototype for demonstration purposes only. It is not intended for clinical use.
