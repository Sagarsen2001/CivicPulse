/*
==========================================
CivicPulse Authentication JavaScript
==========================================

Handles client-side validation for
registration and login forms.

Author : Sagar Sen
Project : CivicPulse
*/

document.addEventListener("DOMContentLoaded", function () {

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener("submit", function (event) {

            const fullName = document.getElementById("full_name").value.trim();

            const email = document.getElementById("email").value.trim();

            const phone = document.getElementById("phone_number").value.trim();

            const password = document.getElementById("password").value;

            const confirmPassword = document.getElementById("confirm_password").value;

            // ==========================
            // Full Name
            // ==========================

            if (fullName.length < 3) {

                alert("Full Name must contain at least 3 characters.");

                event.preventDefault();

                return;

            }

            // ==========================
            // Email
            // ==========================

            const emailPattern =
                /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

            if (!emailPattern.test(email)) {

                alert("Please enter a valid email address.");

                event.preventDefault();

                return;

            }

            // ==========================
            // Phone Number
            // ==========================

            const phonePattern = /^[6-9]\d{9}$/;

            if (!phonePattern.test(phone)) {

                alert("Please enter a valid 10-digit phone number.");

                event.preventDefault();

                return;

            }

            // ==========================
            // Password
            // ==========================

            const passwordPattern =
                /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#]).{8,}$/;

            if (!passwordPattern.test(password)) {

                alert(
                    "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character."
                );

                event.preventDefault();

                return;

            }

            // ==========================
            // Confirm Password
            // ==========================

            if (password !== confirmPassword) {

                alert("Passwords do not match.");

                event.preventDefault();

                return;

            }

        });

    }

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {

        loginForm.addEventListener("submit", function (event) {

            const email = document.getElementById("email").value.trim();

            const password = document.getElementById("password").value.trim();

            if (email === "") {

                alert("Email is required.");

                event.preventDefault();

                return;

            }

            if (password === "") {

                alert("Password is required.");

                event.preventDefault();

                return;

            }

        });

    }

});