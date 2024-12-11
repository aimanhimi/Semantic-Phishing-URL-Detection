# Phishing URL Detection with Machine Learning
This project implements a machine learning-based approach to detect phishing URLs using semantic URL-based features. It includes a Streamlit interface for visualization and user interaction, allowing you to classify URLs as phishing or legitimate

# Semantic Malicious URL Detector
![image](https://github.com/user-attachments/assets/05afcbee-dd61-47f9-8afe-eb80b05b345e)

---
## Features

The project includes:
- **Semantic URL-Based Model**: Detects domain obfuscation and malicious intent through host analysis. We implement a novel well performing feature: `RatioNLP`.
- **Interactive Interface**: Built with Streamlit for ease of use and visualization.


## Dataset
The model is a tuned Random Forest trained on the PhiUSIIL dataset and an tested on an unrelated dataset  (JISHNU K S KAITHOLIKKAL). 
The training dataset includes:
- **134,850 legitimate URLs** and **100,945 phishing URLs**.
The test dataset includes:
- **345,738 legitimate URLS** and **104.438 phishing URLs**


## How to Run the Semantic Malicious URL Detector

### Prerequisites

1. Ensure **Python 3.8+** is installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the program
1. Open a terminal and navigate to the project directory:
  ```bash
   cd path/to/CASKAGGLE
   ```

2. Run the streamlit app:
```bash
  streamlit run URLdetection.py
```

The application will launch in your browser

## Usage
Enter a URL in the text input box on the application page. Click Submit. The app will classify the URL as phishing or legitimate with a confidence level

## Key results
Ensemble model achieves high classification performance with significant accuracy in phishing URL detection.
Real-time classification through an interactive interface, without relying on external tools nor HTML content.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.


