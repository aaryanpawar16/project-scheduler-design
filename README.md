# 🏗️ Intelligent Project Schedule Designer
An AI-powered construction orchestration platform that generates grounded, data-driven project schedules using a Retrieval-Augmented Generation (RAG) pipeline. Unlike generic AI, this system leverages historical project metadata to ensure schedules are realistic and regionally accurate.

# 🚀 The Core Workflow
The system demonstrates a clear, logical pipeline to move from a concept to a high-fidelity execution plan:

Input Module: User defines project parameters (Region, Market, Type, Budget, Size).

Similarity Detection: A weighted engine analyzes Project_JOB_meta_data.csv to find the most relevant historical "Parent Projects."

Schedule Retrieval: Raw task sequences and dependency logic are extracted from Project_Schedule_Data.csv based on the detected matches.

LLM Generation: Azure OpenAI (GPT-4o) synthesizes the historical context with new constraints to produce a validated, stateful schedule.

# ✨ Key Features
📊 Executive Dashboard
Live Gantt Chart: Interactive timeline visualization of project tasks.

Financial Allocation: Donut chart breakdown of costs across project phases.

Manpower Analysis: Automated estimation of daily labor force and peak labor phases.

# ⛈️ Risk Management (Weather Simulation)
Simulate real-world delays (Rain, Snow, Hurricanes).

Ripple Effect Logic: AI automatically identifies outdoor tasks and shifts the entire dependency chain, recalculating the project completion date.

# 🔍 Similarity Logging
Full transparency into the RAG process.

Displays specific Project IDs and Match Scores (e.g., Project_0567 | 87% Match) to prove the schedule is grounded in data.

# 🛠️ Technical Stack
Frontend: Streamlit

LLM Orchestration: Azure OpenAI (GPT-4o)

Data Handling: Pandas

Visualizations: Plotly

Similarity Engine: Custom Weighted Euclidean/Cosine logic

# 📂 Folder Structure
Bash
project-schedule-designer/

├── app.py                # Main Streamlit Dashboard

├── data/

│   ├── Project_JOB_meta_data.csv    # Historical Metadata

│   └── Project_Schedule_Data.csv    # Historical Task Data

├── src/

│   ├── similarity.py     # Similarity Detection Engine

│   ├── retrieval.py      # Data Retrieval Logic

│   └── llm_agent.py      # Azure OpenAI Orchestration

├── requirements.txt      # Dependencies

└── .env                  # API Keys

# 🏃 Getting Started
Clone the repository:

git clone https://github.com/aaryanpawar16/project-schedule-designer.git

Install dependencies:

pip install -r requirements.txt

Setup Environment Variables:

Create a .env file and add your Azure credentials:

Code snippet

AZURE_OPENAI_KEY="your_key_here"
AZURE_OPENAI_ENDPOINT="your_endpoint_here"
Run the App:

streamlit run app.py
