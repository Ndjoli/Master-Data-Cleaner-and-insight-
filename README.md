# 🧼 Master Data Cleaner & Insight Generator

An AI-powered Streamlit app that cleans messy datasets (CSV or Excel), provides GPT-generated cleaning suggestions, and exports a full PDF cleaning report. Built to demonstrate the power of AI agent workflows in business data scenarios.

🔗 **Live App:** [Try it Here](https://ai-master-cleaner.streamlit.app/)

---

## 💬 What This Project Does

This tool acts like an intelligent data janitor:
- Analyzes your uploaded dataset (CSV or Excel)
- Flags issues like missing values, duplicates, and empty columns
- Offers GPT-powered cleaning suggestions using OpenAI GPT-3.5
- Lets you apply common cleaning operations in one click
- Exports the cleaned data + an automated PDF report summarizing the cleaning process

Built to help analysts, startups, and recruiters save time with AI-augmented cleaning.

---

## 🧰 Tech Stack

**Language:** Python  
**Frameworks/Libraries:**  
- Streamlit (for UI)  
- Pandas (data handling)  
- OpenAI Python SDK (GPT integration)  
- FPDF (PDF report generation)  
- OpenPyXL (Excel compatibility)

---

## 🚀 How to Run Locally

1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-username/master-data-cleaner.git
   cd master-data-cleaner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key:**

   Create a file `.streamlit/secrets.toml`:
   ```toml
   openai_key = "sk-..."
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## 📦 Requirements

```
streamlit
pandas
openai>=1.1.0
fpdf
openpyxl
``

## 📬 Contact

📧 armanndjoli97@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/arman-ndjoli97)
