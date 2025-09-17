### CM3070 Computer Science Final Project ###

## AI Chatbot Mentor ##

This is an early version of an AI Mentor Chatbot. It's an intelligent helper made to give smart, reliable support to students using the smartlearnsolution.com.au website. The project uses a special method to find and use facts (called Retrieval-Augmented Generation, or RAG) and a system that handles different types of information, all built into a three-part web application.

<img width="599" height="183" alt="image" src="https://github.com/user-attachments/assets/7a078468-72e3-4215-a6dc-1f2d03092d14" />

![image](https://github.com/user-attachments/assets/f58e02a0-4743-4548-a033-245a0868f36f)

<img width="1016" height="860" alt="image" src="https://github.com/user-attachments/assets/863087a0-e533-4511-b6d4-eb979b40767e" />

Watch the project demonstration video [here](https://youtu.be/IZLmP6DjqAc).

## Main Features & What It Does: ##

# 1. System for Bringing in Course Information #

Handles All Kinds of Content: Takes in various course materials, like video lessons, written documents (PDFs), and pictures (PNGs).

Automatic Speech-to-Text: Uses OpenAI's Whisper to turn spoken words from video lessons into text very accurately. Also uses Tesseract OCR to get text from PDFs and images.

Organised Knowledge: Turns all the processed information into a standard, easy-to-use format with lots of helpful details (like where it came from, page numbers, and timings).

Computer-Friendly Storage: Turns bits of text into a special format for computers (called vector embeddings), which are then kept in a database called ChromaDB.

# 2. Smart Answer System (RAG) #

Answers Based on Facts: Puts together a smart language model (LLM) with real, checked facts from the course materials.

Finds the Right Information: When you ask a question, the system finds the most important parts of the course information that relate to it.

Stops Making Things Up: The AI's answers always stick to the facts it finds, making sure they are true and match the course.

Acts Like a Mentor: We've used a clever way to tell the AI how to behave, so its answers are friendly, helpful, and patient, just like a good teacher.

# 3. Three-Part Web Application #

Clear Parts: The system is clearly split into three main parts: what users see (the front-end, made with Node.js/EJS), the web server that keeps track of things (Node.js/Express), and a separate AI helper (Flask/Python).

Easy-to-use Chat Screen: Features a special chat page where you can talk to the AI in real-time. It shows quick messages like "Thinking..." so you know it's working.

Smooth Talking: Uses a smart way for the different parts of the system to communicate quickly and without delays.

# 4. Remembers Past Chats #

Keeps Track of Your Talk: The chatbot remembers what you've talked about, even if you refresh the page or come back later.

Separate Chats for Each User and Course: Your chat history is saved in a database (SQLite). Each chat is found using a unique code for you and the course, so your conversations stay separate and correct.

# 5. Can Handle More Courses #

Can Grow Easily: The system is set up so it's simple to add and look after new courses.

Switches Course Information Automatically: The chatbot automatically brings in the right AI information and facts for each course, depending on which course page you're on.

## What's Used to Make It Work: ##
- Backend (Python)
  
    + Flask: A simple framework for the AI helper part.
      
    + OpenAI Whisper: For turning speech into text.
      
    + pytesseract: A tool to get text from images.
      
    + chromadb: A database for storing special computer-friendly text data.
      
    + Qwen3 (or similar): The main AI language model.
      
    + langchain: A tool to build AI applications.
      
    + sentence-transformers: For turning text into computer-readable formats.
      
    + numpy, torch, transformers: Key tools for machine learning.
      
    + sqlite3: For simple database storage.
      
- Frontend & Web Server (Node.js/JavaScript)
  
    + Node.js: Runs the JavaScript code.
      
    + Express: Helps build the web application.
      
    + EJS: Used to create the web pages.
      
    + better-sqlite3: A fast tool for using SQLite databases with Node.js.
      
    + Axios: For sending and receiving information over the internet.
      
    + showdown: Converts special text (Markdown) into web page format (HTML).
      
    + express-session: Helps manage user sessions on the website.
      
---

## How to Set Up and Run the Project: ##

What you need:

- Python 3 or newer

- Node.js (version 16 or newer) & npm (version 8 or newer)

- Git

# Steps: #

# 1. Copy the project # 

# 2. Install Python Tools: #

python -m venv venv

On Linux/macOS:
source venv/bin/activate

On Windows:
venv\Scripts\activate

pip install -r requirements.txt

# 3. Install Node.js Tools: #

npm install

or 

I used the additional sanitize-html packages.
npm init
npm install --save express express-validator ejs body-parser method-override mysql sqlite3 sanitize-html better-sqlite3 showdown

# 4. Start the AI Helper (Python part): #
Open a new terminal or command prompt, go to the folder where prompt_api.py is, and start it.

(If your virtual environment isn't active) source venv/bin/activate
python prompt_api.py

The AI helper will usually start at http://0.0.0.0:5001.

# 5. Start the Web App (Node.js part): #
Open another new terminal or command prompt, go to the main project folder (where package.json is).
node index.js

The web app will usually start at http://localhost:3000.

You can then visit the chatbot by going to a course page, the login details are username: "admin" and the password: "admin".

* NodeJS 
    - follow the install instructions at https://nodejs.org/en/
    - we recommend using the latest LTS version
* Sqlite3 
    - follow the instructions at https://www.tutorialspoint.com/sqlite/sqlite_installation.htm 
    - Note that the latest versions of the Mac OS and Linux come with SQLite pre-installed
* Ollama's Qwen3 model
    - crucial, visit their website to setup the model


