const API_BASE_URL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", function() {
    // Retrieve room data from sessionStorage
    const roomNumber = sessionStorage.getItem('roomNumber');
    const price = sessionStorage.getItem('price');
    const roomId = sessionStorage.getItem('roomId'); // Room ID
    const hotelId = sessionStorage.getItem('hotelID'); 
    const guestId = sessionStorage.getItem('GuestId'); 

    // Format date as mm/dd/yyyy and display in a separate element if needed
    function formatDateForDisplay(dateString) {
        const [year, month, day] = dateString.split('-');
        return `${month}/${day}/${year}`;
    }

    const checkinDate = sessionStorage.getItem('CheckinDate');
    const checkoutDate = sessionStorage.getItem('CheckoutDate');

    // Example usage
    const formattedCheckinDate = formatDateForDisplay(checkinDate);
    const formattedCheckoutDate = formatDateForDisplay(checkoutDate);

    // Display formatted date somewhere on your page
    document.getElementById('checkinDate').value = formattedCheckinDate;
    document.getElementById('checkoutDate').value = formattedCheckoutDate;


    // Populate the form fields with the room data
    document.getElementById('roomNumber').value = roomNumber;
    document.getElementById('price').value = price;

  

    // Handle the form submission
    const bookingForm = document.getElementById('bookingForm');
    bookingForm.addEventListener('submit', async function(event) {
        event.preventDefault();  // Prevent the default form submission


        const guestName = document.getElementById('guestName').value;
        const guestEmail = document.getElementById('guestEmail').value;
        const accommType = document.getElementById('accommodationType').value;
        if(accommType ==  'Bed & Breakfast')
            accommTypeID = 1
        else if(accommType ==  'Full Pension')
            accommTypeID = 2
        else if(accommType ==  'Half Pension')
            accommTypeID = 3
        console.log(accommTypeID)

        baseReservation  = " not defined"
        // Validate the form inputs
        if (!checkinDate || !checkoutDate || !guestName || !guestEmail) {
            alert("Please fill out all fields.");
            return;
        }
        const guestData = {
            name: guestName,  // Get RoomID from sessionStorage
            email: guestEmail,
            phone: null,
            guesttypeid: '${1}',
            ssn: null
        };

            // Send the reservation data to your Flask backend
            const response1 = await fetch(`${API_BASE_URL}/booking/guest/insert`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(guestData),
            });
        const guest = await response1.json();
        console.log(guest)

        ///önce guesti guests tableına ekleyip sonra reservation yapmalıyız aksi takdirde forign key ihlali oluyor.
        // çünkü db de  biz reservationdaki guest ıd yi guests deki guest ıd ye bağladık

        const reservationData = {
            room_id: roomId,  // Get RoomID from sessionStorage
            guest_id: guestId ,
            checkin_date: checkinDate,
            checkout_date: checkoutDate,
            base_reservation : baseReservation,
            accommodation_type_id: accommTypeID,
            otel_id: hotelId
        };

        try {
            // Send the reservation data to your Flask backend
            const response2 = await fetch(`${API_BASE_URL}/booking/reservations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reservationData),
            });

            const result = await response2.json();
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
