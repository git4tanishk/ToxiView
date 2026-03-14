const API_BASE = "http://127.0.0.1:8000";

async function apiSearch(q, skip = 0, limit = 50) {
  const res = await fetch(
    `${API_BASE}/papers?q=${encodeURIComponent(q || "")}&skip=${skip}&limit=${limit}`
  );
  return res.json();
}

async function apiGetPaper(pmid) {
  const res = await fetch(`${API_BASE}/papers/${pmid}`);
  return res.json();
}

async function apiCountByGroup() {
  const res = await fetch(`${API_BASE}/stats/count_by_group`);
  return res.json();
}
