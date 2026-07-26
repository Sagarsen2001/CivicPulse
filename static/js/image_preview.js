/*
=========================================
    CivicPulse Image Preview
=========================================

Displays the selected complaint image
before submission.

Author : Sagar Sen
Project : CivicPulse
*/

document.addEventListener("DOMContentLoaded", function () {

    const imageInput = document.getElementById("image");

    const previewImage = document.getElementById("previewImage");

    if (!imageInput || !previewImage) {

        return;

    }

    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {

            previewImage.style.display = "none";

            previewImage.src = "";

            return;

        }

        // ==========================
        // Validate Image Type
        // ==========================

        const allowedTypes = [

            "image/jpeg",

            "image/jpg",

            "image/png",

            "image/webp"

        ];

        if (!allowedTypes.includes(file.type)) {

            alert(

                "Only JPG, JPEG, PNG, and WEBP images are allowed."

            );

            imageInput.value = "";

            previewImage.src = "";

            previewImage.style.display = "none";

            return;

        }

        // ==========================
        // Validate Image Size
        // ==========================

        const maxSize = 5 * 1024 * 1024;

        if (file.size > maxSize) {

            alert(

                "Image size must be less than 5 MB."

            );

            imageInput.value = "";

            previewImage.src = "";

            previewImage.style.display = "none";

            return;

        }

        // ==========================
        // Show Preview
        // ==========================

        const reader = new FileReader();

        reader.onload = function (event) {

            previewImage.src = event.target.result;

            previewImage.style.display = "block";

        };

        reader.readAsDataURL(file);

    });

});