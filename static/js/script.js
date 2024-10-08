//Generate the chart for the expenses
fetch('/static/expenses_data.json')
    .then(response => response.json())
    .then(data => {
        let categorySums = getAmounts(data);

        let colors = Array(Object.keys(data).length).fill().map(getRandomColor);

        new Chart("expenses_chart", {
            type: "pie",
            data: {
                labels: Object.keys(categorySums),
                datasets: [{
                    label: 'Expenses in €',
                    backgroundColor: colors,
                    data: Object.values(categorySums)
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Expenses in €"
                }
            }
        });
    })
    .catch(error => console.error('Error:', error));

//Generate the chart for the incomes
fetch('/static/incomes_data.json')
    .then(response => response.json())
    .then(data => {
        let categorySums = getAmounts(data);

        let colors = Array(Object.keys(data).length).fill().map(getRandomColor);

        new Chart("incomes_chart", {
            type: "pie",
            data: {
                labels: Object.keys(categorySums),
                datasets: [{
                    label: 'Incomes in €',
                    backgroundColor: colors,
                    data: Object.values(categorySums)
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Incomes in €"
                }
            }
        });
    })
    .catch(error => console.error('Error:', error));

//Function to get random colors for the pie chart
function getRandomColor() {
    const getByte = () => 95 + Math.round(Math.random() * 160);
    return `rgb(${getByte()},${getByte()},${getByte()})`;
}

//Function to get the amounts of the categories
function getAmounts(data) {
    let categorySums = {};

    for (let key in data) {
        let item = data[key];
        let value = item.amount;

        if (typeof value === 'string') {
            value = parseFloat(value.replace(',', '.'));
        }

        if (isNaN(value)) {
            console.error(`Invalid value for item with id ${key}: ${item.value}`);
            continue;
        }

        if (categorySums[item.category]) {
            categorySums[item.category] += value;
        } else {
            categorySums[item.category] = value;
        }
    }

    return categorySums;
}