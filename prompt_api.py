#!/usr/bin/env python3
from prompt_gen_main import PG_SML
from flask import Flask, request, jsonify
app = Flask(__name__)


CHROMA_DB_PATH = "SML/courses_vector_DB"
# COLLECTION_NAME = "smartlearn_padbrc"
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
chosen_model = 'qwen3'

print("Initializing models and ChromaDB client...")
client, embedding_model = PG_SML.initialise_chromadb_and_embedding_model(chromadb_path = CHROMA_DB_PATH,
                                                                         embed_model_name = EMBEDDING_MODEL_NAME)
print("Initializing completed.")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    question = data.get('question')
    collection_name = data.get('collection_name')
    prompt_type = data.get('prompt_type')
    full_response = data.get('full_response')
    module_name = data.get("module_name")
    if not question or not collection_name:
        return jsonify({"error": "Missing 'question' or 'collection_name' in request"}), 400
    
    try:
        collection = PG_SML.get_collection(client=client, collection_name= collection_name)
    except Exception as e:
        print(f"Error getting collection '{collection_name}': {e}")
        return jsonify({"error": f"Course materials for '{collection_name}' not found."}), 404
    
    if prompt_type == "summ":
        full_response,_ = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type)
 
    print(f"Question: {question}")
    if prompt_type == 'init':
        prompt_to_llm = PG_SML.embed_question_and_retrieves (user_question = question,embedding_model = embedding_model,
                                                            collection = collection,prompt_type = prompt_type, module_name=module_name)
        full_response, answer = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type,prompt_to_llm = prompt_to_llm)
        prompt_type = 'cont'

    elif prompt_type == 'cont':
        prompt_to_llm = PG_SML.embed_question_and_retrieves (user_question = question,embedding_model = embedding_model,
                                                            collection = collection,prompt_type = prompt_type,full_response=full_response, module_name=module_name)
        full_response, answer = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type,prompt_to_llm = prompt_to_llm,full_response_past=full_response)

    elif prompt_type == 'summ':
        prompt_to_llm = PG_SML.embed_question_and_retrieves (user_question = question,embedding_model = embedding_model,
                                                            collection = collection,prompt_type = prompt_type,full_response=full_response, module_name=module_name)
        prompt_type = 'cont'
        full_response, answer = PG_SML.generate_answer(chosen_model = chosen_model,prompt_type=prompt_type,prompt_to_llm = prompt_to_llm,full_response_past=full_response)
            
    token_len = PG_SML.get_string_token_count(full_response = full_response)
    print(f"\n--- End of Response --- Total Token Count: {token_len} \n")
    if token_len >= 30000:
        prompt_type = 'summ'

    return jsonify({"answer": answer,"prompt_type":prompt_type,"full_response":full_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)