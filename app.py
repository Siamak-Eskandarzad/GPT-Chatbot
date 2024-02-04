from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI GPT-3 API key
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_input = request.form.get('user_input')

        if not user_input:
            raise ValueError("User input is missing")

        # Make a request to ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )

        # Check if the response contains choices and messages
        if 'choices' in response and response['choices']:
            chatbot_response = response['choices'][0].get('message', {}).get('content', '').strip()
            if chatbot_response:
                return jsonify({'response': chatbot_response})

        raise ValueError("Invalid response from OpenAI")

    except ValueError as ve:
        app.logger.error(f"ValueError: {ve}")
        return jsonify({'error': 'Bad Request'}), 400

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
