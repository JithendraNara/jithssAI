from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai
import os

app = Flask(__name__)

# Set API key from environment variables
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
#just a comment
# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Create the database and the db table
with app.app_context():
    db.create_all()

@app.route('/health')
def health_check():
    return 'Healthy', 200

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Save user to the database
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index', name=name, email=email))
    return render_template('home.html')

@app.route('/app', methods=['GET', 'POST'])
def index():
    name = request.args.get('name')
    email = request.args.get('email')
    generated_text = None
    error_message = None
    if request.method == 'POST':
        user_input = request.form['prompt']
        print("User Input:", user_input)  # Debugging: Print the user input
        
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            generated_text = ""
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    generated_text += part.text + "\n"
        except Exception as e:
            error_message = str(e)
        
        # Debugging: Print the generated text to the console
        print("Generated Text:", generated_text)
    
    return render_template('index.html', name=name, email=email, generated_text=generated_text, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
