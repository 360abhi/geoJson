## 🗺️ GeoJSON Test Automation Suite

This repository contains automated test cases for verifying GeoJSON map functionalities such as:

✅ Map loading

✅ Marker placement & deletion

✅ Polygon & Line drawing

✅ Search functionality

✅ Zoom controls

✅ File upload

✅ Property editing

Tests are written in Python (Pytest + Playwright) with reporting via Allure..


## 📦 Setup & Installation

1️⃣ Clone the Repository

git clone https://github.com/360abhi/geoJson.git

cd geoJson

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣Install Playwright Browsers

️playwright install

▶️ Running All Tests at Once and Generate Allure Reports

cd Tests/

pytest --alluredir=../allure-results

cd ..

allure generate allure-results -o allure-report --clean

allure open .\allure-report\

▶️ Running Any One Module

cd Tests/

pytest {testfile} --alluredir=../allure-results

## 📂 Project Structure  

geoJson/

│── Browser/             # BrowserManager class for handling browser, context & page creation

│── Configuration/       # Config variables, constants

│── Data/                # JSON test data files

│── Pages/               # Page Object Model (POM) for Map HomePage

│── Tests/               # Test case files

│── utils/               # Common utilities, validations

│── requirements.txt     # Python dependencies

│── README.md            # Documentation



## Key Validation Points


Map Load Validation → Checks map canvas existence and visibility.

Marker Validation → Ensures marker exists

Delete Marker Validation → Ensures no "Point" node exists in editor.

Line Validation → Verifies "LineString" node presence.

Polygon Validation → Verifies "Polygon" node presence.

Search Validation → Ensures map moves to expected lat/lon after search.

Zoom Validation → Confirms zoom level in URL matches expected.

Property Validation → Compares key/value properties between expected & actual.

Invalid JSON Validation → Verifies error marker appears when an invalid GeoJSON file is uploaded.

**All validations:**

Attach screenshots for visual confirmation.

Attach expected vs actual details as text in Allure.





