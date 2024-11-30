const API_BASE_URL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", function() {
    // Retrieve room data from sessionStorage
    const roomNumber = sessionStorage.getItem('roomNumber');
    const price = sessionStorage.getItem('price');
    const roomId = sessionStorage.getItem('roomId'); // Room ID

    // Populate the form fields with the room data
    document.getElementById('roomNumber').value = roomNumber;
    document.getElementById('price').value = price;

    // Handle the form submission
    const bookingForm = document.getElementById('bookingForm');
    bookingForm.addEventListener('submit', async function(event) {
        event.preventDefault();  // Prevent the default form submission

        const checkinDate = document.getElementById('checkinDate').value;
        const checkoutDate = document.getElementById('checkoutDate').value;
        const guestName = document.getElementById('guestName').value;
        const guestEmail = document.getElementById('guestEmail').value;

        // Validate the form inputs
        if (!checkinDate || !checkoutDate || !guestName || !guestEmail) {
            alert("Please fill out all fields.");
            return;
        }

        const reservationData = {
            room_id: roomId,  // Get RoomID from sessionStorage
            checkin_date: checkinDate,
            checkout_date: checkoutDate,
            guest_name: guestName,
            guest_email: guestEmail,

            price: price,
        };

        try {
            // Send the reservation data to your Flask backend
            const response = await fetch(`${API_BASE_URL}/booking/reservations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reservationData),
            });

            const result = await response.json();
            if (result.success) {
                alert("Room booked successfully!");
                // Optionally redirect to a confirmation page or home
                window.location.href = '/confirmation';  // Assuming a confirmation page exists
            } else {
                alert("Booking failed. Please try again.");
            }
        } catch (error) {
            console.error("Error booking room:", error);
            alert("An error occurred. Please try again later.");
        }
    });
});
