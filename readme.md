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

### Create a Virtual Environment

```powershell
python -m venv myenv
```

### Activate the virtual Env.

```powershell
myenv\Scripts\activate       
```
or 
```powershell
.\myenv\Scripts\Activate.ps1
```
If above gives error: try running this in terminal, then activate:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
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

1. Download and install **Ollama** from [https://ollama.com](https://ollama.com). (installing directly saves in C drive)
#### or
1. To install it in D Drive, put downloaded `ollama.exe` file in the same folder as our code, then run this command:

   ```powershell
   .\OllamaSetup.exe /DIR="D:\Ollama"
   ```

3. Pull the base quantized model in another command prompt `cmd` outside VS code:

   ```bash
   ollama pull llama3.2:1b
   ```
   <b>Remember one thing, smaller models like these: `llama3.2:1b`, don't follow System prompt well.</b>

---
<i>
   
#### Backend Data Flow

Run `ollama serve` in a new termnial.

</i>

---


## 🚀 Run the Apps

Inside apps files, `app1.py` and `app2.py`, change the system prompt according to your need.

### 1. Basic Chat UI (`app1.py`)

```bash
streamlit run app1.py
```

---

### 2. RAG-Enabled App (`app2.py`)

Fill the `data/` folder with pdfs of your own choice. And run the following scripts

1. Generate the vector store first:

```bash
python vectorstore_builder.py
```

2. Then run the RAG-based app:

```bash
streamlit run app2.py
```

---

## Viusalize the vectorstore in 3d

First install `plotly`

```bash
pip install plotly nbformat>=4.2.0
```

Then run the `visual.ipynb` notebook. 

---

