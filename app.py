from flask import Flask, render_template, request
import google.generativeai as genai
import openai
import os

app = Flask(__name__)

# Set API keys from environment variables
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
openai.api_key = os.environ["OPENAI_API_KEY"]
@app.route('/health')
def health_check():
    return 'Healthy', 200
@app.route('/', methods=['GET', 'POST'])
def index():
    generated_text = None
    error_message = None
    if request.method == 'POST':
        user_input = request.form['prompt']
        api_choice = request.form.get('api_choice', 'gemini')  # Use 'gemini' as default if not provided
        print("User Input:", user_input)  # Debugging: Print the user input
        print("API Choice:", api_choice)  # Debugging: Print the API choice
        
        try:
            if api_choice == 'gemini':
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(user_input)
                generated_text = ""
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        generated_text += part.text + "\n"
            elif api_choice == 'openai':
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=100
                )
                generated_text = response.choices[0].message['content'].strip()
            else:
                error_message = "Invalid API choice."
        except Exception as e:
            error_message = str(e)
        
        # Debugging: Print the generated text to the console
        print("Generated Text:", generated_text)
    
    return render_template('index.html', generated_text=generated_text, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)