import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
openai.api_key=config["openai_key"]

app = Flask(__name__,
    template_folder='templates'
)

def get_colours(prompt):
    chat = f"""
    You are a colour generating assistant that responds to text prompts for colour palettes.
    The palettes should have between 2 and 6 colours.
    Desired format: One single JSON arrary with hexadecimal colour codes, including the #, and no comments or additional info
    Prompt: {prompt}
    """
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chat,
        max_tokens=512
    )
    
    colours = json.loads(response["choices"][0]["text"])

    return colours

@ app.route('/')
def index():
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Can you give me a single really good idea to make money?",
        max_tokens=512
    )
    return response["choices"][0]["text"]
    # return "<h1>Hello Wuddy!</h1>"
    # return render_template('index.html')

@ app.route("/letitsnow", methods=['POST'])
def palette_prompt(
    # openAI completion call
):
    query = request.form.get('query')
    result = get_colours(query)
    return {"colours": result}
    # return "Le Tits Now!"
    # return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)