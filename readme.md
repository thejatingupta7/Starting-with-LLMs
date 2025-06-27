# 🧠 Starting with LLMs

A quick guide to get started with local LLMs using Python, Ollama, and Streamlit.

---

## 📦 Prerequisites

* Python: **3.13.2** or any compatible version.
* Git (for cloning the repository).

---

## 🔁 Clone the Repository

```bash
git clone https://github.com/thejatingupta7/Starting-with-LLMs.git
cd Starting-with-LLMs
```

---

## 🛠️ Environment Setup

### Create and Activate a Virtual Environment

```powershell
python -m venv myenv
myenv\Scripts\activate       # or .\myenv\Scripts\Activate.ps1
```

---

## ⚙️ Install Dependencies

### For GPU Users:

```bash
pip install torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/cu118
pip install ollama transformers datasets scikit-learn ipykernel streamlit faiss-cpu hf-xet langchain langchain-community sentence-transformers openpyxl pymupdf
```

### For CPU Users:

```bash
pip install ollama torch transformers datasets scikit-learn ipykernel streamlit faiss-cpu hf-xet langchain langchain-community sentence-transformers openpyxl pymupdf
```

---

## 📥 Download the Base LLM

1. Download and install **Ollama** from [https://ollama.com](https://ollama.com).

2. Install it in the same directory where your code/venv resides (recommended):

   ```powershell
   .\OllamaSetup.exe /DIR="D:\Ollama"
   ```

3. Pull the base quantized model:

   ```bash
   ollama pull llama3.2:1b
   ```

---

## 🚀 Run the Apps

### 1. Basic Chat UI (`app1.py`)

```bash
streamlit run app1.py
```

---

### 2. RAG-Enabled App (`app2.py`)

Generate the vector store first:

```bash
python vectorstore_builder.py
```

Then run the RAG-based app:

```bash
streamlit run app2.py
```

---

### 3. Visualize Your Vectorstore

```bash
python visual.py
```

