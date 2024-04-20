import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from datetime import datetime

class Room(ABC):
    def __init__(self, roomNumber, price):
        self.roomNumber = roomNumber
        self.price = price

    @abstractmethod
    def get_type(self):
        pass

    @property
    def roomNumber(self):
        return self._roomNumber

    @roomNumber.setter
    def roomNumber(self, value):
        if isinstance(value, int) and value > 0:
            self._roomNumber = value
        else:
            raise ValueError("A szobaszám csak pozitív egész lehet")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, int) and value > 0:
            self._price = value
        else:
            raise ValueError("Az ár csak pozitív egész lehet")

class SingleRoom(Room):
    def get_type(self):
        return "Egyágyas"

class DoubleRoom(Room):
    def get_type(self):
        return "Ketágyas"

class Hotel:
    def __init__(self):
        self.rooms = {}
        self.bookings = []

        self.add_room(SingleRoom(8, 6585))
        self.add_room(DoubleRoom(3, 8856))

        self.add_booking(Booking(8, '2024-04-20', 6585))
        self.add_booking(Booking(3, '2024-04-21', 8856))

    def add_room(self, room):
        self.rooms[room.roomNumber] = room

    def add_booking(self, booking):
        if any(b for b in self.bookings if b.roomNumber == booking.roomNumber and b.date == booking.date):
            raise Exception("A szoba ezen a napon már foglalt!")
        self.bookings.append(booking)

    def delete_booking(self, roomNumber, date):
        self.bookings = [b for b in self.bookings if not (b.roomNumber == roomNumber and b.date == date)]

    def list_bookings(self):
        return self.bookings

class Booking:
    def __init__(self, roomNumber, date, price):
        self.roomNumber = roomNumber
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.price = price

class HotelApp:
    def __init__(self, root, hotel):
        self.hotel = hotel
        root.title("Szállodai Szobafoglaló Rendszer")
        self.setup_ui(root)

    def setup_ui(self, root):
        tk.Label(root, text="Szobaszám:").pack()
        self.roomNumber_entry = tk.Entry(root)
        self.roomNumber_entry.pack()

        tk.Label(root, text="Dátum (ÉÉÉÉ-HH-NN):").pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        tk.Label(root, text="Ár:").pack()
        self.price_entry = tk.Entry(root)
        self.price_entry.pack()

        tk.Label(root, text="Szoba típusa:").pack()
        self.roomType_combo = ttk.Combobox(root, values=["Egyágyas", "Ketágyas"])
        self.roomType_combo.pack()

        tk.Button(root, text="Foglalás Hozzáadása", command=self.add_booking).pack()
        tk.Button(root, text="Foglalás Törlése", command=self.delete_booking).pack()
        tk.Button(root, text="Foglalások Listázása", command=self.list_bookings).pack()
        self.bookings_listbox = tk.Listbox(root)
        self.bookings_listbox.pack()
        root.geometry("600x600")# szerintem elég ekkora ablak, web API-kat szoktam írni C# .NEt fejlesztő vagyok , úgyhogy nem vagyok jártas az ilyen megjelenítéses dolgokban sajnos
                                # De gondoltam jobb mint a console-os, ha már csinálom :) Meg nyilván ezt lehetne tovább vinni, hogy külön mappák, melyben osztályok külön fájlokban stb, de nagyon sok a munkám és bízokbenne,
                                # hogy most ez így elég lesz, ha gyorsan leszögelem ezt. Egyébként nyilván C# ban nagy alkalmazásoknál használok patterneket (repository, builder stb...)
                                #Továbbá a commitok-ba  atest commit 4 -et elfelejtetem átírni, szóval az azért ismétlődik...
        self.list_bookings()

    def add_booking(self):
        try:
            roomNumber = int(self.roomNumber_entry.get())
            date = self.date_entry.get()
            price = int(self.price_entry.get())
            roomType = self.roomType_combo.get()
            roomClass = SingleRoom if roomType == "Egyágyas" else DoubleRoom
            room = roomClass(roomNumber, price)
            booking = Booking(roomNumber, date, price)
            self.hotel.add_room(room)
            self.hotel.add_booking(booking)
            self.list_bookings()
            messagebox.showinfo("Sikeres", "A foglalás sikeresen hozzáadva")
        except Exception as e:
            messagebox.showerror("Hiba", str(e))

    def delete_booking(self):
        try:
            roomNumber = int(self.roomNumber_entry.get())
            date = self.date_entry.get()
            self.hotel.delete_booking(roomNumber, date)
            self.list_bookings()
            messagebox.showinfo("Sikeres", "A foglalás sikeresen törölve.")
        except Exception as e:
            messagebox.showerror("Hiba", str(e))

    def list_bookings(self):
        self.bookings_listbox.delete(0, tk.END)
        for b in self.hotel.list_bookings():
            self.bookings_listbox.insert(tk.END, f"{b.roomNumber} - {b.date.strftime('%Y-%m-%d')} - {b.price}")

if __name__ == "__main__":
    root = tk.Tk()
    hotel = Hotel()
    app = HotelApp(root, hotel)
    root.mainloop()
