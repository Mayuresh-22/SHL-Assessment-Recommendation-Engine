from fastapi import FastAPI

from app.services.api.routes import health, recommend


app = FastAPI(title="SHL Assessment Recommendation Engine API", version="1.0.0")

app.include_router(health.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "Welcome to the SHL Assessment Recommendation Engine API built by Mayuresh Choudhary!"}
