# Stock Market Prediction Using LLM

A Django web application that predicts stock market trends for NSE (National Stock Exchange of India) listed companies using large language models.

## Features

- **NSE Stock Support**: Predict trends for any company listed on the National Stock Exchange of India
- **AI-Powered Analysis**: Utilizes TWO AI's SUTRA API for intelligent market predictions
- **Comprehensive Data Retrieval**: Fetches real-time and historical stock data
- **User-Friendly Interface**: Simple company selection and prediction viewing
- **Responsive Design**: Works seamlessly on both desktop and mobile devices

## Demo

<!-- Check out the live demo: [Stock Market Prediction Demo](https://your-demo-link-here.com) -->
The Demo will be available soon.

## Installation

### Prerequisites

- Python 3.8+
- Django 4.0+
- API key for TWO AI's SUTRA API

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/SAGAR-TAMANG/stock-market-prediction-using-llm.git
   cd stock-market-prediction-using-llm
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API key:
   ```
   SUTRA_API_KEY=your_api_key_here
   ```

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

1. Select a company from the NSE listed options
2. View historical stock data for the selected company
3. Generate prediction by clicking "Predict"
4. Review the AI-generated market prediction and analysis
5. Optional: Export or save the prediction for future reference

## Project Structure

```
stock-market-prediction-using-llm/
├── main/               # Main application
│   ├── views.py              # View controllers
│   └── urls.py               # URL configuration
├── templates/            # HTML templates
├── core/         # Project settings
│   ├── settings.py           # Django settings
│   └── urls.py               # Project URL configuration
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables (create this file)
└── README.md                 # This file
```

## Customization

- To modify the appearance, edit the CSS in the HTML templates
- To adjust the prediction algorithm, update the API call in the views.py file
- To add more stock markets beyond NSE, extend the data retrieval functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Styled with [Bootstrap](https://getbootstrap.com/)
- AI-powered by [TWO AI's SUTRA API](https://www.two.ai/sutra)
- Stock data retrieved using the NSE library