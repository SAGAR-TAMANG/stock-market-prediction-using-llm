from django.shortcuts import render
import random, os, re
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def index(request):
    
    context = {
        'name': 'Upasana',
        'name_full': 'Upasana Das',
        'image': 'upasana.jpg',
        'today_market': round(random.uniform(-50.0, 50.0), 2),
        'today_datetime': datetime.now(),
        'today_date': datetime.now().date(),

        # Company details
        'company1_name': "Airtel",
        'company1_logo': "airtel.jpg",
        'company1_desc': "Bharti Airtel Limited is an Indian multinational telecommunications company based in New Delhi operating in 18 countries across South Asia and Africa, as well as the Channel Islands.",
        'company1_market': round(random.uniform(-50.0, 50.0), 2),

        'company2_name': "Asian Paints",
        'company2_logo': "asian-paints.png",
        'company2_desc': "Asian Paints is India's largest paint company and a major player in the paint industry worldwide.",
        'company2_market': round(random.uniform(-50.0, 50.0), 2),

        'company3_name': "Axis Bank",
        'company3_logo': "axis-bank.png",
        'company3_desc': "Axis Bank is one of the largest private sector banks in India, providing a range of financial services.",
        'company3_market': round(random.uniform(-50.0, 50.0), 2),

        'company4_name': "HDFC",
        'company4_logo': "hdfc.avif",
        'company4_desc': "HDFC Bank is a leading private sector bank in India known for its strong market position and diversified portfolio.",
        'company4_market': round(random.uniform(-50.0, 50.0), 2),

        'company5_name': "Kotak",
        'company5_logo': "kotak.avif",
        'company5_desc': "Kotak Mahindra Bank offers a range of banking products and financial services for corporate and retail customers.",
        'company5_market': round(random.uniform(-50.0, 50.0), 2),

        'company6_name': "HUL",
        'company6_logo': "hul.webp",
        'company6_desc': "Hindustan Unilever Limited is India's largest fast-moving consumer goods company, with numerous household brands.",
        'company6_market': round(random.uniform(-50.0, 50.0), 2),

        'company7_name': "ICICI",
        'company7_logo': "icici.jpg",
        'company7_desc': "ICICI Bank is a major private sector bank in India, with a substantial presence in corporate and retail banking.",
        'company7_market': round(random.uniform(-50.0, 50.0), 2),

        'company8_name': "Infosys",
        'company8_logo': "infosys.gif",
        'company8_desc': "Infosys is a global leader in consulting, technology, and outsourcing solutions, headquartered in India.",
        'company8_market': round(random.uniform(-50.0, 50.0), 2),

        'company9_name': "L&T",
        'company9_logo': "l&t.jpg",
        'company9_desc': "Larsen & Toubro is an Indian multinational engaged in engineering, construction, and manufacturing.",
        'company9_market': round(random.uniform(-50.0, 50.0), 2),

        'company10_name': "Reliance",
        'company10_logo': "reliance.jpg",
        'company10_desc': "Reliance Industries is a diversified conglomerate with businesses in energy, petrochemicals, textiles, and telecommunications.",
        'company10_market': round(random.uniform(-50.0, 50.0), 2),
    }
  
    return render(request, 'index.html', context=context)

def prediction(request):
    company_name = request.GET.get('company_name', None)
    context = {'company_name': company_name or "Default Company"}

    if company_name:
        ai_pred = chatTWO(company_name)
        # stock_info = finetune_gpt_data(ai_pred)
        prediction, percentage, description = finetune_gpt_data(ai_pred)
        context = {
            'company_name' : company_name,
            'pred' : prediction,
            'percent': percentage,
            'desc': description,
        }
    else:
        ai_pred = "NIL"
        context = {
            'pred' : "NIL",
            'percent': "NIL",
            'desc': "NIL",
        }

    return render(request, 'prediction.html', context)

import openai
from openai import OpenAI
client = OpenAI()

def chatGPT(company_name):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": 
    #     f"""
    #     I want you to go through the web, newspapers, and everywhere online to predict the stock market of "Airtel" company in India. Give your outputs like this: 

    #     Stock: Airtel
    #     Prediction: Bearish/Bullish
    #     Percentage: Float Value
    #     Short Descriptive Reason: Give a short description from your findings on why you are predictingthis.
    # """},
        {"role": "user", "content": 
        f"""
        I want you to go through the web, newspapers, and everywhere online to predict the stock market of "Airtel" company in India. Give your outputs like this: 

        Stock: Airtel
        Prediction: Bearish/Bullish
        Percentage: Float Value
        Short Descriptive Reason: Give a short description from your findings on why you are predictingthis.
    """},
    ]
    )

    print(completion.choices[0].message)

def chatTWO(company_name):
    # Define the API base URL
    url = 'https://api.two.ai/v2'

    # Create the OpenAI client
    client = OpenAI(base_url=url,
                    api_key=os.environ.get("SUTRA_API_KEY"))

    # Create the chat completion request
    stream = client.chat.completions.create(
        model='sutra-light',
        messages=[{"role": "user", "content": f"""
            I want you to predict the stock market of "{company_name}" company in India. Give your outputs like this: 

            Stock: {company_name}
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

    print("\n################COMPLETE TEXT: \n", complete_text, "################ \n")
    return complete_text


def finetune_gpt_data(text):
    # Define the regex patterns for extraction
    prediction_pattern = r"Prediction:\s*(\w+)"
    percentage_pattern = r"Percentage:\s*([-\d.]+)"
    desc_pattern = r"Short Descriptive Reason:\s*(.+)"

    # Extract information using regex
    prediction_match = re.search(prediction_pattern, text)
    percentage_match = re.search(percentage_pattern, text)
    desc_match = re.search(desc_pattern, text)

    # Get the captured groups or None if not found
    prediction = prediction_match.group(1) if prediction_match else None
    percentage = percentage_match.group(1) if percentage_match else None
    desc = desc_match.group(1) if desc_match else None

    print("\n################SPLIT: \n", prediction, "\n", percentage, "\n", desc, "################ \n")

    return prediction, percentage, desc