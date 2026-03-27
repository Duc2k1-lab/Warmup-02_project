const fileInput = document.getElementById("fileInput");
const loadSampleBtn = document.getElementById("loadSampleBtn");
const statusText = document.getElementById("statusText");

const kpiTotal = document.getElementById("kpiTotal");
const kpiCountries = document.getElementById("kpiCountries");
const kpiMovieShare = document.getElementById("kpiMovieShare");
const kpiAvgYear = document.getElementById("kpiAvgYear");

const chartStore = {
  typeChart: null,
  countryChart: null,
  ratingChart: null,
  yearChart: null,
};

const demoData = [
  { type: "TV Show", country: "Brazil", release_year: 2020, rating: "TV-MA" },
  { type: "Movie", country: "India", release_year: 2008, rating: "TV-MA" },
  { type: "Movie", country: "Indonesia", release_year: 2016, rating: "TV-PG" },
  { type: "Movie", country: "United States", release_year: 2019, rating: "R" },
  { type: "TV Show", country: "South Korea", release_year: 2021, rating: "TV-14" },
  { type: "Movie", country: "India", release_year: 2017, rating: "TV-14" },
  { type: "TV Show", country: "Japan", release_year: 2018, rating: "TV-MA" },
  { type: "Movie", country: "United Kingdom", release_year: 2013, rating: "PG-13" },
  { type: "Movie", country: "United States", release_year: 2020, rating: "PG-13" },
  { type: "TV Show", country: "Brazil", release_year: 2022, rating: "TV-MA" },
];

fileInput.addEventListener("change", (event) => {
  const [file] = event.target.files;
  if (!file) return;

  statusText.textContent = "Dang doc file CSV...";
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      const rows = normalizeRows(results.data || []);
      if (rows.length === 0) {
        statusText.textContent = "File khong co du lieu hop le.";
        return;
      }
      statusText.textContent = `Da nap ${rows.length} dong du lieu tu ${file.name}.`;
      renderDashboard(rows);
    },
    error: () => {
      statusText.textContent = "Loi khi doc file CSV.";
    },
  });
});

loadSampleBtn.addEventListener("click", () => {
  statusText.textContent = "Dang su dung du lieu mau.";
  renderDashboard(normalizeRows(demoData));
});

function normalizeRows(rows) {
  return rows
    .map((row) => ({
      type: (row.type || "").toString().trim() || "Unknown",
      country: (row.country || "").toString().trim() || "unknown",
      release_year: Number.parseInt(row.release_year, 10) || null,
      rating: (row.rating || "").toString().trim() || "Unknown",
    }))
    .filter((row) => row.type !== "Unknown" || row.country !== "unknown" || row.release_year !== null);
}

function renderDashboard(rows) {
  const total = rows.length;
  const movieCount = rows.filter((r) => r.type.toLowerCase() === "movie").length;
  const uniqueCountries = new Set(rows.map((r) => r.country)).size;
  const avgYear = computeAverage(rows.map((r) => r.release_year).filter(Boolean));

  kpiTotal.textContent = total.toLocaleString("vi-VN");
  kpiCountries.textContent = uniqueCountries.toLocaleString("vi-VN");
  kpiMovieShare.textContent = `${((movieCount / total) * 100 || 0).toFixed(1)}%`;
  kpiAvgYear.textContent = avgYear ? avgYear.toFixed(0) : "N/A";

  drawBarChart("typeChart", countBy(rows, "type"), "So luong");
  drawBarChart("countryChart", topN(countBy(rows, "country"), 10), "So luong");
  drawBarChart("ratingChart", topN(countBy(rows, "rating"), 10), "So luong");
  drawBarChart("yearChart", topN(sortMapByKey(countBy(rows, "release_year")), 15), "So luong");
}

function countBy(rows, key) {
  const map = new Map();
  rows.forEach((row) => {
    const value = (row[key] ?? "Unknown").toString();
    map.set(value, (map.get(value) || 0) + 1);
  });
  return map;
}

function sortMapByKey(map) {
  return new Map(
    [...map.entries()].sort((a, b) => Number(a[0]) - Number(b[0]))
  );
}

function topN(map, n) {
  return new Map(
    [...map.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, n)
  );
}

function computeAverage(arr) {
  if (!arr.length) return null;
  const sum = arr.reduce((acc, v) => acc + v, 0);
  return sum / arr.length;
}

function drawBarChart(canvasId, dataMap, label) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (chartStore[canvasId]) {
    chartStore[canvasId].destroy();
  }

  chartStore[canvasId] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [...dataMap.keys()],
      datasets: [
        {
          label,
          data: [...dataMap.values()],
          backgroundColor: "rgba(122, 162, 255, 0.7)",
          borderColor: "rgba(122, 162, 255, 1)",
          borderWidth: 1,
          borderRadius: 6,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          ticks: {
            color: "#cdd8ff",
            maxRotation: 45,
            minRotation: 0,
          },
          grid: { color: "rgba(255,255,255,0.08)" },
        },
        y: {
          ticks: {
            color: "#cdd8ff",
          },
          grid: { color: "rgba(255,255,255,0.08)" },
          beginAtZero: true,
        },
      },
    },
  });
}

renderDashboard(normalizeRows(demoData));
