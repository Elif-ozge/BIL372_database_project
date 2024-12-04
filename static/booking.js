const API_BASE_URL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", function() {
    // Retrieve room data from sessionStorage
    const roomNumber = sessionStorage.getItem('roomNumber');
    const price = sessionStorage.getItem('price');
    const roomId = sessionStorage.getItem('roomId'); // Room ID
    const hotelId = sessionStorage.getItem('hotelID'); 

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

    function calculateTotalPrice() {
        const pricePerNight = parseFloat(sessionStorage.getItem('price'));
        const checkinDate = new Date(sessionStorage.getItem('CheckinDate'));
        const checkoutDate = new Date(sessionStorage.getItem('CheckoutDate'));

        const numberOfNights = Math.round((checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));
        return pricePerNight * numberOfNights;
    }

      // Populate the Total Price field
    const totalPrice = calculateTotalPrice();
    document.getElementById('totalPrice').value = `$${totalPrice.toFixed(2)}`;


    // Handle Payment Method selection
    const paymentMethodSelect = document.getElementById('paymentMethod');
    const cardDetailsDiv = document.getElementById('cardDetails');

    paymentMethodSelect.addEventListener('change', function() {
        if (this.value === "Card") {
            cardDetailsDiv.style.display = "block";
        } else {
            cardDetailsDiv.style.display = "none";
            document.getElementById('cardNumber').value = ""; // Clear the card number field
        }
    });

    // Display formatted date somewhere on your page
    document.getElementById('checkinDate').value = formattedCheckinDate;
    document.getElementById('checkoutDate').value = formattedCheckoutDate;


    // Populate the form fields with the room data
    document.getElementById('roomNumber').value = roomNumber;
    document.getElementById('price').value =  '$' + price;



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

        baseReservation  = " not defined"
        // Validate the form inputs
        if (!checkinDate || !checkoutDate || !guestName || !guestEmail) {
            alert("Please fill out all fields.");
            return;
        }

         // Validation
         const paymentMethod = document.getElementById('paymentMethod').value;
         if (paymentMethod === "Card") {
             const cardNumber = document.getElementById('cardNumber').value;
             if (!/^\d{12}$/.test(cardNumber)) {
                 alert("Please enter a valid 12-digit card number.");
                 return;
             }
         }
        ///önce guesti guests tableına ekleyip sonra reservation yapmalıyız aksi takdirde forign key ihlali oluyor.
        // çünkü db de  biz reservationdaki guest ıd yi guests deki guest ıd ye bağladık

        const response2 = await fetch(`${API_BASE_URL}/booking/guest/id`, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-store', // Instructs the browser not to cache the response
            },
            cache: 'no-store', // Ensures the fetch API bypasses the cache
        });
        
        const last_guest_id = await response2.json();
        guestId = last_guest_id.LastID + 1;



        const reservationData = {
            room_id: roomId,  // Get RoomID from sessionStorage
            guest_id: guestId ,
            checkin_date: checkinDate,
            checkout_date: checkoutDate,
            base_reservation : baseReservation,
            accommodation_type_id: accommTypeID,
            otel_id: hotelId,
            total_price: totalPrice,
            payment_method: paymentMethod
        };

        try {
            const response1 = await fetch(`${API_BASE_URL}/booking/guest/insert?name=${guestName}&email=${guestEmail}&phone=${null}&guesttypeid=${1}&ssn=${null}`, {
                method: 'POST', // Explicitly specify the POST method
            });            
            const guest = await response1.json();
            console.log(guest)
            
            // Send the reservation data to your Flask backend
            const response2 = await fetch(`${API_BASE_URL}/booking/reservations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reservationData),
            });

            const result = await response2.json();
            if (result.success) {
                alert("Room booked successfully!");
                // Store the reservation ID in sessionStorage
                sessionStorage.setItem('reservationId', result.reservation_id);
                console.log(result.reservation_id)
                // Optionally redirect to a review page
                window.location.href = '/reviews'; 
            } else {
                alert("Booking failed. Please try again.");
            }
        } catch (error) {
            console.error("Error booking room:", error);
            alert("An error occurred. Please try again later.");
        }
    });
});
