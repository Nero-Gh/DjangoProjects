const ctx = document.getElementById("myChart");

const renderChart = (data, labels) => {
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datasets: [
        {
          label: "Last 6 months Expenses",
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: true,
      text: "Expenses per category",
    },
  });
};

const getChartData = () => {
  fetch("/expense-category-summary")
    .then((res) => res.json())
    .then((result) => {
      console.log("result", result);
      const category_date = result.expense_category_data;
      const [labels, data] = [
        Object.keys(category_date),
        Object.values(category_date),
      ];

      renderChart([data], [labels]);
    });
};

document.onload = getChartData();
