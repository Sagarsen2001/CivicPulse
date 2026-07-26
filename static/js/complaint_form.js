/*
=========================================
    CivicPulse Complaint Form Validation
=========================================

Author : Sagar Sen
Project : CivicPulse
*/

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("complaintForm");

    if (!form) {

        return;

    }

    form.addEventListener("submit", function (event) {

        const title = document
            .getElementById("title")
            .value
            .trim();

        const category = document
            .getElementById("category")
            .value;

        const severity = document
            .getElementById("severity")
            .value;

        const location = document
            .getElementById("location")
            .value
            .trim();

        const description = document
            .getElementById("description")
            .value
            .trim();

        // ==========================
        // Title Validation
        // ==========================

        if (title.length < 5) {

            alert(

                "Complaint title must contain at least 5 characters."

            );

            event.preventDefault();

            return;

        }

        // ==========================
        // Category Validation
        // ==========================

        if (category === "") {

            alert(

                "Please select a complaint category."

            );

            event.preventDefault();

            return;

        }

        // ==========================
        // Severity Validation
        // ==========================

        if (severity === "") {

            alert(

                "Please select the complaint severity."

            );

            event.preventDefault();

            return;

        }

        // ==========================
        // Location Validation
        // ==========================

        if (location.length < 5) {

            alert(

                "Please enter a valid complaint location."

            );

            event.preventDefault();

            return;

        }

        // ==========================
        // Description Validation
        // ==========================

        if (description.length < 20) {

            alert(

                "Description should contain at least 20 characters."

            );

            event.preventDefault();

            return;

        }

    });

});