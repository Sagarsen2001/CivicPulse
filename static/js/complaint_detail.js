/*
=========================================
CivicPulse Complaint Detail JavaScript
=========================================

Handles:
- Complaint ID copy
- Image modal
- Keyboard controls
- Modal close behavior

Author : Sagar Sen
Project: CivicPulse
*/


document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // Complaint ID Copy
    // ==========================================

    const copyButton = document.getElementById(
        "copyComplaintId"
    );

    const complaintIdElement = document.getElementById(
        "complaintId"
    );


    if (
        copyButton &&
        complaintIdElement
    ) {

        copyButton.addEventListener(
            "click",
            async function () {

                const complaintId =
                    complaintIdElement.textContent.trim();

                try {

                    await navigator.clipboard.writeText(
                        complaintId
                    );

                    copyButton.classList.add(
                        "copied"
                    );

                    copyButton.textContent = "✓";

                    copyButton.title =
                        "Complaint ID copied";

                    setTimeout(function () {

                        copyButton.classList.remove(
                            "copied"
                        );

                        copyButton.textContent = "📋";

                        copyButton.title =
                            "Copy Complaint ID";

                    }, 2000);

                }
                catch (error) {

                    // Fallback for browsers that do not
                    // support navigator.clipboard.

                    const textArea =
                        document.createElement("textarea");

                    textArea.value =
                        complaintId;

                    textArea.style.position =
                        "fixed";

                    textArea.style.opacity =
                        "0";

                    document.body.appendChild(
                        textArea
                    );

                    textArea.select();

                    try {

                        document.execCommand(
                            "copy"
                        );

                        copyButton.classList.add(
                            "copied"
                        );

                        copyButton.textContent = "✓";

                        setTimeout(function () {

                            copyButton.classList.remove(
                                "copied"
                            );

                            copyButton.textContent = "📋";

                        }, 2000);

                    }
                    catch (fallbackError) {

                        console.error(
                            "Unable to copy complaint ID:",
                            fallbackError
                        );

                    }

                    document.body.removeChild(
                        textArea
                    );

                }

            }
        );

    }


    // ==========================================
    // Image Modal
    // ==========================================

    const complaintImage =
        document.getElementById(
            "complaintImage"
        );

    const imageModal =
        document.getElementById(
            "imageModal"
        );

    const modalImage =
        document.getElementById(
            "modalImage"
        );

    const closeImageModal =
        document.getElementById(
            "closeImageModal"
        );


    // ==========================================
    // Open Image Modal
    // ==========================================

    if (
        complaintImage &&
        imageModal &&
        modalImage
    ) {

        complaintImage.addEventListener(
            "click",
            function () {

                modalImage.src =
                    complaintImage.src;

                imageModal.style.display =
                    "flex";

                document.body.style.overflow =
                    "hidden";

            }
        );

    }


    // ==========================================
    // Close Modal
    // ==========================================

    function closeModal() {

        if (!imageModal) {

            return;

        }

        imageModal.style.display =
            "none";

        document.body.style.overflow =
            "";

        if (modalImage) {

            modalImage.src =
                "";

        }

    }


    // ==========================================
    // Close Button
    // ==========================================

    if (closeImageModal) {

        closeImageModal.addEventListener(
            "click",
            closeModal
        );

    }


    // ==========================================
    // Close When Clicking Outside Image
    // ==========================================

    if (imageModal) {

        imageModal.addEventListener(
            "click",
            function (event) {

                if (
                    event.target === imageModal
                ) {

                    closeModal();

                }

            }
        );

    }


    // ==========================================
    // Keyboard Support
    // ==========================================

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                imageModal &&
                imageModal.style.display === "flex"
            ) {

                closeModal();

            }

        }
    );

});
