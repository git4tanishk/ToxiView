# ingest.py — import CSVs into the DB

import pandas as pd
import os
from sqlalchemy.orm import Session

# FIXED: no relative imports
import models
import database
from relevance import score_text


def ingest_csv(db: Session, filepath: str, group_name: str = None):
    df = pd.read_csv(filepath)

    expected_cols = ['PMID', 'Title', 'Abstract', 'Journal', 'Year', 'Keyword']

    # Auto-map columns
    col_map = {}
    for c in expected_cols:
        if c in df.columns:
            col_map[c] = c

    # Fallback for weird column names
    for c in df.columns:
        if c.lower() == 'pmid':
            col_map['PMID'] = c
        if c.lower() == 'title':
            col_map['Title'] = c
        if 'abstract' in c.lower():
            col_map['Abstract'] = c
        if 'journal' in c.lower():
            col_map['Journal'] = c
        if 'year' in c.lower():
            col_map['Year'] = c
        if 'keyword' in c.lower():
            col_map['Keyword'] = c

    # FIXED — moved OUT of the loop
    models.Base.metadata.create_all(bind=database.engine)

    added = 0

    for _, row in df.iterrows():
        pmid = str(row.get(col_map.get('PMID', ''), ''))
        if not pmid:
            continue

        # Skip if already in DB
        exists = db.query(models.Paper).filter(models.Paper.pmid == pmid).first()
        if exists:
            continue

        title = row.get(col_map.get('Title', ''), '')
        abstract = row.get(col_map.get('Abstract', ''), '')
        journal = row.get(col_map.get('Journal', ''), '')
        year = row.get(col_map.get('Year', ''), '')
        keyword = row.get(col_map.get('Keyword', ''), '')

        relevance = score_text(title, abstract)

        paper = models.Paper(
            pmid=pmid,
            title=str(title),
            abstract=str(abstract),
            journal=str(journal),
            year=str(year),
            keyword=str(keyword),
            group=group_name or '',
            relevance=relevance
        )

        db.add(paper)
        added += 1

    # FIXED — commit once (faster & correct)
    db.commit()

    return added


if __name__ == '__main__':
    # FIXED import
    from database import SessionLocal

    db = SessionLocal()

    base = os.path.join(os.path.dirname(__file__), '..', 'data')
    for fname in os.listdir(base):
        if fname.lower().endswith('.csv'):
            path = os.path.join(base, fname)
            print('Ingesting', path)
            num = ingest_csv(db, path, group_name=fname)
            print('Added', num)
