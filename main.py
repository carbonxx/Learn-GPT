import openai
import re
from gradio.components import Textbox, HTML
from gradio import Interface

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY"

questions = [
    [
        "History of {} programming language",
        "What is {} programming language?",
        "What are the features of {} programming language?",
    ],
    "PreRequisites for {} programming language?",
    "Requirements for {} programming language?",
    "Installations for {} programming language?",
    "What are the advantages of {} programming language?",
    "What are the applications of {} programming language? (with examples like frameworks, libraries, etc.)",
    "What are the concepts to learn {} programming language?",
    "What are the resources to learn {} programming language? (like courses, video, blogs, etc. links)",
]

infoQuestions = [
    "About {}: ",
    "PreRequisites for {}: ",
    "Requirements for {}: ",
    "Installations for {} programming language?",
    "Advantages of {}: ",
    "Applications of {}: ",
    "Concepts to learn {}: ",
    "Resources to learn {}: ",
]

def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=400,  # Increase the max_tokens value to get a longer response
        temperature=0.7,
        top_p=1.0,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def chatbot_interface(language):
    if language:
        language = language.lower()
        question = "Is {} a programming language? Reply True or False"
        if bool(generate_response(question.format(language))):
            responses = ""
            i = -1
            for question in questions:
                i += 1
                if type(question) == list:
                    responses += f'<p style="font-size: 20px; font-weight: bold;">{infoQuestions[i].format(language)}</p><br>'
                    for q in question:
                        res = re.sub(r"\n", "<br>", generate_response(q.format(language)))
                        responses += f'{res}<br><br>'
                else:
                    res = re.sub(r"\n", "<br>", generate_response(question.format(language)))
                    responses += f'<p style="font-size: 20px; font-weight: bold;">{infoQuestions[i].format(question)}</p><br>{res}<br><br>'
            return responses
        else:
            rs = re.sub(r"\n", "<br>", generate_response(f"What is {language}?"))
            responses = f'The provided input is not a programming language.<br><p style="font-size: 20px; font-weight: bold;">What is {language}</p><br>{rs}'
            return responses
    else:
        return "Please enter the name of a programming language."

# Create a Gradio Component
inputs = Textbox(lines=2, label="Chat with AI")
outputs = HTML(label="Reply")
# Create a Gradio interface
chat_interface = Interface(
    fn=chatbot_interface,
    inputs=inputs, 
    outputs=outputs, 
    title="Programming Language Chatbot",
    description="Enter the name of a programming language.",
    theme="default"
)

chat_interface.queue()
chat_interface.launch(inline=True, share=True)
