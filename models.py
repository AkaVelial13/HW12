from collections import UserDict
from datetime import datetime
import pickle
import os


class Field:
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @staticmethod
    def validate(value):
        pass

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self.__value = new_value


class Name(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        if not value.isalpha():
            raise ValueError("Invalid name format, must contain only letters")


class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format, must be 10 digits")


class Birthday(Field):
    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        try:
            datetime.strptime(value, Birthday.DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid birthday format, must be in the format {Birthday.DATE_FORMAT}")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday already exists for this record")
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("No birthday set for this record")

        today = datetime.today().date()
        birthday_date = datetime.strptime(self.birthday.value, Birthday.DATE_FORMAT).date()

        next_birthday = datetime(today.year, birthday_date.month, birthday_date.day).date()

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, birthday_date.month, birthday_date.day).date()

        days_left = (next_birthday - today).days
        return days_left

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        if not any(p.value == phone for p in self.phones):
            raise ValueError(f"Phone number {phone} not found in record {self.name.value}")

        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)

        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone number {old_phone} not found in record {self.name.value}")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

        if not self.phones:
            return None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact Name: {self.name.value}, Phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):

    @staticmethod
    def save_address_book(filename, data):
        directory = "AddressBooks"
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "wb") as file:
                pickle.dump(data, file)
            message = "Address book saved successfully."
        except IOError:
            message = "Error: Failed to save the address book."

        return message

    def load_address_book(self, filename):
        directory = "AddressBooks"
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "rb") as file:
                data = pickle.load(file)
            message = "Address book loaded successfully."
            self.data = data
        except (IOError, pickle.UnpicklingError):
            message = "Error: Failed to load the address book."
            data = None

        return data, message

    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError(f"Record with name {record.name.value} already exist  in the address book")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n=2):
        start = 0
        end = n
        while start < len(self.data):
            yield {name: self.data[name] for name in list(self.data)[start:end]}
            start += n
            end += n
