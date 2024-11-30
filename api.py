from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

# have flask downloaded

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


# Route for the booking page
@app.route('/booking')
def booking():
    return render_template('booking.html')  # Render booking.html

# Database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "***",  # Replace with your MySQL password
    "database": "hotel_chain"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# API Endpoints

# 1. Get all hotels (home page)
@app.route('/hotels', methods=['GET'])
def get_hotels():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Otel")
    hotels = cursor.fetchall()
    conn.close()
    return jsonify(hotels)

# 2. Get rooms by hotel (home page)
@app.route('/hotels/<int:hotel_id>/rooms', methods=['GET'])
def get_rooms_by_hotel(hotel_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Rooms WHERE OtelID = %s"
    cursor.execute(query, (hotel_id,))
    rooms = cursor.fetchall()
    conn.close()
    return jsonify(rooms)

# 3. Make a reservation (booking page)

"""
    TODO:
        - Burda rezervasyon yapıldığında RoomID aracılığıyla room.status=1'e çevirilmeli oda available değil anlamında
        - Payment ile ilişkilendirmemiz gerekecek
        - Yeni rezervasyonda guestid'nin atanması falan lazım guest bilgilerini nasıl aktarıcaz ordan?
"""

@app.route('/booking/reservations', methods=['POST'])
def make_reservation():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO Reservations (RoomID, GuestID, DateCheckin, DateCheckout, BaseReservation, AccommodationTypeID, OtelID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['room_id'], data['guest_id'], data['checkin_date'], data['checkout_date'],
            data['base_reservation'], data['accommodation_type_id'], data['otel_id']
        ))
        conn.commit()
        response = {"message": "Reservation created successfully!", "reservation_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        response = {"error": str(e)}
    finally:
        conn.close()
    return jsonify(response)


# 4. View a guest's reservations
@app.route('/guests/<int:guest_id>/reservations', methods=['GET'])
def get_guest_reservations(guest_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT r.ReservationID, r.RoomID, r.DateCheckin, r.DateCheckout, rt.Type AS RoomType, o.OtelName
    FROM Reservations r
    JOIN Rooms ro ON r.RoomID = ro.RoomID
    JOIN RoomType rt ON ro.RoomTypeID = rt.RoomTypeID
    JOIN Otel o ON r.OtelID = o.OtelID
    WHERE r.GuestID = %s
    """
    cursor.execute(query, (guest_id,))
    reservations = cursor.fetchall()
    conn.close()
    return jsonify(reservations)

# 5. Cancel a reservation
"""
    TODO:
        - rezervasyon silindiğinde payment bilgisi vardıysa onun da silinmesi lazım
        - aynı zamanda rezerve edilmiş olan odanın tekrar status=0 yani müsait olarak güncellenmesi lazım
"""
@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM Reservations WHERE ReservationID = %s"
        cursor.execute(query, (reservation_id,))
        conn.commit()
        response = {"message": "Reservation canceled successfully!"}
    except Exception as e:
        conn.rollback()
        response = {"error": str(e)}
    finally:
        conn.close()
    return jsonify(response)

# 6. Get available rooms for a date range
@app.route('/rooms/availability', methods=['GET'])
def check_room_availability():
    checkin_date = request.args.get('checkin_date')
    checkout_date = request.args.get('checkout_date')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT r.RoomID, r.RoomNumber, rt.Type AS RoomType, r.Price
    FROM Rooms r
    JOIN RoomType rt ON r.RoomTypeID = rt.RoomTypeID
    WHERE r.Status = 1 AND r.RoomID NOT IN (
        SELECT RoomID FROM Reservations
        WHERE DateCheckin < %s AND DateCheckout > %s
    )
    """
    cursor.execute(query, (checkout_date, checkin_date))
    available_rooms = cursor.fetchall()
    conn.close()
    return jsonify(available_rooms)

# 7. Submit a review

"""
    TODO:
        - burda yine insert işlemi için reservationid rating comment reviewdate gibi bilgilerin frontend'den çekilmesi
        lazım, tam olarak nasıl implement edilir bu kısıma emin değilim.
"""
@app.route('/reviews', methods=['POST'])
def submit_review():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO Reviews (ReservationID, Rating, Comment, ReviewDate)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['reservation_id'], data['rating'], data['comment'], data['review_date']
        ))
        conn.commit()
        response = {"message": "Review submitted successfully!", "review_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        response = {"error": str(e)}
    finally:
        conn.close()
    return jsonify(response)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
