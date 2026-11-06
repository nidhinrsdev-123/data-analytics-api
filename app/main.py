from fastapi import FastAPI
from app.api.routes import router
from app.core.database import Base,engine
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Data Analytics API",version="1.0.0",description="CSV ingestion and Pandas-powered analytics.")
app.include_router(router)
@app.get("/health",tags=["health"])
def health(): return {"status":"ok"}
