import os
import dotenv
from openai import OpenAI

# Load environment variables from .env file
dotenv.load_dotenv()

# Define the API base URL
url = 'https://api.two.ai/v2'

# Create the OpenAI client
client = OpenAI(base_url=url,
                 api_key=os.environ.get("SUTRA_API_KEY"))

# Create the chat completion request
stream = client.chat.completions.create(
    model='sutra-light',
    messages=[{"role": "user", "content": """
        I want you to predict the stock market of "Airtel" company in India. Give your outputs like this: 

        Stock: Boeing
        Prediction: Bearish/Bullish
        Percentage: Float Value
        Short Descriptive Reason: Give a short description from your findings on why you are predicting this.
    """}],
    max_tokens=250,
    temperature=0,
    stream=True  # Use stream=True to receive chunks of data
)

# Initialize an empty string to collect the content
complete_text = ""

# Iterate through the stream to collect output
for chunk in stream:
    if len(chunk.choices) > 0:
        content = chunk.choices[0].delta.content
        finish_reason = chunk.choices[0].finish_reason
        if content:
            complete_text += content  # Concatenate the content to the complete_text variable
            if finish_reason is not None:
                break  # Exit loop if finished

# Now complete_text contains the full response
print("Complete Response:")
print(complete_text)
