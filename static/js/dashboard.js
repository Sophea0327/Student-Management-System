document.addEventListener("DOMContentLoaded", () => {
  // -------------------------------
  // ✅ Utility: Create Chart Function
  // -------------------------------
  const createChart = (ctxId, type, data, options = {}) => {
    const ctx = document.getElementById(ctxId);
    if (!ctx) return console.warn(`⚠️ Canvas ID '${ctxId}' not found.`);
    return new Chart(ctx.getContext("2d"), {
      type,
      data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1000,
          easing: "easeInOutQuart",
        },
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              font: { size: 13 },
              color: "#333",
            },
          },
          tooltip: {
            enabled: true,
            mode: "index",
            intersect: false,
          },
        },
        ...options,
      },
    });
  };

  // -------------------------------
  // ✅ Grade Bar Chart (Average Grade per Class)
  // -------------------------------
  const classNames = JSON.parse(document.getElementById("chartDataClass").textContent);
  const avgGrades = JSON.parse(document.getElementById("chartDataAvg").textContent);

  createChart(
    "gradeChart",
    "bar",
    {
      labels: classNames,
      datasets: [
        {
          label: "Average Grade",
          data: avgGrades,
          backgroundColor: "rgba(54, 162, 235, 0.6)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1.5,
          borderRadius: 8,
          hoverBackgroundColor: "rgba(54, 162, 235, 0.8)",
        },
      ],
    },
    {
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: "Grade (%)",
            font: { size: 14 },
          },
          grid: { color: "rgba(200,200,200,0.2)" },
        },
        x: { grid: { display: false } },
      },
    }
  );

  // -------------------------------
  // ✅ Student Grade Distribution Pie Chart
  // -------------------------------
  const studentLabels = JSON.parse(document.getElementById("chartDataLabels").textContent);
  const studentCounts = JSON.parse(document.getElementById("chartDataCounts").textContent);

  createChart("studentPieChart", "pie", {
    labels: studentLabels,
    datasets: [
      {
        data: studentCounts,
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
        ],
        borderColor: "#fff",
        borderWidth: 2,
        hoverOffset: 10,
      },
    ],
  });
});
