// charts.js — builds the dashboard charts using Chart.js

window.addEventListener("load", async () => {
  await buildBarChart();

  // Search button connection
  document.getElementById("searchBtn").onclick = async () => {
    const q = document.getElementById("searchInput").value;
    const res = await apiSearch(q);

    const container = document.getElementById("results");
    container.innerHTML = "";

    res.papers.forEach(p => {
      const div = document.createElement("div");
      div.className = "paper";

      div.innerHTML = `
        <h3>${p.title}</h3>
        <p>${p.journal} — ${p.year}</p>
        <p>${(p.abstract || "").slice(0, 250)}...</p>
        <a href="paper.html?pmid=${p.pmid}">View Paper</a>
        <hr>
      `;

      container.appendChild(div);
    });
  };
});


// ------------------------------
// 📊 Build bar chart
// ------------------------------

async function buildBarChart() {
  const stats = await apiCountByGroup();

  const labels = Object.keys(stats);
  const data = Object.values(stats);

  const ctx = document.getElementById("barChart").getContext("2d");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Number of Papers",
          data: data,
          backgroundColor: "rgba(54, 162, 235, 0.6)"
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}
