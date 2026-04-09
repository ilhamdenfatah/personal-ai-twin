from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv('GOOGLE_API_KEY'),
    http_options=types.HttpOptions(api_version='v1')
)

for m in client.models.list():
    print(m.name)

http_options=types.HttpOptions(api_version='v1beta')