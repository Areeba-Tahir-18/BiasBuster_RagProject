# BiasBuster_RagProject
# 🛡️ Bias Buster  
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)  
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)  
![LangChain](https://img.shields.io/badge/LangChain-Framework-purple)  

Bias Buster is an AI-powered tool that detects and explains potential bias in text, datasets, and AI-generated outputs.  
It leverages **LangChain**, **ChromeDB**, and **OpenAI** to provide transparent, contextual bias analysis for journalists, researchers, and organizations.

---

## 📌 Features
- 🔍 **Bias Detection** – Identify political, gender, racial, cultural, and other biases in text.
- 🧠 **Contextual Explanations** – Understand *why* the text may be biased.
- 📂 **Search & History** – Store and query past analyses using ChromeDB.
- ⚙️ **Customizable Prompts** – Fine-tune detection rules per domain.
- 📊 **Multiple Bias Categories** – Detect implicit, explicit, and statistical bias.

---

## 🛠️ Tech Stack
- **[LangChain](https://www.langchain.com/)** – LLM orchestration
- **[ChromeDB](https://chromadb.com/)** – Vector database for storage & retrieval
- **[OpenAI API](https://platform.openai.com/)** – Text understanding & analysis
- **Python 3.10+**

## 📂 Project Structure
bias-buster/
│
├── data/ # Sample datasets for testing
├── notebooks/ # Jupyter notebooks for experiments
│
├── src/
│ ├── main.py # Main script to run the tool
│ ├── analyzer.py # Bias detection logic
│ ├── storage.py # ChromeDB interaction
│ └── prompts.py # Prompt templates for OpenAI
│
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .env.example # Example environment variables

1️⃣ **Clone the repository
git clone https://github.com/Areeba-Tahir-18/BiasBuster_RagProject.git
cd bias-buster


2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


3️⃣ Install dependencies
pip install -r requirements.txt


4️⃣ Set environment variables
Create a .env file in the root directory
OPENAI_API_KEY=your_openai_api_key
CHROMADB_PATH=./chroma_storage

▶️ Usage
Run the main script:

 src/app.py
Example interaction:


Enter your text: Women are bad drivers.
[Bias Buster Output] 🚨 Gender bias detected.
Explanation: This statement generalizes a negative stereotype about women without evidence.
📊 Example Output
Input Text	Bias Type	Explanation
"Immigrants take our jobs."	Cultural/Ethnic Bias	Generalizes an entire group and attributes economic issues without context.
"The president is a genius."	Positive Bias	Overly positive sentiment without factual basis.
"All teenagers are lazy."	Age Bias	Assumes negative traits about all young people.




