// data.js
// Contient les fonctions pour manipuler les données

let titles = ["Consommation client et prédiction client",
    "Modèle 1 : Régression linéaire sur peu de données",
    "Modèle 2 : Régression linéaire avec les données boursières",
    "Modèle 3 : Random Forest",
    "Modèle 4 : Gradient Boosting",
    "Modèle 5 : SVM",
    "Modèle 6 : Random Forest avec les données bruités"];

function loadImages(client) {
    let client_modif = client.slice(0, 6) + "_" + client.slice(6,)
    // Charger les images du client depuis le dossier "data"
    var images = [
        `/images/${client_modif}/scatter_corr.png`,
        `/images/${client_modif}/corr.png`
    ];

    return images;
}

function displayData(client) {
    let images = loadImages(client);
    // Afficher les images du client
    for (var i = 0; i < images.length; i++) {
        var image = document.getElementById(`image${i}`);
        image.src = images[i];
    }

    for (let i = 0; i < 7; i++) {
        /*
        let chart = document.getElementsByClassName("chart")[i];
        let chartContainer1 = chart.querySelectorAll(".chart-container")[0]
        let chartContainer2 = chart.querySelectorAll(".chart-container")[1]

        // ajout du zoom in / zoom out
        chartContainer1.addEventListener('mouseover', function () {
            this.classList.add('chart-hover');
        });

        chartContainer1.addEventListener('mouseout', function () {
            this.classList.remove('chart-hover');
        });

        chartContainer2.addEventListener('mouseover', function () {
            this.classList.add('chart-hover');
        });

        chartContainer2.addEventListener('mouseout', function () {
            this.classList.remove('chart-hover');
        });

        let div_title = chartContainer1.querySelectorAll(".chart-title")[0];
        div_title.textContent = titles[i];
        */
        if (i == 0) {
            var axis = ["Consommation réelle", "Consommation prédite par le client"];
            plotChart(client, `plot${i}.csv`, `chart${i}`, axis);
        } else {
            var axis = ["Valeur réelle", "Prédiction du modèle"];
            plotChart(client, `plot${i}.csv`, `chart${i}`, axis);
            plotChart_scatter(client, `plot${i}.csv`, `scatter${i}`, axis);
            error_display(client, i);
        }
    }
    results_display(client);
}

function results_display(client) {
    let client_modif = client.slice(0, 6) + "_" + client.slice(6,);
    fetch(`/results/${client_modif}`)
        .then(response => response.json())
        .then(data => {
            const MSE = data.map(entry => entry.MSE);
            const MAE = data.map(entry => entry.MAE);
            const R2 = data.map(entry => entry.R2);

            const maxValues = [
                Math.max(...MSE),
                Math.max(...MAE),
                Math.max(...R2)
            ];

            const normalizedData = [
                MSE.map(value => value / maxValues[0]),
                MAE.map(value => value / maxValues[1]),
                R2.map(value => value / maxValues[2])
            ];

            const ctx1 = document.getElementById('chart-results-mse').getContext('2d');

            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['Données brutes', 'Modèle 1', 'Modèle 2', 'Modèle 3', 'Modèle 4', 'Modèle 5', 'Modèle 6'],
                    datasets: [
                        {
                            label: 'MSE',
                            data: MSE,
                            backgroundColor: 'rgba(255, 99, 132, 0.5)', // Customize the color of the bars
                        }
                    ],
                },
                options: {
                    responsive: true, // Adjust chart responsiveness as per your needs
                    scales: {
                        x: {
                            beginAtZero: true, // Start the x-axis at zero
                        },
                        y: {
                            beginAtZero: true, // Start the y-axis at zero
                        },
                    },
                },
            });

            const ctx2 = document.getElementById('chart-results-mae').getContext('2d');

            new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['Données brutes', 'Modèle 1', 'Modèle 2', 'Modèle 3', 'Modèle 4', 'Modèle 5', 'Modèle 6'],
                    datasets: [
                        {
                            label: 'MAE',
                            data: MAE,
                            backgroundColor: 'rgba(54, 162, 235, 0.5)', // Customize the color of the bars
                        }
                    ],
                },
                options: {
                    responsive: true, // Adjust chart responsiveness as per your needs
                    scales: {
                        x: {
                            beginAtZero: true, // Start the x-axis at zero
                        },
                        y: {
                            beginAtZero: true, // Start the y-axis at zero
                        },
                    },
                },
            });

            const ctx3 = document.getElementById('chart-results-r2').getContext('2d');

            new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: ['Données brutes', 'Modèle 1', 'Modèle 2', 'Modèle 3', 'Modèle 4', 'Modèle 5', 'Modèle 6'],
                    datasets: [
                        {
                            label: 'R2',
                            data: R2,
                            backgroundColor: 'rgba(75, 192, 192, 0.5)', // Customize the color of the bars
                        }
                    ],
                },
                options: {
                    responsive: true, // Adjust chart responsiveness as per your needs
                    scales: {
                        x: {
                            beginAtZero: true, // Start the x-axis at zero
                        },
                        y: {
                            beginAtZero: true, // Start the y-axis at zero
                        },
                    },
                },
            });

            const ctx4 = document.getElementById('chart-results').getContext('2d');

            new Chart(ctx4, {
                type: 'bar',
                data: {
                    labels: ['Données brutes', 'Modèle 1', 'Modèle 2', 'Modèle 3', 'Modèle 4', 'Modèle 5', 'Modèle 6'],
                    datasets: [
                        {
                            label: 'MSE',
                            data: normalizedData[0],
                            backgroundColor: 'rgba(255, 99, 132, 0.5)', // Customize the color of the bars
                        },
                        {
                            label: 'MAE',
                            data: normalizedData[1],
                            backgroundColor: 'rgba(54, 162, 235, 0.5)', // Customize the color of the bars
                        },
                        {
                            label: 'R2',
                            data: normalizedData[2],
                            backgroundColor: 'rgba(75, 192, 192, 0.5)', // Customize the color of the bars
                        },
                    ],
                },
                options: {
                    responsive: true, // Adjust chart responsiveness as per your needs
                    scales: {
                        x: {
                            beginAtZero: true, // Start the x-axis at zero
                        },
                        y: {
                            beginAtZero: true, // Start the y-axis at zero
                        },
                    },
                },
            });

        });
}

function error_display(client, num) {
    let client_modif = client.slice(0, 6) + "_" + client.slice(6,);
    fetch(`/results/${client_modif}`)
        .then(response => response.json())
        .then(data => {
            const MSE = data.map(entry => entry.MSE);
            const MAE = data.map(entry => entry.MAE);
            const R2 = data.map(entry => entry.R2);
            let crossVal = data.map(entry => entry.crossVal);
            crossVal = parseListFloat(crossVal[num]);

            let error = document.getElementById(`error${num}`);
            error.innerHTML = `MSE : ${MSE[num]} <br /> MAE : ${MAE[num]} <br /> R2 : ${R2[num]} <br /> Validation Croisée : ${crossVal.join(", ")}`;
        })
}

function plotChart(client, file, id, axis) {
    let client_modif = client.slice(0, 6) + "_" + client.slice(6,)
    fetch(`/data/${client_modif}/${file}`)
        .then(response => response.json())
        .then(data => {
            const chartLabels = data.map(entry => entry.time);
            const y1 = data.map(entry => entry.y1);
            const y2 = data.map(entry => entry.y2);

            const ctx = document.getElementById(id).getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartLabels,
                    datasets: [
                        {
                            label: axis[0],
                            data: y1,
                            borderColor: 'red',
                            fill: false
                        },
                        {
                            label: axis[1],
                            data: y2,
                            borderColor: 'blue',
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        zoom: {
                            zoom: {
                                enabled: true,
                                mode: 'xy',
                                drag: {
                                    borderColor: 'rgba(225,225,225,0.3)',
                                    borderWidth: 5,
                                    backgroundColor: 'rgb(225,225,225)',
                                    animationDuration: 0
                                },
                                zoomBox: {
                                    backgroundColor: 'rgba(225,225,225,0.4)',
                                    borderWidth: 1,
                                    borderColor: 'rgba(225,225,225,0.7)',
                                    animationDuration: 0
                                },
                                onZoom: function ({ chart }) {
                                    // Fonction appelée lorsqu'un zoom est effectué
                                    // Ajoutez votre logique personnalisée ici
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Value'
                            }
                        }
                    }
                }
            });
        });
}



function plotChart_scatter(client, file, id, axis) {
    let client_modif = client.slice(0, 6) + "_" + client.slice(6,)
    fetch(`/data/${client_modif}/${file}`)
        .then(response => response.json())
        .then(data => {
            const points = data.map(entry => ({ x: entry.y1, y: entry.y2 }));

            const ctx = document.getElementById(id).getContext('2d');
            new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [
                        {
                            label: 'Scatter Plot',
                            data: points,
                            borderColor: 'blue',
                            backgroundColor: 'blue',
                            pointRadius: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: axis[0]
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: axis[1]
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    var label = context.dataset.label || '';

                                    if (context.parsed.y === context.parsed.x) {
                                        label += ' (Bisecting Line)';
                                    }

                                    return label;
                                }
                            }
                        }
                    },
                    annotation: {
                        annotations: [
                            {
                                type: 'line',
                                drawTime: 'beforeDatasetsDraw',
                                mode: 'horizontal',
                                scaleID: 'y',
                                value: 0,
                                borderColor: 'black',
                                borderWidth: 1
                            },
                            {
                                type: 'line',
                                drawTime: 'beforeDatasetsDraw',
                                mode: 'vertical',
                                scaleID: 'x',
                                value: 0,
                                borderColor: 'black',
                                borderWidth: 1
                            }
                        ]
                    }
                }
            });
        });
}
