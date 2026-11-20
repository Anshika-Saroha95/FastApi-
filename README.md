# Patient Management System

## About the Project
The Patient Management System is a web-based application developed using FastAPI, HTML, and CSS. It helps manage patient records by providing features to add, search, view, and delete patient information.

## Technologies Used
- Python
- FastAPI
- HTML
- CSS
- JSON (Data Storage)

## Features
- Add new patient records.
- View patient details.
- Search patients using their details.
- Delete patient records.
- Calculate Body Mass Index (BMI).
- Display BMI-based health categories.

## Project Structure

```text
FastApi-/
│
├── main.py
├── patient.json
├── requirements.txt
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    └── index.html
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/Anshika-Saroha95/FastApi-.git
```

**2. Navigate to the project directory**

```bash
cd FastApi-
```

**3. Create a virtual environment**

```bash
python -m venv myenv
```

**4. Activate the virtual environment**

Windows:

```bash
myenv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

**6. Run the application**

```bash
uvicorn main:app --reload
```

**7. Open in your browser**

```text
http://127.0.0.1:8000
```

## How It Works
1. The user interacts with the frontend through HTML and CSS.
2. FastAPI handles backend operations and API requests.
3. Patient records are stored in a JSON file.
4. Users can add, search, view, and delete patient records.

## Author

**Anshika Saroha**

GitHub: [Anshika-Saroha95](https://github.com/Anshika-Saroha95)
