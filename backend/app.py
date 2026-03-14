# app.py — FastAPI backend
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import shutil
import os

# FIXED IMPORTS
import database
import models
from ingest import ingest_csv  # FIXED — no dot
from database import engine    # FIXED — no dot

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToxiView API")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/papers")
def list_papers(q: str = None, skip: int = 0, limit: int = 50, db: Session = Depends(database.get_db)):
    query = db.query(models.Paper)

    if q:
        q2 = f"%{q}%"
        query = query.filter(
            models.Paper.title.ilike(q2) |
            models.Paper.abstract.ilike(q2) |
            models.Paper.keyword.ilike(q2)
        )

    total = query.count()
    papers = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "papers": [
            {
                "pmid": p.pmid,
                "title": p.title,
                "abstract": p.abstract,
                "journal": p.journal,
                "year": p.year,
                "keyword": p.keyword,
                "group": p.group,
                "relevance": p.relevance,
            }
            for p in papers
        ],
    }


@app.get("/papers/{pmid}")
def get_paper(pmid: str, db: Session = Depends(database.get_db)):
    p = db.query(models.Paper).filter(models.Paper.pmid == pmid).first()
    if not p:
        raise HTTPException(status_code=404, detail="PMID not found")
    return p


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    tmp_path = f"temp_{file.filename}"

    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    added = ingest_csv(db, tmp_path, group_name=file.filename)
    os.remove(tmp_path)

    return {"added": added}


@app.get("/stats/count_by_group")
def count_by_group(db: Session = Depends(database.get_db)):
    q = db.query(models.Paper.group, func.count(models.Paper.pmid)).group_by(models.Paper.group).all()
    return {g or "unknown": int(c) for g, c in q}
