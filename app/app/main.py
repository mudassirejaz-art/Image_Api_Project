from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import httpx, os
from dotenv import load_dotenv
from .models import SessionLocal, init_db
from .crud import like_image, save_image

# Load .env
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

# Initialize DB
init_db()

# App setup
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home
@app.get("/", response_class=HTMLResponse)
async def select_interests(request: Request):
    return templates.TemplateResponse("select_interests.html", {"request": request})

# Fetch images
async def fetch_pexels_images(category: str, page: int = 1, per_page: int = 50, query: str = None):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query.strip() if query else category.strip(), "per_page": per_page, "page": page}
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(PEXELS_BASE_URL, headers=headers, params=params)
        except httpx.RequestError as e:
            print(f"Request error for {category}: {e}")
            return []

        if resp.status_code != 200:
            print(f"Error fetching {category}: Status {resp.status_code}, Response: {resp.text}")
            return []

        try:
            data = resp.json()
        except Exception as e:
            print(f"JSON decode error for {category}: {e}, Response: {resp.text}")
            return []

        images = []
        for photo in data.get("photos", []):
            images.append({
                "url": photo.get("src", {}).get("medium"),
                "photographer": photo.get("photographer"),
                "download": photo.get("src", {}).get("original"),
                "tags": category
            })
        return images

# Dashboard
@app.post("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, interests: list[str] = Form(...)):
    interests = interests[:5]  # Limit to 5
    all_images = []
    for category in interests:
        imgs = await fetch_pexels_images(category)
        all_images.extend(imgs)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "categories": interests,
        "images": all_images
    })

# Infinite scroll & search
@app.post("/load_more")
async def load_more(request: Request, interests: list[str] = Form(...), page: int = Form(1), search: str = Form(None)):
    images = []
    for category in interests:
        imgs = await fetch_pexels_images(category, page=page, per_page=50, query=search)
        images.extend(imgs)
    return JSONResponse({"images": images})

# Like endpoint
@app.post("/like")
async def like_endpoint(image_url: str = Form(...), db: Session = Depends(get_db)):
    img = like_image(db, image_url)
    return {"status": "liked", "image_url": img.image_url}

# Save endpoint
@app.post("/save")
async def save_endpoint(image_url: str = Form(...), photographer: str = Form(...), db: Session = Depends(get_db)):
    img = save_image(db, image_url, photographer)
    return {"status": "saved", "image_url": img.image_url}

# Proxy download to force download
@app.get("/download")
async def download_image(url: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return StreamingResponse(resp.aiter_bytes(), media_type="application/octet-stream", headers={
            "Content-Disposition": "attachment; filename=image.jpg"
        })
