from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.api.routes import health, recommend


app = FastAPI(title="SHL Assessment Recommendation Engine API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://mayuresh-shl-assessment-recommendation-frontend.pages.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "Welcome to the SHL Assessment Recommendation Engine API built by Mayuresh Choudhary!"}
