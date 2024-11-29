from datetime import timedelta

import mysql.connector
from faker import Faker
import random

import mysql.connector

"""
    TODO: 
        // burası genel TODO, aklıma gelenleri yazıcam:
        
        - her seferinde kodu çalıştırıp table oluşturduğumuzda rastgelelik olduğu için farklı sayılarda
          dağılmış oda tipleri vs olabiliyor. yani hepimizin bilgisayarındaki database aynı olmaz böyle bir kodu
          ayrı ayrı çalıştırmaya kalktığımızda. bu durum şuanlık sorun teşkil ediyor mu emin değilim tek birinin
          bilgisayarından local olarak demo yapılacak ve teslim edilecekse sorun olmamalı, ama eğer web sitesiyle
          birlikte gerçek zamanlı düzgün erişim istiyorsa hoca bunu güncellememiz gerekebilir. datanın dağılım oranını
          veya direk datalarun sayısını hardcoded olarak verebiliriz. hangisi mantıklı olur şuanlık bilemedim o yüzden 
          böyle bırakıyorum.
          
        - bu sadece table'ları oluşturan kod dosyası, tamamen düzenlendiğinde bir kez çalıştırılıp bırakılacak. kalan
          logici implement etmek için ayrıca bi dosya açarız yine. kalan logicten kastım da yeni rezervasyon durumunda
          table'a yapılacak olan ekleme ve çıkarmalar güncellemeler vs. 
          
        - son aklıma gelen de, projenin readme file'ına, kodu çalıştırmadan önce mysql kurulup hotel_chain diye bir
          schema üretilmesi gerektiğini yazsak iyi olur açık ve net olması için ve hoca denerse sorun çıkmasın en 
          azından her şeyin açıklaması olsun. 
"""



try:
    # try if we can connect the database
    # if can, close the connection immediately, this is just for test purposes
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="***", # append your own password
        database="hotel_chain"
    )
    print("Database connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")


# MySQL veritabanı bağlantısı
conn = mysql.connector.connect(
    host="localhost",      # MySQL sunucu adresi (örneğin: "127.0.0.1")
    user="root",           # MySQL kullanıcı adı
    password="**",   # append your mysql user password
    database="hotel_chain" # Kullanılacak veritabanı adı
)
cursor = conn.cursor()

# Tabloları oluşturma

cursor.execute("""
CREATE TABLE IF NOT EXISTS RoomType (
    RoomTypeID INT PRIMARY KEY,
    Type TEXT,
    Description TEXT,
    MaxOccupancy INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Otel (
    OtelID INT PRIMARY KEY,
    OtelName TEXT,
    OtelLocation TEXT,
    OtelType INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS RoomImages (
    ImgID INT  PRIMARY KEY,
    ImgData TEXT,
    OtelID INT,
    FOREIGN KEY (OtelID) REFERENCES Otel(OtelID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Rooms (
    RoomID VARCHAR(10) PRIMARY KEY,
    RoomNumber INT,
    RoomTypeID INT,
    Price INT,
    Status TINYINT,
    RoomImgID INT,
    OtelID INT,
    FOREIGN KEY (RoomTypeID) REFERENCES RoomType(RoomTypeID),
    FOREIGN KEY (RoomImgID) REFERENCES RoomImages(ImgID),
    FOREIGN KEY (OtelID) REFERENCES Otel(OtelID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS AccommodationType (
    AccommodationTypeID INT PRIMARY KEY,
    Description TEXT,
    Type TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS GuestType (
    GuestTypeID INT PRIMARY KEY,
    Type TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Guests (
    GuestID INT AUTO_INCREMENT  PRIMARY KEY,
    Name TEXT,
    Email TEXT,
    Phone TEXT,
    GuestTypeID INT,
    SSN VARCHAR(11),
    FOREIGN KEY (GuestTypeID) REFERENCES GuestType(GuestTypeID)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Reservations (
    ReservationID INT AUTO_INCREMENT  PRIMARY KEY,
    RoomID VARCHAR(10),
    GuestID INT,
    DateCheckin DATE,
    DateCheckout DATE,
    BaseReservation TEXT,
    AccommodationTypeID INT,
    OtelID INT,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID),
    FOREIGN KEY (AccommodationTypeID) REFERENCES AccommodationType(AccommodationTypeID),
    FOREIGN KEY (OtelID) REFERENCES Otel(OtelID)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Payments (
    PaymentID INT AUTO_INCREMENT  PRIMARY KEY,
    ReservationID INT,
    Amount INT,
    PaymentDate DATE,
    PaymentMethod TEXT,
    Status TINYINT,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Reviews (
    ReviewID INT AUTO_INCREMENT  PRIMARY KEY,
    ReservationID INT,
    Rating INT,
    Comment TEXT,
    ReviewDate DATE,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID)
)
""")

# Faker ile rastgele veri üretimi
faker = Faker()

# Otel verilerini ekleme
otels = [
    (1, "Dubai Luxury", "Dubai", 10),
    (2, "Maldives Paradise", "Maldives", 7),
    (3, "Swiss Comfort", "Switzerland", 8)
]

# distinct valueları insert ediyoruz database'e, aynı olmaların engelleyerek
cursor.executemany("INSERT IGNORE INTO Otel (OtelID, OtelName, OtelLocation, OtelType) VALUES (%s, %s, %s, %s)", otels)
conn.commit()  # commit changes to the database

# RoomType verilerini ekleme
room_types = [
    (1, "Single Room", "A room for single occupancy", 2),
    (2, "Double Room", "A room for double occupancy", 3),
    (3, "Suite", "A luxurious suite", 4)
]
cursor.executemany("INSERT IGNORE INTO RoomType VALUES (%s, %s, %s, %s)", room_types)
conn.commit()  # Commit here


"""
    TODO:
        - gpt'ye random 9 tane oda resmi ürettirilip burda direk image path'i verilecek random resim generate etmek yerine,
        - imagelerı githubda repoya ekleriz zaten, buraya da hardcoded value olarak veririz 
        - şimdilik ellemedim gptye resim ürettirme kısmını, random şuanlık üretiliyor resimler
"""
# RoomImages verilerini ekleme
room_images = []
hotel_ids = [1, 2, 3]  # sırasıyla dubai, maldives, switzerland

for hotel_id in hotel_ids:
    for i in range(3):  # 3 images per hotel
        img_data = faker.file_path(extension="jpg")
        img_id = (hotel_id - 1) * 3 + i  # Generate a unique image ID for each image
        room_images.append((img_id, img_data, hotel_id))  # Add to the list with associated hotel ID

cursor.executemany("INSERT IGNORE INTO RoomImages (ImgID, ImgData, OtelID) VALUES (%s, %s, %s)", room_images)

# Commit the changes to the database
conn.commit()



# Rooms verilerini ekleme
room_count = {
    "Dubai": {"2": 50, "3": 25, "4": 25},
    "Maldives": {"2": 25, "3": 15, "4": 10},
    "Switzerland": {"2": 30, "3": 15, "4": 15}
}
prices = {
    "Dubai": {"2": 300, "3": 450, "4": 550},
    "Maldives": {"2": 120, "3": 210, "4": 300},
    "Switzerland": {"2": 100, "3": 200, "4": 230}
}
otel_ids = {"Dubai": 1, "Maldives": 2, "Switzerland": 3}

room_id_counter = 1
rooms = []

for location, types in room_count.items():
    print(location + "    ")
    for max_occupancy, count in types.items():
        print(max_occupancy + "   ")
        for _ in range(count):
            print(0)
            if(location == "Dubai"):
                room_id = f"D{room_id_counter:03d}"
            elif(location == "Maldives"):
                room_id = f"M{room_id_counter:03d}"
            elif(location == "Switzerland"):
                room_id = f"S{room_id_counter:03d}"
            room_number = random.randint(100, 999)
            room_type_id = int(max_occupancy) -1   # Doğrudan max_occupancy yerine RoomTypeID kullanıyoruz
            if room_type_id not in [1, 2, 3]:  # RoomType tablosunda geçerli olup olmadığını kontrol edin
                continue
            price = prices[location][max_occupancy]
            status = random.choice([0, 1])  # Available or not
            room_img_id = random.randint(0,2)
            otel_id = otel_ids[location]
            rooms.append((room_id, room_number, room_type_id, price, status, room_img_id, otel_id))
            room_id_counter += 1

print(rooms)
cursor.executemany("INSERT INTO Rooms VALUES (%s, %s, %s, %s, %s, %s, %s)", rooms)
conn.commit()  # Commit here



# AccommodationType verilerini ekleme
accommodation_types = [
    (1, "Basic Breakfast", "Bed & Breakfast"),
    (2, "Full Meals Included", "Full Pension"),
    (3, "Half Board", "Half Pension")
]
cursor.executemany("INSERT IGNORE INTO AccommodationType VALUES (%s, %s, %s)", accommodation_types)


# GuestType tablosunu doldur
guest_types = [
    (1, "Foreigner"),
    (2, "Citizen"),
]
cursor.executemany("INSERT IGNORE INTO GuestType (GuestTypeID, Type) VALUES (%s, %s)", guest_types)


# Guests tablosunu doldur

cursor.execute("select count(*)*2 from rooms where roomtypeid=1 and status=1 group by roomtypeid;")
guest_number_1 = cursor.fetchone()[0]
cursor.execute("select count(*)*3 from rooms where roomtypeid=2 and status=1 group by roomtypeid;")
guest_number_2 = cursor.fetchone()[0]
cursor.execute("select count(*)*4 from rooms where roomtypeid=3 and status=1 group by roomtypeid;")
guest_number_3 = cursor.fetchone()[0]

guest_number = guest_number_1 + guest_number_2 + guest_number_3
print(guest_number)
guests = []
for _ in range(guest_number):  # Örnek olarak 100 misafir oluştur
    name = faker.name()               # Rastgele isim
    email = faker.email()             # Rastgele e-posta
    phone = faker.phone_number()      # Rastgele telefon numarası
    guest_type_id = random.choice([1, 2])  # GuestType tablosundan rastgele bir tür
    ssn = faker.ssn()                 # Rastgele sosyal güvenlik numarası
    guests.append((name, email, phone, guest_type_id, ssn))
cursor.executemany(
    """
    INSERT INTO Guests (Name, Email, Phone, GuestTypeID, SSN)
    VALUES (%s, %s, %s, %s, %s)
    """,
    guests
)

# Reservations tablosunu doldur
reservations = []

# Rooms ve Guests tablolarından mevcut ID'leri al
cursor.execute("SELECT RoomID, OtelID FROM Rooms")
rooms = cursor.fetchall()  # RoomID ve OtelID'leri içeren liste
room_ids = [row[0] for row in rooms]
otel_ids = {row[0]: row[1] for row in rooms}  # RoomID'den OtelID'ye harita oluştur

cursor.execute("SELECT GuestID FROM Guests")
guest_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT AccommodationTypeID FROM AccommodationType")
accommodation_type_ids = [row[0] for row in cursor.fetchall()]


cursor.execute("select count(*) from rooms where status=1;") # occupied odaların sayısını tutucaz, rezervasyon sayısı için
reservation_number = cursor.fetchone()[0]

# Rastgele rezervasyonlar oluştur
for _ in range(reservation_number):  # Örnek olarak 100 rezervasyon oluştur
    room_id = random.choice(room_ids)  # Rastgele oda seç
    guest_id = random.choice(guest_ids)  # Rastgele misafir seç
    accommodation_type_id = random.choice(accommodation_type_ids)  # Rastgele konaklama tipi seç

    # RoomID'den OtelID'yi al
    otel_id = otel_ids[room_id]

    # Rastgele giriş ve çıkış tarihleri
    checkin_date = faker.date_between(start_date='-1y', end_date='today')  # Geçen yıldan bugüne kadar rastgele tarih
    checkout_date = checkin_date + timedelta(days=random.randint(1, 14))  # 1-14 gün sonrasına çıkış tarihi

    # Rastgele base reservation metni (örnek veri)
    base_reservation = faker.sentence(nb_words=5)

    reservations.append(
        (room_id, guest_id, checkin_date, checkout_date, base_reservation, accommodation_type_id, otel_id))

# Reservations tablosuna verileri ekle
cursor.executemany(
    """
    INSERT INTO Reservations (RoomID, GuestID, DateCheckin, DateCheckout, BaseReservation, AccommodationTypeID, OtelID)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    reservations
)


# Payments tablosunu doldur
payments = []

# Reservations tablosundan mevcut ReservationID'leri al
cursor.execute("select reservationid, (datecheckout-datecheckin)*price as PaymentAmount, datecheckin from rooms, reservations where rooms.roomid=reservations.roomid order by reservationid;")
reservation_payments = cursor.fetchall()


# Rastgele ödemeler oluştur
for i in range(reservation_number):  # rezervasyon sayısı kadar ödeme olmak zorunda
    reservation_id = reservation_payments[i][0]  # ith rezervasyon id yi al

    amount = reservation_payments[i][1]  # Ödeme miktarı (50-2000 arası)
    payment_date = faker.date_between(start_date='-1y', end_date=reservation_payments[i][2])  # Ödeme tarihi checkin date'ten önce olcak

    # alttakiler random olabilir bişey fark etmiyor
    payment_method = random.choice(["Credit Card", "Cash", "Bank Transfer", "Mobile Payment"])  # Rastgele ödeme yöntemi
    status = random.choice([0, 1])  # Ödeme durumu: 0 = Beklemede, 1 = Tamamlandı

    payments.append((reservation_id, amount, payment_date, payment_method, status))

# Payments tablosuna verileri ekle
cursor.executemany(
    """
    INSERT INTO Payments (ReservationID, Amount, PaymentDate, PaymentMethod, Status)
    VALUES (%s, %s, %s, %s, %s)
    """,
    payments
)
# Commit and close
conn.commit()


# Retrieve ReservationID values from Reservations table
cursor.execute("SELECT ReservationID FROM Reservations")
reservation_ids = [row[0] for row in cursor.fetchall()]

# Generate random reviews
reviews = []
cursor.execute("select min(datecheckin) from reservations;")
min_date = cursor.fetchone()[0] # en erken rezervasyonu tutuyor
for _ in range(50):  # Example: generate 50 reviews sayısı fark etmiyo şuanlık sanırım
    reservation_id = random.choice(reservation_ids)  # Select a random reservation ID
    rating = random.randint(1, 5)  # Generate a random rating between 1 and 5
    comment = faker.sentence(nb_words=10)  # Generate a random comment (a sentence with 10 words)
    review_date = faker.date_between(start_date='-1y', end_date=min_date-timedelta(days=1))  # en erken rezervasyondan önce oluyor ödemeler !!

    reviews.append((reservation_id, rating, comment, review_date))

# Insert random reviews into the Reviews table
cursor.executemany(
    """
    INSERT INTO Reviews (ReservationID, Rating, Comment, ReviewDate)
    VALUES (%s, %s, %s, %s)
    """,
    reviews
)

# Commit changes to the database
conn.commit()

# Close the connection
conn.close()

print("Reviews table populated with random data.")



conn.close()

print("MySQL database tables created and populated with random data.")