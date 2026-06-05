# TARDIS: Time Analysis & Railway Delay Intelligence System

TARDIS is an end-to-end Machine Learning ecosystem designed to analyze, clean, and predict SNCF railway delays. By leveraging historical transport logs, the system trains an ensemble learning model to forecast arrival delays based on journey characteristics, ambient factors, and real-time structural incidents. It features a responsive, cached Streamlit web dashboard suitable for both B2C passengers (to mitigate trip uncertainty) and B2B railway operators (to run strategic "What-If" crisis simulations).

---

## Key Features

* **Advanced ETL Pipeline:** Automated data cleansing, duplication removal, and robust textual NA repair inside a dedicated exploratory phase.
* **Feature Engineering:** Converts raw temporal logs into discrete model dimensions (Year, Month, Weekday, Is_Weekend) to allow the model to discover deep seasonal patterns.
* **Ensemble Learning Engine:** A fine-tuned Random Forest Regressor capable of capturing intricate, non-linear relationships that classic linear models fail to resolve.
* **Anti-Data Leakage Logic:** Built-in dashboard matrix alignment that automatically compensates for missing runtime features and structurally re-injects delayed departure weights into arrival matrices.
* **High-Performance Inference:** Implements `@st.cache_resource` serialization, allowing the binary pre-trained model to load once in memory and serve inferences in under 100ms.
* **Tricolor Contextual UI:** User-centric conditional alerting (Success/Warning/Error) mapping mathematical predictions directly to practical decision-making thresholds.

---

## Project Architecture

```text
├── tardis_eda.ipynb       # Phase 1: Extraction, Cleansing, and Feature Engineering
├── tardis_model.ipynb     # Phase 2: Matrix Building, Train/Test Splitting, Training & Evaluation
├── tardis_dashboard.py    # Phase 3: Production Web Interface (Streamlit Application)
├── requirements.txt       # System dependencies and Python libraries listing
└── .gitignore             # Git shield preventing heavy cache/binary/data leakage

Installation & Setup
1. Clone the Repository
Bash

git clone [https://github.com/your-repo/G-AIA-210-STG-2-1-tardis-2.git](https://github.com/your-repo/G-AIA-210-STG-2-1-tardis-2.git)
cd G-AIA-210-STG-2-1-tardis-2

2. Configure the Virtual Environment

Create an isolated Python environment to prevent library collisions:
Bash

python3 -m venv tardis_env
source tardis_env/bin/activate

3. Install Dependencies

Install all required libraries using the provided packet manager log:
Bash

pip install -r requirements.txt

Data & Machine Learning Pipeline
Step 1: Exploratory Data Analysis & Cleaning (tardis_eda.ipynb)

The pipeline ingests raw railway logs (dataset.csv) and executes a structural cleaning protocol:

    Feature Selection: Drops free-text comment columns (Cancellation comments, Departure delay comments, Arrival delay comments) that introduce training noise.

    Data Integrity: Identifies missing indices, drops rows lacking date entries, and converts raw strings or textual 'nan' markers into true mathematical nulls (np.nan).

    Route Deduplication: Purges redundant route entries recorded for the exact same station pair on identical dates.

    Feature Engineering: Deconstructs the standard Date vector into 4 explicit numeric variables: year, month, weekday, and is_weekend (binary flag).

    Standardization: Coerces all quantitative columns into numerical values before exporting the processed dataset to cleaned_dataset.csv.

Step 2: Model Training & Evaluation (tardis_model.ipynb)

The model building notebook handles statistical modeling and benchmarking:

    Matrix Cleansing: Safely fills remaining tabular gaps with 0 (assuming empty incident cells mean no incident occurred) and locks the matrix format to numeric elements.

    Train/Test Splitting: Isolates the target vector (Average delay of all trains at arrival) and splits the features matrix using a strict 80% Training / 20% Testing partition to monitor generalization and avoid overfitting.

    Benchmarking: Pitches a Baseline Linear Regression model against an optimized Random Forest Regressor. The Random Forest model demonstrates substantial architectural superiority by accurately mapping multi-modal delays (e.g., compounding infrastructure failure rates with winter weather trends).

    Metrics Evaluated:

        MAE (Mean Absolute Error): Outlines the average minute-wise margin of error for intuitive business feedback.

        RMSE (Root Mean Squared Error): Severely penalizes outlier errors or aberrant runtime estimations.

        R² Score: Evaluates global variance explanation metrics.

    Serialization: Freezes the final Random Forest model into a compact binary artifact (model.pkl) using joblib for rapid server deployments.

Step 3: Production Web Dashboard (tardis_dashboard.py)

Launches the interactive prediction interface using the serialized intelligence block:
Bash

streamlit run tardis_dashboard.py

Dashboard User Guide & UI Features

The layout features three operational input segments mapping directly to the model's 22 internal matrix dimensions:

    Structural Inputs (Column 1): Captures core trip attributes like Average journey time (min) and the Number of scheduled trains.

    Temporal & Departure Inputs (Column 2): Processes contextual factors such as the Trip Period (Weekdays vs. Weekends) and the Estimated departure delay (min).

    Incident Simulators (Column 3): Sliders mapping external disturbance intensities like External causes % (e.g., Weather) and Infrastructure causes %.

Operational Thresholds & Responses

When the user clicks "Estimer mon retard à l'arrivée", the dashboard maps the quantitative float prediction to a tricolor user alert status:

    Minime (<= 5 mins): Returns a comforting success badge encouraging travel: "Bon voyage ! Le retard estimé est minime : X minutes."

    Moderate (<= 15 mins): Returns a cautionary warning: "Attention, un léger retard est estimé à : X minutes."

    Critique (> 15 mins): Triggers a high-priority alert warning the passenger or manager to adjust plans: "Prévoyez de la marge ! Le retard estimé est de : X minutes."

Version Control Best Practices (.gitignore)

To safeguard repository storage limits, improve download performance, and conform to professional deployment standards, a strict .gitignore layout isolates environment configurations, massive data tables, and pre-trained binaries from version control histories:
Plaintext

# Data files & Tabular sets
*.csv
dataset.csv
cleaned_dataset.csv

# Serialized AI model artifacts
*.pkl
model.pkl

# Python Virtual Environments
tardis_env/
venv/
env/
.env

# Jupyter and Python runtime caches
__pycache__/
.ipynb_checkpoints/

Project Roadmap

    TARDIS 2.0: Moving away from static batch-trained predictions towards real-time stream processing by connecting directly to live IoT track sensors.

    Quantum Acceleration: Integrating quantum-inspired decision tree optimization to scale up prediction accuracies toward a 99.9% target ceiling.

Contributors

    Dragos Nicolier - Data Scientist & Core Dashboard Engineer

    Alan-Ilian-Imran Traore - Data Analyst & ETL Pipeline Architect
