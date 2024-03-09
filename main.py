from flask import Flask, render_template, request, redirect, url_for, session
import openai
from gtts import gTTS
from googletrans import Translator

app = Flask(__name__)
app .secret_key = 'your_secret_key'

# Dummy user data for demonstration purposes (replace with a database in a real application)
users = {
    'demo_user': {
        'name': 'Demo User',
        'email': 'demo@example.com',
        'password': 'password123'
    }
}
# Set up OpenAI API credentials
openai.api_key = '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'

# Define the / route to return the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Define the /app1index route for the app1 index page
@app.route("/app1index")
def app1index():
    return render_template("app1index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    if request.method == "POST":
        # Get the message from the POST request
        message = request.json.get("message")
        # Send the message to OpenAI's API and receive the response

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        if completion.choices[0].message is not None:
            return completion.choices[0].message
        else:
            return 'Failed to Generate response!'

    # Handle cases where the method is not allowed
    return "Method Not Allowed", 405

# Other routes from app.py
@app.route('/signin')
def sign():
    return render_template('signin.html')

@app.route('/pricingtable')
def pricingtable():
    try:
        if 'username' in session:
            user = users.get(session['username'])
            if user:
                return render_template('pricingtable.html', user_name=user['name'])
        return redirect(url_for('login'))
    except Exception as e:
        # Log or print the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return 'Internal Server Error'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password:
            session['username'] = email
            return redirect(url_for('pricingtable'))

        return 'Invalid email or password'

    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if email not in users:
        users[email] = {'name': name, 'email': email, 'password': password}
        session['username'] = email
        return redirect(url_for('pricingtable'))

    return 'Email already registered'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/Main')
def Main():
    return render_template('Main.html')

@app.route('/img')
def img():
    return render_template('img.html')

@app.route('/Chatboat')
def Chatboat():
    return render_template('chatboat.html')

@app.route('/pricingtable')
def home1():
    return render_template('pricingtable.html')


@app.route('/transalator')
def transalator():
    return render_template('transalator.html')

@app.route('/delcha')
def Delcha():
    return render_template('delcha.html')

@app.route('/', methods=['POST'])
def convert():
    if request.method == 'POST':
        text = request.form['text']
        language = request.form['language']

        translator = Translator()
        translated_text = translator.translate(text, dest=language).text

        tts = gTTS(translated_text, lang=language)
        tts.save('static/output.mp3')  # Save the generated audio file

        return render_template('transalator.html', text=translated_text, audio_file='static/output.mp3')


if __name__ == '__main__':
    app.run(debug=True)
