document.addEventListener("DOMContentLoaded", function () {
  const subjects = JSON.parse(document.getElementById("subjectData").textContent);
  const scores = JSON.parse(document.getElementById("scoreData").textContent);

  const ctx = document.getElementById("studentChart");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: subjects,
      datasets: [
        {
          label: "Your Scores",
          data: scores,
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.2,
          pointBackgroundColor: "rgb(75, 192, 192)",
          pointRadius: 5,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Score",
          },
        },
      },
    },
  });
});
