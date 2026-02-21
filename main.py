from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rag_pipeline import search_query
from deep_translator import GoogleTranslator

app = FastAPI()

# Mount static folder (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder (HTML)
templates = Jinja2Templates(directory="templates")


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Ask API (Multilingual Version)
@app.post("/ask")
async def ask(query: str = Form(...),
              language: str = Form(...),
              image: UploadFile = File(None)):

    print("Query:", query)
    print("Language:", language)

    if image:
        print("Image received:", image.filename)

    try:
        # Step 1: Translate query to English if needed
        translated_query = query
        if language != "en":
            translated_query = GoogleTranslator(source=language, target="en").translate(query)

        # Step 2: Search using translated query
        results = search_query(translated_query)

        # Step 3: Prepare single answer
        answer = results[0] if results else "No relevant content found."

        # Step 4: Translate answer back to selected language
        if language != "en" and answer != "No relevant content found.":
            answer = GoogleTranslator(source="en", target=language).translate(answer)

        return {"answer": answer}

    except Exception as e:
        print("Error:", e)
        return {"answer": "Sorry, something went wrong."}