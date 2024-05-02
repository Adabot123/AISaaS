import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key=YOUR_GOOGLE_API_KEY)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

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

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1].uri]

def extract_pdf_pages(pathname: str) -> list[str]:
  parts = [f"--- START OF PDF ${pathname} ---"]
  # Add logic to read the PDF and return a list of pages here.
  pages = []
  for index, page in enumerate(pages):
    parts.append(f"--- PAGE {index} ---")
    parts.append(page)
  return parts

convo = model.start_chat(history=[])

def delete_files():
  for uploaded_file in uploaded_files:
    genai.delete_file(name=uploaded_file.name)


#for first message
messages = [
    {'role':'user',
     'parts': ["You are responsible for ensuring that the client asks the supplier for accurate specifications. I will be uploading the purchase agreements by the client and procurement specifications of the industry.As an output, you need to state where corrections or additions need to be made and include that as an email to the client with a deadline for making the right changes. This is your role."]
     },
    {
    "role": "user",
    "parts": extract_pdf_pages("/Quality Reqs for Control Valves - S-729Qv2022-05.pdf") #replace it with the path name of your uploaded file
  },
  {
    "role": "user",
    "parts": extract_pdf_pages("/control-valve-mr--tender-specifications-79649a.pdf")
  },
]
response = model.generate_content(messages)
to_markdown(response.text)

#for follow up message

messages.append({'role':'model',
                 'parts':[response.text]})

messages.append({'role':'user',
                 'parts':["Okay, what are some actuator valve specifications?"]})

response = model.generate_content(messages)

to_markdown(response.text)

#for follow up message

messages.append({'role':'model',
                 'parts':[response.text]})

messages.append({'role':'user',
                 'parts':['What are the specifications required in supplier master information?']})

response = model.generate_content(messages)

to_markdown(response.text)

