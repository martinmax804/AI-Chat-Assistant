from flask import Flask, render_template, request, jsonify
import aiml
import os

app = Flask(__name__)

# Initialize the AIML kernel once, not every time a message is sent
kernel = aiml.Kernel()

# Load brain file if it exists
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")

@app.route("/")
def index():
    return render_template("chat.html")  # You need a 'templates/chat.html' file

@app.route("/ask", methods=["POST"])
def ask():
    message = request.form.get("messageText", "").strip()

    if not message:
        return jsonify({'status': 'ERROR', 'answer': 'Please send a message.'})

    # Handle special cases
    if message.lower() == "save":
        kernel.saveBrain("bot_brain.brn")
        return jsonify({'status': 'OK', 'answer': 'Brain saved successfully.'})

    # Get response from AIML
    bot_response = kernel.respond(message)
    return jsonify({'status': 'OK', 'answer': bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
