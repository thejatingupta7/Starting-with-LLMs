ENIRONMENT SETUP --------------------------------------

PS D:\jatin_\RAG_MED_LM> python -m venv myenv
PS D:\jatin_\RAG_MED_LM> myenv\Scripts\activate

if using GPU:
    pip install torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/cu118
    (myenv) PS D:\jatin_\RAG_MED_LM> pip install ollama transformers datasets scikit-learn ipykernel faiss-cpu hf-xet langchain langchain-community sentence-transformers openpyxl

if using CPU:
    (myenv) PS D:\jatin_\RAG_MED_LM> pip install ollama torch transformers datasets scikit-learn ipykernel faiss-cpu hf-xet langchain langchain-community sentence-transformers openpyxl

DATA PROCESSING ----------------------------------------

DOWNLOAD THE NECESSARY DATA FOR PUBMEDQA froim the following github repo: https://github.com/pubmedqa/pubmedqa 
After prcoessimnhg u might get a pqaa_train_set.json, pqaa_dev_set.json, and test_set.json and test_ground_truth.json.
Move them to this 'Model_Q/temp_data' directory.

Go to 'Model_Q/vectorize_data.ipynb' file 
& run it to prcoess and generate vectorstores for these 3 datasets:
    1. MED-QA
    2. MED-MCQA
    3. PUBMEDQA

now the corresponsing vectorstoires are present in those 3 folders, now you may delete the temp_data folder

DOWNLOAD BASE LLM --------------------------------------

For base quantized model go to, Ollama 'https://ollama.com' and download Ollama for your device
Make sure the ollama app is installed in the same directory as the code/venv exists like `.\OllamaSetup.exe /DIR="D:\Ollama"`



then run the command in your commandline to pull the base quanitzed model: 'ollama pull llama3.1:8b'


TESTING THE LLM --------------------------------------

1. For testing proceed with the `test.ipynb` file, and run it. It will take hours to test and collect responses.
2. Use the regex code `regex.ipynb` to extract results into a format and find accuracy.


RESULTS ----------------------------------------------

Model_1
    MEDQA       ✅ Accuracy: 62.22% (792 out of 1273 correct)
    MEDMCQA     🔄 Accuracy: XX.XX% 
    PUBMEDQA    ✅ Accuracy: 38.20% (191 out of 500 correct)

Model_2
    MEDQA       ✅ Accuracy: XX.XX%
    MEDMCQA     🔄 Accuracy: XX.XX% 
    PUBMEDQA    ✅ Accuracy: XX.XX%

---
