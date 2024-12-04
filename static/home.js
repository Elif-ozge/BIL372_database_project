// API Base URL
const API_BASE_URL = "http://127.0.0.1:5000";

// Fetch and display all hotels
async function fetchHotels() {
    try {
        const response = await fetch(`${API_BASE_URL}/hotels`);
        const hotels = await response.json();
        const hotelList = document.getElementById('hotel-list');
        hotelList.innerHTML = ''; // Clear previous content

        hotels.forEach(hotel => {
            const hotelCard = document.createElement('div');
            hotelCard.className = 'hotel-card';
            hotelCard.innerHTML = `
                <h3>${hotel.OtelName}</h3>
                <p>Location: ${hotel.OtelLocation}</p>
                <button onclick="fetchRooms(${hotel.OtelID})">View Rooms</button>
            `;
            hotelList.appendChild(hotelCard);
        });
    } catch (error) {
        console.error("Error fetching hotels:", error);
    }
}

// Fetch and display rooms for a selected hotel
async function fetchRooms(hotelId) {

    const checkinDate = document.getElementById('checkin-date').value;
    const checkoutDate = document.getElementById('checkout-date').value;

    if (!checkinDate || !checkoutDate) {
        alert('Please select both check-in and check-out dates.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/hotels/${hotelId}/rooms/available?checkin_date=${checkinDate}&checkout_date=${checkoutDate}`);
        const rooms = await response.json();

        

        const roomList = document.getElementById('room-list');
        roomList.innerHTML = ''; // Clear previous content

        rooms.forEach(room => {
            console.log(room);
                const roomCard = document.createElement('div');
                roomCard.className = 'room-card';
                roomCard.innerHTML = `
                    <h4>Room Number: ${room.RoomNumber}</h4>
                    <p>Price: $${room.Price}</p>
                    <p>Type: ${room.RoomType}</p>

                `;
                 // Room image
                const roomImage = document.createElement('img');
                if (room.RoomID.startsWith('D')) {
                    roomImage.src = `/static/images/dubai-${room.RoomTypeID + 1}.png`;
                } else if (room.RoomID.startsWith('M')) {
                    roomImage.src = `/static/images/maldives-${room.RoomTypeID + 1}.png`;
                } else if (room.RoomID.startsWith('S')) {
                    roomImage.src = `/static/images/switzerland-${room.RoomTypeID + 1}.png`;
                }
                roomImage.alt = `Image of room ${room.RoomNumber}`;
                roomImage.style.width = '250px'; // Set image width
                roomImage.style.height = 'auto'; // Maintain aspect ratio


                // Create the "Book Now" button dynamically
                const bookNowButton = document.createElement('button');
                bookNowButton.textContent = 'Book Now';
                // Attach an event listener to the button
                bookNowButton.addEventListener('click', function() {
                    redirectToBookingPage(room.RoomID,room.RoomNumber,room.Price, checkinDate, checkoutDate,hotelId); // Call the bookRoom function with the room ID
                });

                roomCard.appendChild(bookNowButton);
                roomCard.appendChild(roomImage);
                roomList.appendChild(roomCard);
        });
    } catch (error) {
        console.error("Error fetching rooms:", error);
    }
}

function redirectToBookingPage(roomId, roomNumber,price, dateCheckin, dateCheckout,hotelId) {
    // Store room details in sessionStorage
    sessionStorage.setItem('roomId', roomId);
    sessionStorage.setItem('roomNumber', roomNumber);
    sessionStorage.setItem('price', price);
    sessionStorage.setItem('CheckinDate', dateCheckin);
    sessionStorage.setItem('CheckoutDate', dateCheckout);
    sessionStorage.setItem('hotelID', hotelId);



    // Redirect to booking page
    window.location.href = '/booking';
}


// Initialize
fetchHotels();
