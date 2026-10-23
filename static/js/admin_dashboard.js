/*
=========================================
CivicPulse Admin Dashboard JavaScript
=========================================

Handles:
- Complaint status chart
- Complaint category chart
- Dashboard interactions

Author : Sagar Sen
Project: CivicPulse
*/


// =========================================
// Wait For Page To Load
// =========================================

document.addEventListener("DOMContentLoaded", function () {

    initializeStatusChart();

    initializeCategoryChart();

});


// =========================================
// Status Chart
// =========================================

function initializeStatusChart() {

    const canvas =
        document.getElementById("statusChart");

    if (!canvas) {
        return;
    }

    /*
    Data is provided by dashboard.html
    through Jinja variables.
    */

    const labels =
        typeof statusLabels !== "undefined"
            ? statusLabels
            : [];

    const values =
        typeof statusValues !== "undefined"
            ? statusValues
            : [];


    new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: labels,

            datasets: [
                {
                    label: "Complaints",

                    data: values
                }
            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "bottom"
                },

                tooltip: {
                    enabled: true
                }

            }
        }

    });
}


// =========================================
// Category Chart
// =========================================

function initializeCategoryChart() {

    const canvas =
        document.getElementById("categoryChart");

    if (!canvas) {
        return;
    }


    const labels =
        typeof categoryLabels !== "undefined"
            ? categoryLabels
            : [];

    const values =
        typeof categoryValues !== "undefined"
            ? categoryValues
            : [];


    new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [
                {
                    label: "Complaints",

                    data: values
                }
            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0

                    }

                }

            },

            plugins: {

                legend: {
                    display: false
                },

                tooltip: {
                    enabled: true
                }

            }
        }

    });
}