from django.shortcuts import render
import random
from datetime import datetime

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
        'company1_desc': "Bharti Airtel Limited is an Indian multinational telecommunications company based in New Delhi. It operates in 18 countries across South Asia and Africa, as well as the Channel Islands.",
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
