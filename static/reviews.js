const API_BASE_URL = "http://127.0.0.1:5000";

const reservationId = sessionStorage.getItem('reservationId');
if (reservationId != null) {
    document.getElementById('reservationId').value = reservationId;
    console.log(reservationId)
} else {
    console.error("Reservation ID not found in sessionStorage.");
}    console.log(reservationId)

document.getElementById("review-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const rating = document.getElementById("rating").value;
    const comments = document.getElementById("comments").value;

    const reviewData = {
        reservation_id: reservationId,
        rating: parseInt(rating),
        comment: comments,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/reviews`, { // Backend API for saving the review
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reviewData)
        });

        const result = await response.json();

        if (result.success) {
            document.getElementById("feedback-message").textContent = "Thank you for your feedback!";
            document.getElementById("feedback-message").style.color = "green";
            document.getElementById("feedback-message").style.display = "block";

            // Optionally clear the form
            document.getElementById("review-form").reset();
        } else {
            document.getElementById("feedback-message").textContent = "Failed to submit review. Please try again.";
            document.getElementById("feedback-message").style.color = "red";
            document.getElementById("feedback-message").style.display = "block";
        }
    } catch (error) {
        console.error("Error submitting review:", error);
        document.getElementById("feedback-message").textContent = "An error occurred. Please try again later.";
        document.getElementById("feedback-message").style.color = "red";
        document.getElementById("feedback-message").style.display = "block";
    }
});
