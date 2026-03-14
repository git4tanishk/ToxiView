# relevance.py — improved relevance scoring system

FOOD_KEYWORDS = [
    'food', 'edible', 'dietary', 'diet', 'ingestion', 'foodborne',
    'dairy', 'milk', 'meat', 'seafood', 'grain', 'cereal', 'crop',
    'vegetable', 'fruit', 'wheat', 'rice', 'soy', 'maize'
]

TOXICANT_KEYWORDS = [
    'toxic', 'contaminant', 'contamination', 'residue',
    'mycotoxin', 'aflatoxin', 'acrylamide', 'phthalate', 'bisphenol',
    'heavy metal', 'lead', 'cadmium', 'mercury', 'arsenic',
    'pesticide', 'pesticides', 'pollutant', 'paHs', 'benzo[a]pyrene',
    'PFAS', 'microplastic', 'nanoplastic', 'nanoparticle'
]

EXPOSURE_KEYWORDS = [
    'exposure', 'risk', 'toxicity', 'hepatotoxic', 'nephrotoxic',
    'genotoxic', 'cytotoxic', 'oxidative stress', 'cancer risk'
]

def score_text(title: str, abstract: str) -> float:
    """
    Returns a score 0.0 – 1.0 indicating relevance to food toxicants.
    Title is weighted more heavily than abstract.
    """
    t = (title or '').lower()
    a = (abstract or '').lower()

    # Weighted scoring
    score = 0.0

    # FOOD relevance
    if any(w in t for w in FOOD_KEYWORDS): score += 0.40
    if any(w in a for w in FOOD_KEYWORDS): score += 0.20

    # TOXICANT relevance
    if any(w in t for w in TOXICANT_KEYWORDS): score += 0.30
    if any(w in a for w in TOXICANT_KEYWORDS): score += 0.15

    # EXPOSURE relevance
    if any(w in t for w in EXPOSURE_KEYWORDS): score += 0.20
    if any(w in a for w in EXPOSURE_KEYWORDS): score += 0.10

    # Cap score at 1.0
    return float(min(score, 1.0))
