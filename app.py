import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from fpdf import FPDF
import datetime

# 🚀 Page config
st.set_page_config(page_title="AI Data Cleaner", layout="wide")
st.title("🪼 Master Data Cleaner & Insight Generator")

# 🔑 OpenAI API Key (from Streamlit secrets)
client = OpenAI(api_key=st.secrets["openai_key"])

# 📄 Upload section
st.subheader("Step 1: Upload Your Dataset")
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

# Global holders
gpt_suggestions = ""
null_counts = pd.Series()
duplicate_count = 0
cleaned_df = None
df = pd.DataFrame()

if uploaded_file is not None:
    try:
        file_ext = os.path.splitext(uploaded_file.name)[-1]

        if file_ext == ".csv":
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # Phase 1: Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(20))

        st.markdown("### 📊 Dataset Info")
        st.write(f"📜 Rows: `{df.shape[0]}`")
        st.write(f"📜 Columns: `{df.shape[1]}`")
        st.write(f"📦 Size: ~{uploaded_file.size // 1024} KB")

        # Phase 2: Data Quality Report
        st.subheader("🧪 Step 2: Data Quality Report")

        null_counts = df.isnull().sum()
        total_nulls = null_counts.sum()
        st.write(f"🔸 **Total Missing Values:** `{total_nulls}`")
        st.dataframe(null_counts[null_counts > 0].sort_values(ascending=False))

        duplicate_count = df.duplicated().sum()
        st.write(f"🔸 **Duplicate Rows:** `{duplicate_count}`")

        st.markdown("🔸 **Column Types:**")
        st.dataframe(df.dtypes.astype(str))

        empty_cols = [col for col in df.columns if df[col].count() == 0]
        if empty_cols:
            st.warning(f"⚠️ Empty Columns: {empty_cols}")
        else:
            st.success("✅ No completely empty columns detected.")

        # Phase 3: GPT Suggestions
        st.subheader("🧠 Step 3: AI Cleaning Suggestions")

        if st.button("Get AI Cleaning Suggestions"):
            with st.spinner("Thinking like a data janitor... 🧫"):
                prompt = f"""
You're a data cleaning expert. Based on the following dataset, suggest steps to clean and standardize it.

Column Types:
{df.dtypes.to_string()}

Null Value Summary:
{df.isnull().sum().to_string()}

Sample Rows:
{df.head(5).to_string(index=False)}

Be specific and include common practices like handling missing values, standardizing columns, fixing data types, etc.
                """
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=600,
                        temperature=0.3
                    )
                    gpt_suggestions = response.choices[0].message.content
                    st.success("✅ AI Suggestions Ready!")
                    st.markdown(gpt_suggestions)
                except Exception as e:
                    st.error(f"OpenAI error: {e}")

        # Phase 4: Clean & Export
        st.subheader("🯝 Step 4: Clean & Export")

        drop_nulls = st.checkbox("🗑️ Drop rows with missing values")
        fill_nulls = st.checkbox("✏️ Fill missing values with placeholder")
        drop_dupes = st.checkbox("🗑️ Drop duplicate rows")
        rename_columns = st.text_input(
            "🔤 Rename columns (format: old:new, comma-separated)",
            placeholder="e.g. Name:CustomerName, Age:CustomerAge"
        )

        if st.button("🯼 Apply Cleaning"):
            cleaned_df = df.copy()

            if drop_nulls:
                cleaned_df = cleaned_df.dropna()

            if fill_nulls:
                cleaned_df = cleaned_df.fillna("N/A")

            if drop_dupes:
                cleaned_df = cleaned_df.drop_duplicates()

            if rename_columns:
                try:
                    mappings = {
                        pair.split(":")[0].strip(): pair.split(":")[1].strip()
                        for pair in rename_columns.split(",")
                    }
                    cleaned_df = cleaned_df.rename(columns=mappings)
                except Exception as e:
                    st.warning(f"⚠️ Column rename failed: {e}")

            st.success("✅ Cleaning complete! Preview below:")
            st.dataframe(cleaned_df.head(20))

            # Layout buttons side by side
            col1, col2 = st.columns(2)

            with col1:
                csv = cleaned_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📅 Download Cleaned CSV",
                    data=csv,
                    file_name="cleaned_data.csv",
                    mime="text/csv"
                )

            with col2:
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt="Final Data Cleaning Report", ln=True, align="C")
                    pdf.set_font("Arial", size=10)
                    pdf.ln(5)

                    pdf.multi_cell(0, 8, f"File cleaned on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
                    pdf.cell(200, 10, txt=f"Original shape: {df.shape}", ln=True)
                    pdf.cell(200, 10, txt=f"Cleaned shape: {cleaned_df.shape}", ln=True)
                    pdf.ln(5)

                    pdf.multi_cell(0, 8, f"Null Value Summary:\n{null_counts.to_string()}")
                    pdf.cell(200, 10, txt=f"Duplicate Rows Removed: {duplicate_count}", ln=True)

                    pdf.ln(5)
                    pdf.multi_cell(0, 8, "Actions Taken:")
                    if drop_nulls:
                        pdf.multi_cell(0, 8, "- Dropped rows with nulls")
                    if fill_nulls:
                        pdf.multi_cell(0, 8, "- Filled missing values with 'N/A'")
                    if drop_dupes:
                        pdf.multi_cell(0, 8, "- Removed duplicate rows")
                    if rename_columns:
                        pdf.multi_cell(0, 8, f"- Renamed columns: {rename_columns}")

                    if gpt_suggestions:
                        pdf.ln(4)
                        pdf.multi_cell(0, 8, f"AI Suggestions:\n{gpt_suggestions}")

                    pdf_output_path = "cleaning_report.pdf"
                    pdf.output(pdf_output_path)

                    with open(pdf_output_path, "rb") as f:
                        st.download_button(
                            label="📄 Download Cleaning Report",
                            data=f,
                            file_name="cleaning_report.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Report generation failed: {e}")

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a CSV or Excel file to begin.")
# 🌐 Footer
st.markdown(
    """
    <hr style="margin-top: 50px;">
    <div style="text-align: center; font-size: 0.9em; color: gray;">
        Built with 🧠 by <strong>Iloyeka Arman Ndjoli</strong> |
        <a href="https://github.com/Ndjoli/Master-Data-Cleaner-and-insight-" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/arman-ndjoli97" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)
