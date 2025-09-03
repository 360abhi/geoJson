🗺️ GeoJSON Test Automation Suite

This repository contains automated test cases for verifying GeoJSON map functionalities such as:

✅ Map loading

✅ Marker placement & deletion

✅ Polygon & Line drawing

✅ Search functionality

✅ Zoom controls

✅ File upload

✅ Property editing

Tests are written in Python (Pytest + Playwright) with reporting via Allure..


📦 Setup & Installation

1️⃣ Clone the Repository

git clone https://github.com/360abhi/geoJson.git

cd geoJson

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣Install Playwright Browsers

️playwright install

▶️ Running All Tests at Once and Generate Allure Reports

cd Tests/

pytest --alluredir=../allure-results --headed

cd ..

allure generate allure-results -o allure-report --clean

allure open .\allure-report\

▶️ Running Any One Module

cd Tests/

pytest {testfile} --alluredir=../allure-results --headed

📂 Project Structure
geoJson/
│── Browser/             # BrowserManager class for handling browser, context & page creation
│── Configuration/       # Config variables, constants
│── Data/                # JSON test data files
│── Pages/               # Page Object Model (POM) for Map HomePage
│── Tests/               # Test case files
│── utils/               # Common utilities, validations
│── requirements.txt     # Python dependencies
│── README.md            # Documentation




