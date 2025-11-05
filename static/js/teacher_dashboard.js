document.addEventListener("DOMContentLoaded", function () {
  const classNames = JSON.parse(document.getElementById("classData").textContent);
  const avgScores = JSON.parse(document.getElementById("scoreData").textContent);

  const ctx = document.getElementById("teacherChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: classNames,
      datasets: [
        {
          label: "Average Class Scores",
          data: avgScores,
          backgroundColor: "rgba(54, 162, 235, 0.5)",
          borderColor: "rgb(54, 162, 235)",
          borderWidth: 1,
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
            text: "Average Score",
          },
        },
      },
    },
  });
});
