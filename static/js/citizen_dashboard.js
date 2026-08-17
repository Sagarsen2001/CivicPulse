/*
=========================================
CivicPulse Citizen Dashboard JavaScript
=========================================

Handles:
- Complaint search
- Status filtering
- Complaint count updates

Author : Sagar Sen
Project: CivicPulse
*/


document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById(
        "complaintSearch"
    );

    const statusFilter = document.getElementById(
        "statusFilter"
    );

    const complaints = document.querySelectorAll(
        ".complaint-item"
    );

    const visibleCount = document.getElementById(
        "visibleComplaintCount"
    );

    const noResults = document.getElementById(
        "noResults"
    );


    // ==========================================
    // Check Required Elements
    // ==========================================

    if (
        !searchInput ||
        !statusFilter ||
        !visibleCount
    ) {

        return;

    }


    // ==========================================
    // Filter Complaints
    // ==========================================

    function filterComplaints() {

        const searchText = searchInput.value
            .trim()
            .toLowerCase();

        const selectedStatus = statusFilter.value
            .trim()
            .toLowerCase();

        let matchingComplaints = 0;


        complaints.forEach(function (complaint) {

            const complaintStatus =
                (
                    complaint.dataset.status || ""
                ).toLowerCase();

            const complaintSearchText =
                (
                    complaint.dataset.search || ""
                ).toLowerCase();


            // --------------------------------------
            // Search Matching
            // --------------------------------------

            const matchesSearch =
                searchText === "" ||
                complaintSearchText.includes(
                    searchText
                );


            // --------------------------------------
            // Status Matching
            // --------------------------------------

            const matchesStatus =
                selectedStatus === "all" ||
                complaintStatus === selectedStatus;


            // --------------------------------------
            // Show / Hide Complaint
            // --------------------------------------

            if (
                matchesSearch &&
                matchesStatus
            ) {

                complaint.classList.remove(
                    "hidden"
                );

                matchingComplaints++;

            }
            else {

                complaint.classList.add(
                    "hidden"
                );

            }

        });


        // ==========================================
        // Update Visible Count
        // ==========================================

        visibleCount.textContent =
            matchingComplaints;


        // ==========================================
        // Show / Hide No Results
        // ==========================================

        if (noResults) {

            if (matchingComplaints === 0) {

                noResults.style.display = "block";

            }
            else {

                noResults.style.display = "none";

            }

        }

    }


    // ==========================================
    // Search Event
    // ==========================================

    searchInput.addEventListener(
        "input",
        filterComplaints
    );


    // ==========================================
    // Status Filter Event
    // ==========================================

    statusFilter.addEventListener(
        "change",
        filterComplaints
    );


    // ==========================================
    // Initial Filtering
    // ==========================================

    filterComplaints();

});