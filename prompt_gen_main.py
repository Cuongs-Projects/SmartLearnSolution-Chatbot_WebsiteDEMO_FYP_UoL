#!/usr/bin/env python3
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json

import ollama

from transformers import AutoTokenizer

import re

import textwrap

# CHROMA_DB_PATH = "SML/PADBRC/PADBRC_vector_DB"
CHROMA_DB_PATH = "SML/courses_vector_DB"
COLLECTION_NAME = "smartlearn_padbrc"
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' # Ensure this is THE SAME model used for ingestion
chosen_model = 'qwen3'

class PG_SML():
    @staticmethod
    def initialise_chromadb_and_embedding_model(chromadb_path,embed_model_name):
        try:
            client = chromadb.PersistentClient(path=chromadb_path,settings=Settings(anonymized_telemetry=False))
            print(f"ChromaDB client initialized. Data will be stored in: {chromadb_path}")
        except Exception as e:
            print(f"Error initializing ChromaDB client: {e}")
            exit()

        try:
            embedding_model = SentenceTransformer(embed_model_name)
            print(f"Embedding model '{embed_model_name}' loaded successfully.")
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            exit()
        
        return client,embedding_model
    
    @staticmethod
    def get_collection(client,collection_name):
        try:
            collection = client.get_collection(name=collection_name)
            print(f"Successfully connected to collection '{collection_name}'.")
            print(f"Total items in collection: {collection.count()}")
            if collection.count() == 0:
                print("Warning: Collection is empty")
                exit()
        except Exception as e:
            print(f"Error getting collection '{collection_name}': {e}")
            print("Ensure the collection name is correct and the DB was populated.")
            exit()
        return collection
    
    @staticmethod
    def embed_question_and_retrieves(instructors,user_question,embedding_model,collection,prompt_type,module_name,num_results_to_fetch = 75,full_response = None):
        try:
            query_embedding = embedding_model.encode(user_question).tolist()
        except Exception as e:
            print(f"Error embedding question: {e}")

        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=num_results_to_fetch,
                include=['documents', 'metadatas', 'distances']
            )
        except Exception as e:
            print(f"Error querying collection: {e}")

        retrieved_documents = results.get('documents', [[]])[0] # Get the list of document texts
        retrieved_metadatas = results.get('metadatas', [[]])[0] # Get the list of metadatas

        if not retrieved_documents:
            print("No relevant documents found in the database for this question.")

        if retrieved_documents:
            context_for_llm = ""
            for j,doc_text in enumerate(retrieved_documents):
                context_for_llm = context_for_llm + doc_text + " |metadate_of_text: " + str(retrieved_metadatas[j]) + "\n\n---\n\n"

            if prompt_type == "init":
                prompt_to_llm =f"""

                ---CONTEXT FOR ANSWERING--- The metadata is important too, look at them closely as well
                {context_for_llm}

                ---STUDENT'S CURRENT QUESTION---
                {user_question}

                You are a teacher for the website "SmartLearnSolution.com".
                Right now, you will be answering the student's question based on the content from course "{module_name}", which is provided as CONTEXT FOR ANSWERING.
                The main instructors of this course are {instructors}.
                Please answer the student question as if you are confident about this knowledge field.
                Your personality is: friendly, helpful, encouraging, and patient. But not too much, be human-like.

                YOUR RULES:
                1.  Your entire response will be based on the "CONTEXT FOR ANSWERING" as much as possible.
                2.  NEVER mention the "CONTEXT FOR ANSWERING" to the student. "CONTEXT FOR ANSWERING" is simply for you and only you to understand, with "CONTEXT FOR ANSWERING" acting like your brain. Use the information within them to answer the question and DO NOT EVEN REFER ABOUT THE CONTEXT TO THE STUDENT EVER OR YOULL DIE.
                3.  Answer the student's question. However, since the conversational medium is word, there might not be enough context for you to know the entire problem. So if there is something missing that crucial to solve this, let the student know and ask them appropriate question.
                4.  If your answer is not "teacher-like", politely say "I'm sorry, I couldn't find specific information on that topic in the course materials."
                5.  Format your answers for clarity using Markdown. Use lists, bold text, and paragraphs to structure your response.

                From this point onward, whatever prompt you receives will be straight from the student.
                """
            elif prompt_type == "cont":
                prompt_to_llm =f"""

                ---CONTEXT FOR ANSWERING--- The metadata is important too, look at them closely as well
                {context_for_llm}

                ---STUDENT'S CURRENT QUESTION---
                {user_question}

                ---CONVERSATION HISTORY--- This is the conversation so far (you dont need to answers the questions found in here. It is for you to reference)
                {full_response}

                You are a teacher for the website "SmartLearnSolution.com".
                Right now, you will be answering the student's question based on the content from course "{module_name}", which is provided as CONTEXT FOR ANSWERING.
                The main instructors of this course are {instructors}.
                Please answer the student question as if you are confident about this knowledge field.
                Your personality is: friendly, helpful, encouraging, and patient. But not too much, be human-like.

                YOUR RULES:
                1.  Your entire response will be based on the "CONTEXT FOR ANSWERING" as much as possible.
                2.  NEVER mention the "CONTEXT FOR ANSWERING" to the student. "CONTEXT FOR ANSWERING" is simply for you and only you to understand, with "CONTEXT FOR ANSWERING" acting like your brain. Use the information within them to answer the question and DO NOT EVEN REFER ABOUT THE CONTEXT TO THE STUDENT EVER OR YOULL DIE.
                3.  Answer the student's question. However, since the conversational medium is word, there might not be enough context for you to know the entire problem. So if there is something missing that crucial to solve this, let the student know and ask them appropriate question.
                4.  If your answer is not "teacher-like", politely say "I'm sorry, I couldn't find specific information on that topic in the course materials."
                5.  Format your answers for clarity using Markdown. Use lists, bold text, and paragraphs to structure your response.
                6.  Refer to the "CONVERSATION HISTORY" to understand the flow of the conversation and avoid repeating information.

                From this point onward, whatever prompt you receives will be straight from the student.
                """
            # elif prompt_type == "summ":
            #     prompt_to_llm = f"""

            #     ---CONTEXT FOR ANSWERING---
            #     {context_for_llm}

            #     ---STUDENT'S CURRENT QUESTION---
            #     {user_question}

            #     ---CONVERSATION HISTORY--- This is the conversation so far (you dont need to answers the questions found in here. It is for you to reference)
            #     {full_response}

            #     You are a teacher for the website "SmartLearnSolution.com".
            #     Right now, you will be answering the students based on the content from module/course "{module_name}", which is provided as CONTEXT FOR ANSWERING.
            #     Please answer the student question as if you are confident about this knowledge field.
            #     Your personality is: friendly, helpful, encouraging, and patient. But not too much, be human-like.

            #     YOUR RULES:
            #     1.  Your entire response will be based on the "CONTEXT FOR ANSWERING" as much as possible.
            #     2.  NEVER mention the "CONTEXT FOR ANSWERING" to the student. "CONTEXT FOR ANSWERING" is simply for you and only you to understand, with "CONTEXT FOR ANSWERING" acting like your brain. Use the information within them to answer the question and DO NOT EVEN REFER ABOUT THE CONTEXT TO THE STUDENT EVER OR YOULL DIE.
            #     3.  Answer the student's question. However, since the conversational medium is word, there might not be enough context for you to know the entire problem. So if there is something missing that crucial to solve this, let the student know and ask them appropriate question.
            #     4.  If your answer is not "teacher-like", politely say "I'm sorry, I couldn't find specific information on that topic in the course materials."
            #     5.  Format your answers for clarity using Markdown. Use lists, bold text, and paragraphs to structure your response.
            #     6.  Refer to the "CONVERSATION HISTORY" to understand the flow of the conversation and avoid repeating information.

            #     From this point onward, whatever prompt you receives will be straight from the student.
            #     """
        
        return prompt_to_llm

    @staticmethod
    def generate_answer(user_question,chosen_model,prompt_type,prompt_to_llm = None,full_response_past = None):
        print("--- LLM Response ---")
        prompt = f""" 
        Instruction: Could you help me summarise a conversation into a compact reference form (max 2000 tokens)? 
        Do keep all technical details, conclusions, user preferences, and any named resources. 
        Do not summarise greetings or unrelated chit-chat. 
        You don't need to answer any questions you sees in the conversation, just purely summarise the conversation so you can refer to it in the future.
        You don't need to provide the token length after your summarisation.
        -----------------------
        The conversation to summerise is this: {full_response_past}

        Please answer in format of (and dont deviate from it):
        1) Key Points Mentioned
        2) Technical Details
        3) User Preference
        4) Named Resources Mentioned

        I REPEAT, NO NEED TO ANSWER ANY QUESTIONS YOU FOUND IN THE CONVERSATION, Thank you.
        """
        answer = ""
        out_of_think = False
        thinking_printed = False
        try:
            if prompt_type == "summ":
                stream = ollama.chat(
                    model=chosen_model,
                    messages=[{'role': 'user', 'content': prompt }],
                    stream=True,
                )
            else:
                stream = ollama.chat(
                    model=chosen_model,
                    messages=[{'role': 'user', 'content': prompt_to_llm }],
                    stream=True,
                )

            if prompt_type == "init" or prompt_type == "summ":
                full_response = ""
            if prompt_type == "cont":
                full_response = full_response_past
                
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    if out_of_think == True:
                        print(chunk['message']['content'], end='', flush=True)
                        answer += chunk['message']['content']
                    else:
                        if thinking_printed == False:
                            print("[thinking...]", flush=True)
                            thinking_printed = True

                    if chunk['message']['content'] == '</think>':
                        out_of_think = True
                    
        except Exception as e:
            print(f"Error with streaming chat API: {e}")
        
        answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)
        full_response += f"---The student's question:{user_question}---"
        full_response += answer
        return full_response, answer

    @staticmethod
    def get_string_token_count(full_response):
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-14B-Chat")
        tokens = tokenizer.encode(full_response)
        return len(tokens)
    
    @staticmethod
    def master_prompt_gen(chromadb_path, embed_model_name,collection_name,chosen_model = 'qwen3'):
        client,embedding_model = PG_SML.initialise_chromadb_and_embedding_model(chromadb_path=chromadb_path,embed_model_name= embed_model_name)
        collection = PG_SML.get_collection(client=client,collection_name=collection_name)
        first = True
        full_response = None
        while True:
            if first:
                prompt_type = 'init'
                first = False

            if prompt_type == "summ":
                full_response,_ = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type)

            
            print("-----------------Please ask a Question----------------------")
            print("Type the following to leave the chatbot: exit\n")
            user_input = input("Enter here: ")
            print("------------------------------------------------------------\n")
            if user_input.lower() == 'exit':
                break
            print(f"Question: {user_input}")
            if prompt_type == 'init':
                prompt_to_llm = PG_SML.embed_question_and_retrieves (user_question = user_input,embedding_model = embedding_model,
                                                            collection = collection,prompt_type = prompt_type)
                full_response,_ = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type,prompt_to_llm = prompt_to_llm)
                prompt_type = 'cont'

            elif prompt_type == 'cont':
                prompt_to_llm = PG_SML.embed_question_and_retrieves (user_question = user_input,embedding_model = embedding_model,
                                                            collection = collection,prompt_type = prompt_type,full_response=full_response)
                full_response,_ = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type,prompt_to_llm = prompt_to_llm,full_response_past=full_response)

            elif prompt_type == 'summ':
                prompt_to_llm = PG_SML.embed_question_and_retrieves (user_question = user_input,embedding_model = embedding_model,
                                                            collection = collection,prompt_type = prompt_type,full_response=full_response)
                prompt_type = 'cont'
                full_response,_ = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type,prompt_to_llm = prompt_to_llm,full_response_past=full_response)
            
            token_len = PG_SML.get_string_token_count(full_response = full_response)
            print(f"\n--- End of Response --- Total Token Count: {token_len} \n")
            if token_len >= 30000:
                prompt_type = 'summ'

#test questions:
#Who are the instructors for this course? -- test data retrieval
#What are the key stages of a research project? -- test data retrieval
#Thank you so much! But where can I find the document for this topic? -- test metadata
#Cảm ơn bạn, nhưng mục đích chính của chương trình nghiên cứu cơ bản là gì? -- test multilingual
if __name__ == "__main__":
    PG_SML.master_prompt_gen(chromadb_path = CHROMA_DB_PATH, embed_model_name = EMBEDDING_MODEL_NAME,
                    collection_name = COLLECTION_NAME)