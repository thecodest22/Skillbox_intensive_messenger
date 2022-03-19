import json
from flask import Flask, render_template, request
from datetime import datetime as dt
from pathlib import Path


app = Flask(__name__)

db_file_path = Path.cwd() / 'database' / 'db.json'

# Reading a message history from the database file
with open(db_file_path, 'rb') as source:
    data = json.load(source)
    messages = data['messages']  # Declare a variable - list of messages (dicts) read


# Save messages from a chat to the JSON-file (database file)
def save_messages():
    with open(db_file_path, 'w') as target_file:
        write_data = {'messages': messages}
        json.dump(write_data, target_file)  # Write messages (messages is a list of dicts)
                                            # to the target file (JSON database file)


# Add a message to the common list
def add_message(text: str, sender: str) -> None:
    new_message = {
        "text": text,
        "sender": sender,
        "time": dt.now().strftime("%d-%m-%Y, %H:%M:%S")
    }
    messages.append(new_message)  # Add new message to the message list
    save_messages()


# Main page
@app.route('/')
def index_page() -> str:
    return 'Greetings!'


# Show all messages in JSON format
@app.route('/get_messages')
def get_messages() -> dict:
    return {'messages': messages}


# Show a chat form
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/send_message')
def send_message() -> None:
    name = request.args['name']
    text = request.args['text']
    add_message(text, name)


app.run()
