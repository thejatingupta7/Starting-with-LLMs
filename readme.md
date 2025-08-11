# 🧠 Starting with LLMs

![Bravo!](https://i.pinimg.com/originals/ef/8b/bd/ef8bbd4554dedcc2fd1fd15ab0ebd7a1.gif)

Don't be like this cat, just try for once, the repo will guide you: 😊😏

---

A quick guide to get started with local LLMs using Python, Ollama, and Streamlit.

---

## 📦 Prerequisites

* Python: **3.13.2** or any compatible version.
* Git (for cloning the repository).
* VS Code Installed

---

## 🔁 Clone the Repository

Either run the below command, or directly download and unzip the folder:

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

![image](https://github.com/user-attachments/assets/d4e2e072-5b98-4ac6-9c3a-6a2b28da77ce)

You see this ollama, you  may right click on it, to close it from keep runnning in background.

Run `ollama serve` in a new termnial `cmd`, outside VS code. and keep it like that, dont do anything with that.

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

![Bravo!](https://media.tenor.com/dk14TWjRq5AAAAAM/bravo-gif.gif)         
You did it!!! ✅🎊

---

# Viusalize the vectorstore in 3d

First install `plotly`

```bash
pip install plotly nbformat>=4.2.0
```

Then run the `visual.ipynb` notebook. 

---
When you actually see the vectorstore visually, you be like:<br>
![Bravo!](https://media.tenor.com/swYDigA0_sAAAAAM/reactions.gif)


# Ollama commands to add, remove, stop, run... models

| Command | Use (Keywords) |
| :-- | :-- |
| `ollama serve` | Start server, enable API |
| `ollama run <model>` | Run model, interact |
| `ollama pull <model>` | Download model |
| `ollama list` | List downloaded models |
| `ollama ps` | Show running models |
| `ollama stop <model>` | Stop running model |
| `ollama rm <model>` | Remove model |
| `ollama show <model>` | Show model details |
| `ollama create <new_model>` | Create custom model |
| `ollama help` | Command help, usage info |
| `ollama --version` | Show Ollama version |

These commands form the foundation for managing and interacting with models in Ollama via the command line.

---
