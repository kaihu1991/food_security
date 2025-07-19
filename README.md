# 🏙️ Mayor and secretary Information Crawler System

A Python-based web scraping project specifically designed to collect public information about mayors from various cities in China. By simulating browser behavior, the crawler extracts structured data such as name, birthdate, resume, education, and more, saving it in an Excel file for further analysis and processing.

---

## 📚 Project Background

Information about mayors is usually scattered across different pages on government websites. Manually collecting this information is inefficient and prone to errors. This project automates the process by simulating browser behavior to collect mayor data efficiently. The scraped data is ready for analysis, research, and reference purposes.

---

## ⚙️ Technology Stack & Dependencies

- **Programming Language**: Python 3.7+
- **Core Libraries**:
  - `selenium`: Simulates a browser and controls page behavior
  - `pandas`: For data processing and saving data into Excel files
  - `beautifulsoup4`: For parsing HTML content from web pages
  - `tqdm`: Displays a progress bar in the terminal/console

---

## 🛠 Environment Setup

### 1. Install Python Dependencies

    Make sure you are in the project directory, then run the following command to install the dependencies:

bash
`pip install -r requirements.txt`




###  2. Set Up ChromeDrive
This script relies on ChromeDriver to control the browser. Please follow these steps:

Install the latest version of Google Chrome (available at https://www.google.com/chrome/).

Download the ChromeDriver that matches your installed version of Chrome (from https://sites.google.com/chromium.org/driver/).


🚀 How to Run
    Open your terminal/command line and navigate to the project directory

    Run the following command:
secretary
`cd ~\mayor_secretary_git\spider\Baidu_baike\secretary`
mayor
`cd ~\mayor_secretary_git\spider\Baidu_baike\mayor`

bash
`python main.py`

The program will automatically:

    Launch a browser (with hidden control prompts)

    Access mayor profile pages

    Extract information fields

    Save the data to output.xlsx or the specified file path



Project Structure

mayor-secretary/
├── spider/              # Main script: Executes the crawling logic
│ ├── Baidu_baike        # Baidu Baike Crawler Code and data
├── requirements.txt      # Dependency list for the project
└── README.md             # This README file