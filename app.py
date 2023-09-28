from flask import Flask, request, jsonify, render_template
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

app = Flask(__name__, template_folder="templates")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

def chat_with_bot(user_message):
    sentence = tokenize(user_message)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.65:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    else:
        return "I do not understand... Try again!"

@app.route('/')
def home():
    return render_template('index_modified.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        chatbot_response = chat_with_bot(user_message)
        return jsonify({"response": chatbot_response})
    else:
        return jsonify({"error": "No message provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
