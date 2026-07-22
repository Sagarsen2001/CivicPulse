/*
==========================================
CivicPulse - Main JavaScript
==========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    console.log("✅ CivicPulse Loaded Successfully");

    initializeButtons();

    smoothScrolling();

    highlightCurrentPage();

});


/*
==========================================
Button Effects
==========================================
*/

function initializeButtons() {

    const buttons = document.querySelectorAll(".btn");

    buttons.forEach(button => {

        button.addEventListener("mouseenter", function () {

            this.style.transition = "0.3s";

        });

    });

}


/*
==========================================
Smooth Scrolling
==========================================
*/

function smoothScrolling() {

    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {

        link.addEventListener("click", function (event) {

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                event.preventDefault();

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });

}


/*
==========================================
Highlight Current Navigation Link
==========================================
*/

function highlightCurrentPage() {

    const currentPage = window.location.pathname;

    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach(link => {

        if (link.getAttribute("href") === currentPage) {

            link.style.color = "#FFD54F";

            link.style.fontWeight = "bold";

        }

    });

}


/*
==========================================
Future Features
==========================================

Week 3
-------
✓ Login Validation

✓ Register Validation

✓ Password Strength Checker


Week 4
-------
✓ Complaint Form Validation

✓ Image Preview

✓ Character Counter


Week 5
-------
✓ Complaint Search

✓ Complaint Filter

✓ AJAX Requests


Week 6
-------
✓ Dashboard Charts

✓ Status Update

✓ Notifications


Week 7
-------
✓ Admin Panel

✓ Worker Dashboard

✓ Analytics


Week 8
-------
✓ AI Suggestions

✓ Duplicate Complaint Detection

✓ Smart Priority System

*/