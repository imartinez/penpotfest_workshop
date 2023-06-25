#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All


load_dotenv()


# Load environment variables
models_directory = os.environ.get('MODELS_DIRECTORY')
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')
llm_model_name = os.environ.get('LLM_MODEL_NAME')


def main():
    # Download embeddings model to /models
    print(f"Downloading embeddings model {embeddings_model_name} into {models_directory}")
    HuggingFaceEmbeddings(model_name=embeddings_model_name, cache_folder=models_directory)
    print("Embeddings model downloaded and ready!")

    # Download LLM model
    print(f"Downloading LLM model {llm_model_name} into {models_directory}")
    GPT4All(model=f'./{models_directory}/{llm_model_name}', allow_download=True)
    print("LLM model downloaded and ready!")


if __name__ == "__main__":
    main()