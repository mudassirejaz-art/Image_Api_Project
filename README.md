# Image API Project

This project fetches images from the **Pexels API** based on user-selected interests and categories. Users can view, like, save, and download images in a professional dashboard interface.

---

## Features

* Fetch images from Pexels API per selected interests.
* Display images in a clean, responsive dashboard.
* Search bar to filter images.
* Infinite scroll to load more images.
* Like, Save, and Download images.
* Categories listed on the left side for easy navigation.
* Fully dynamic dashboard with real-time image updates.

---

## Tech Stack

* Python 3.12
* FastAPI
* SQLAlchemy (SQLite)
* Jinja2 templates
* HTTPX
* HTML/CSS/JS

---

## Project Structure

Image\_Api\_Project/
│
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── models.py
│   ├── templates/
│   │   ├── select\_interests.html
│   │   └── dashboard.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── db/
│       └── db.sqlite3
│
├── requirements.txt
├── .gitignore
└── README.md

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/mudassirejaz-art/Image_Api_Project.git
cd Image_Api_Project
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup .env file

Create a .env file in the root directory and add your Pexels API key:

```
PEXELS_API_KEY=your_pexels_api_key_here
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the dashboard.

### Usage

* Select your interests on the home page.
* Click Continue to view the dashboard.
* Use the search bar to filter images.
* Scroll down to load more images.
* Like, Save, or Download images using the buttons/icons.

### License

This project is for educational purposes. Feel free to use and modify it for personal projects.
