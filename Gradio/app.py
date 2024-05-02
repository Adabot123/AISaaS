import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key='AIzaSyDFpxqmAS4S9Y-ScmuWpHQUeMp16FqI5T8')

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

from pathlib import Path
import hashlib
import google.generativeai as genai

#genai.configure(api_key="YOUR_API_KEY")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

import gradio as gr

theme = gr.themes.Soft(
    primary_hue="cyan",
    neutral_hue="neutral",
    font=[gr.themes.GoogleFont('Poppins'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
)

def input(User_Prompt, Procurement_Specifications, Client_or_Supplier_Data):
    messages = [
      {
          'role':'user',
          'parts': [User_Prompt]
          },
      {
          "role": "user",
          "parts": [Procurement_Specifications]
          },
      {
        "role": "user",
        "parts": [Client_or_Supplier_Data]
      },
    ]
    response = model.generate_content(messages)
    return response.text

desc = "This app **DataBridge** takes *Procurement Specifications and Supplier or Client Data as input* and highlights " \
       "what data is ***missing or inaccurate***, and sends an email to the supplier or client to change it accordingly"

article = "<h3>How to Use:</h3> " \
          "<ul><li>Open the DataBridge app.</li> " \
          "<li>Enter your prompt in the provided input box giving clear instructions.</li>" \
          "<li>Click on the 'Submit' button for your personalized email " \
          "about the corrections you need to make to adhere to the contract.</li></ul>" \
          "Example Prompt: You are responsible for ensuring that the supplier submits accurate specifications." \
          "                I will be uploading the purchase agreements by the client and procurement specifications of the industry." \
          "                As an output, you need to state where corrections or additions need to be made and include that as an email to the supplier. This is your role."



demo = gr.Interface(
    fn=input,
    inputs=['text', 'text', 'text'],
    outputs=["text"],
    theme = theme,
    title = 'DataBridge',
    description = desc,
    article = article
)

demo.launch(share = True)
