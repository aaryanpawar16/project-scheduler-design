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

# 📸 Documentation: Visual Walkthrough
1. The Intelligence Gate: Parametric Input & Similarity Detection
This is the starting point of the Grounded-RAG workflow. Instead of a blank prompt, the system requires structural parameters to define the search space.
•	What it shows: The user defines the project context (e.g., Northeast Region, Clinical Infrastructure, Hospitals). Immediately upon clicking "Generate," the system performs a weighted Euclidean distance calculation against the meta_data.csv.
•	Technical Description: The "Similarity Detection Logs" (visible on the main screen) display the Grounding Confidence. This provides transparency by showing the specific Project IDs from which the AI is "learning" its schedule logic. It proves the system is retrieving real construction data before generating a single task.
 

2. The Executive Dashboard: Multimodal Visualization
Once the retrieval is complete, the LLM orchestrates the data into three distinct, synchronized views.
•	What it shows: The Executive Overview cards, the Live Gantt Chart, and the Financial Allocation donut chart.
•	Technical Description: This view represents the Transformation Layer. The LLM processes the raw CSV retrieval and outputs a stateful data block. Streamlit then parses this block into interactive Plotly objects. This allows stakeholders to immediately identify the Peak Labor Phase and Critical Path without reading through raw spreadsheets.
 
3. Dynamic Risk Modeling: Weather Simulation
This feature demonstrates the Stateful Refinement capability of the system.
•	What it shows: The user adjusting the "Delay Duration" slider in the sidebar and the resulting update in the chat bubble and Gantt chart.
•	Technical Description: When a weather delay is triggered, the prompt design forces a Chain-of-Thought (CoT) reasoning process. The AI identifies specific "outdoor-sensitive" phases (like Substructure or Exterior Fabrication) and applies a temporal shift. Because the system maintains dependency logic, the entire timeline "ripples" forward, accurately reflecting how real-world delays impact project delivery.
 
4. Conversational Refinement: The Schedule Assistant
The Assistant is the bridge between human expertise and AI automation.
•	What it shows: A clean, numbered chat history where the user asks for specific optimizations (e.g., "Make construction 10 days faster").
•	Technical Description: The Assistant uses Prompt Shielding and Selective Markdown Rendering. We filter out the "Machine Data" (CSV tags) from the chat bubbles to provide a clean, human-readable narrative. The LLM justifies its changes (e.g., "Shortened 'Finishes' by 5 days as it had the most flexibility") while simultaneously updating the backend data to keep the charts in sync.

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
