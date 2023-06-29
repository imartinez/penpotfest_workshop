# PenpotFest privateGPT workshop
This repo contains a simplified version of the original [privateGPT](https://github.com/imartinez/privateGPT), adapted for PenpotFest workshop. 

## What is privateGTP?

privateGPT is a tool that allows you to ask questions to your documents (for example penpot's user guide) without an internet connection, using the power of LLMs. 100% private, no data leaves your execution environment at any point. You can ingest documents and ask questions without an internet connection!

```
> Question:
Can I use custom fonts in Penpot?

> Answer (took 62.48 s.):
 Yes, you can upload your personal or purchased custom fonts that are not included in the catalog provided by Penpot and use them across files of a team using shared libraries feature as mentioned on step 2 under "Custom Fonts" section. Make sure to read about font licensing beforehand for better understanding rights related with these types of resources according to Terms Of Service.

--

> Question:
Is there a shortcut in Penpot to create a component?

> Answer (took 63.58 s.):
 Yes, you can use Ctrl + K (Windows) or right click and select "Create Component" at the object menu.

--

> Question:
Can I invite my team to use Penpot and collaborate?

> Answer (took 63.84 s.):
 Yes, at Penpot you can create as many teams as you need and be invited to teams owned by others. You have the option of creating a new team or joining an existing one with different groups of people. To do this go to "Team Selector" in your dashboard where you will find options for both inviting members and accepting requests from other users who want to join your team.

```

Built with [LangChain](https://github.com/hwchase17/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Chroma](https://www.trychroma.com/) and [SentenceTransformers](https://www.sbert.net/).

# Before the workshop
Complete the setup and models download ahead of the workshop

## Environment setup
Note: This tool requires a rather powerful CPU and RAM. Old or less powerful computers can take minutes to provide an answer to each question. A Mac M1 2020 with 16GB RAM will provide answers less than a minute. 

Clone this repository and navigate to the privateGPT folder.

Make sure you have Python 3.10 or later installed.

```shell
#Windows
py --version

#Unix/macOS
python3 --version
````

Clone this repository and navigate to its directory.

Create a virtual environment for the project to avoid issues with dependencies:

```shell
#Windows
py -m venv env

#Unix/macOS
python3 -m venv env
````

Activate the virtual environment:

```shell
#Windows
.\env\Scripts\activate

#Unix/macOS
source env/bin/activate
```

Install the requirements in the active virtual environment using pip:

```shell
#Windows
py -m pip install -r requirements.txt

#Unix/macOS
python3 -m pip install -r requirements.txt
```

Important: if you get an error during requirements installation, read the Troubleshooting section at the bottom of this file!

Copy the `example.env` template into `.env`
```shell
cp example.env .env
```

Note: the default LLM model specified in `.env` (`LLM_MODEL_NAME=ggml-gpt4all-j-v1.3-groovy.bin`) is a relatively simple model: good performance on most CPUs but can sometimes hallucinate or provide not great answers. If you are running on a powerful computer, specially on a Mac M1/M2, you can try a way better model by editing `.env` and setting `LLM_MODEL_NAME=nous-hermes-13b.ggmlv3.q4_0.bin`; you'll need to set `MODEL_N_BATCH=1` to make it work. Inference time is higher (~1min/answer on a M1) but the result is on par with GPT3.5!

## Models download
There are two models used in this tool: an embeddings model and a LLM model. 
You'll need around 8GB free space in your local hard drive.

Run the `download_models.py` script. It will download both models to the folder specified in the `MODELS_DIRECTORY` variable in `.env` file (defaults to `./models` directory). It will also validate the models are working:

```shell
#Windows
py download_models.py

#Unix/macOS
python3 download_models.py
```

If you got an output similar to this one, your setup was completed correctly! 

```shell
Downloading embeddings model all-MiniLM-L6-v2 into models
Embeddings model downloaded and ready!
Downloading LLM model ggml-gpt4all-j-v1.3-groovy.bin into models
Found model file at  ./models/ggml-gpt4all-j-v1.3-groovy.bin
gptj_model_load: loading model from './models/ggml-gpt4all-j-v1.3-groovy.bin' - please wait ...
gptj_model_load: n_vocab = 50400
gptj_model_load: n_ctx   = 2048
gptj_model_load: n_embd  = 4096
gptj_model_load: n_head  = 16
gptj_model_load: n_layer = 28
gptj_model_load: n_rot   = 64
gptj_model_load: f16     = 2
gptj_model_load: ggml ctx size = 5401.45 MB
gptj_model_load: kv self size  =  896.00 MB
gptj_model_load: ................................... done
gptj_model_load: model size =  3609.38 MB / num tensors = 285
LLM model downloaded and ready!
```

# During the workshop
We are going to ingest local documents (create embeddings based on those) and ask questions about those in a fully offline environment. 

## 0. Get the environment ready

First of all, make sure you completed the "Before the workshop" steps, and you've activated the virtual environment created during that setup:

```shell
#Windows
.\env\Scripts\activate

#Unix/macOS
source env/bin/activate
```

## 1. Ingesting the documents

![ingest_flow](https://github.com/imartinez/penpotfest_workshop/assets/721666/6663763a-0b25-433b-85cd-e281c200d9fc)

This repo uses a PDF export of [penpot's user guide](https://help.penpot.app/user-guide/) as an example.

If you want to use your own documents, delete all the contents of `source_documents` directory and put any and all your files there instead.

The supported extensions are:

   - `.csv`: CSV,
   - `.docx`: Word Document,
   - `.doc`: Word Document,
   - `.enex`: EverNote,
   - `.eml`: Email,
   - `.epub`: EPub,
   - `.html`: HTML File,
   - `.md`: Markdown,
   - `.msg`: Outlook Message,
   - `.odt`: Open Document Text,
   - `.pdf`: Portable Document Format (PDF),
   - `.pptx` : PowerPoint Document,
   - `.ppt` : PowerPoint Document,
   - `.txt`: Text file (UTF-8),

Run the following command to ingest all the data.

```shell
#Windows
py ingest.py

#Unix/macOS
python3 ingest.py
```

Output should look like this:

```shell
Creating new vectorstore
Loading documents from source_documents
Loading new documents: 100%|██████████████████████| 1/1 [00:01<00:00,  1.73s/it]
Loaded 1 new documents from source_documents
Split into 90 chunks of text (max. 500 tokens each)
Creating embeddings. May take some minutes...
Using embedded DuckDB with persistence: data will be stored in: db
Ingestion complete! You can now run privateGPT.py to query your documents
```

It will create a `db` folder containing the local vectorstore. Will take 20-30 seconds per document, depending on the size of the document.
You can ingest as many documents as you want, and all will be accumulated in the local embeddings database.

Note: Every time you want to start from an empty database, delete the `db` folder.

During the ingest process no data leaves your local environment. You can ingest without an internet connection!

## 2. Ask questions to your documents, locally!

![privateGPT_flow](https://github.com/imartinez/penpotfest_workshop/assets/721666/4bebe9ef-4f36-4e6c-928d-b425c75eee9d)

In order to ask a question, run a command like:

```shell
#Windows
py privateGPT.py

#Unix/macOS
python3 privateGPT.py
```

And wait for the script to require your input.

```plaintext
> Enter a query:
```

Enter your question and hit enter. You'll need to wait 30-60 seconds (depending on your machine, the model you are using, etc.) while the LLM model consumes the prompt and prepares the answer. Once done, it will print the answer and the sources it used as context from your documents; you can then ask another question without re-running the script, just wait for the prompt again.

You could turn off your internet connection, and the script inference would still work. No data gets out of your local environment.

Type `exit` to finish the script.


# How does it work?
Selecting the right local models and the power of `LangChain` you can run the entire pipeline locally, without any data leaving your environment, and with reasonable performance.

- `ingest.py` uses `LangChain` tools to parse the document and create embeddings locally using `HuggingFaceEmbeddings` (`SentenceTransformers`). It then stores the result in a local vector database using `Chroma` vector store.
- `privateGPT.py` uses a local LLM based on `GPT4All-J` or `LlamaCpp` to understand questions and create answers. The context for the answers is extracted from the local vector store using a similarity search to locate the right piece of context from the docs.

# Troubleshooting

## Python Version
To use this software, you must have Python 3.10 or later installed. Earlier versions of Python will not compile.

## ModuleNotFoundError on Windows
Depending on your installation of Python, you may need to use `py` or `python` to run the different scripts. If one of the two fails with `ModuleNotFoundError`, try the other one.

## C++ Compiler
If you encounter an error while building a wheel during the `pip install` process, you may need to install a C++ compiler on your computer.

### For Windows 10/11
To install a C++ compiler on Windows 10/11, follow these steps:

1. Install Visual Studio 2022.
2. Make sure the following components are selected:
   * Universal Windows Platform development
   * C++ CMake tools for Windows
3. Download the MinGW installer from the [MinGW website](https://sourceforge.net/projects/mingw/).
4. Run the installer and select the `gcc` component.

## Mac Running Intel
When running a Mac with Intel hardware (not M1), you may run into _clang: error: the clang compiler does not support '-march=native'_ during pip install.

If so set your archflags during pip install. eg: _ARCHFLAGS="-arch x86_64" pip3 install -r requirements.txt_

# Disclaimer
This is a test project to validate the feasibility of a fully private solution for question answering using LLMs and Vector embeddings. It is not production ready, and it is not meant to be used in production. The models selection is not optimized for performance, but for privacy; but it is possible to use different models and vectorstores to improve performance.
