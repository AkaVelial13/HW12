from models import AddressBook, Record, Birthday, Name, Phone


class CommandHandler:
    def __init__(self, address_book):
        self.address_book = address_book
        self.command_handlers = {
            'hello': self.handle_hello,
            'good bye': self.handle_end,
            'close': self.handle_end,
            'exit': self.handle_end,
            'add': self.handle_contact_add,
            'change': self.handle_contact_change,
            'phone': self.handle_contact_get_by_name,
            'birthday': self.handle_set_birthday,
            'show all': self.handle_contact_get_all,
            'search': self.handle_search_contacts,
            'save': self.handle_save_address_book,
            'load': self.handle_load_address_book
        }

    @staticmethod
    def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return 'Enter user name'
            except ValueError:
                return 'Give me name and phone please'
            except IndexError:
                return 'Invalid command format'
        return wrapper

    @staticmethod
    def handle_invalid_command(*_):
        return 'Invalid command format'

    @staticmethod
    def handle_hello(*_):
        return 'How can I help you?'

    @staticmethod
    def handle_end(*_):
        return 'Good bye!'

    @input_error
    def handle_save_address_book(self, command):
        try:
            filename = command[0]
            message = self.address_book.save_address_book(filename, self.address_book.data)
            return message
        except IndexError:
            return 'Please provide a filename'

    @input_error
    def handle_load_address_book(self, command):
        try:
            filename = command[0]
            data, message = self.address_book.load_address_book(filename)
            if data is not None:
                return f'Address book "{filename}" loaded'
            else:
                return message
        except IndexError:
            return 'Please provide a filename'

    @input_error
    def handle_contact_add(self, command):
        name, *phones = command
        try:
            Name.validate(name)
            if not phones:
                raise ValueError('At least one phone number must be provided')
            for phone in phones:
                Phone.validate(phone)

            record = Record(name)
            for phone in phones:
                record.add_phone(phone)
            self.address_book.add_record(record)

            return f'Contact {name} added with phone numbers: {", ".join(phones)}'

        except ValueError as ve:
            return str(ve)

    @input_error
    def handle_set_birthday(self, command):
        name, birthday = command
        try:
            Name.validate(name)
            Birthday.validate(birthday)

            record = self.address_book.find(name)
            if not record:
                return f'Contact {name} not found'

            record.add_birthday(birthday)
            return f'Birthday {birthday} added for contact {name}'

        except ValueError as ve:
            return str(ve)

    @input_error
    def handle_contact_change(self, command):
        name, *phones = command
        try:
            Name.validate(name)
            if not phones:
                raise ValueError('At least one phone number must be provided')
            for phone in phones:
                Phone.validate(phone)

            record = self.address_book.find(name)
            if not record:
                return f'Contact {name} not found'

            for phone in phones:
                record.add_phone(phone)

            return f'Phone number(s) for {name} changed to {", ".join(phones)}'

        except ValueError as ve:
            return str(ve)

    @input_error
    def handle_contact_get_by_name(self, command):
        name = command[0]
        try:
            Name.validate(name)
        except ValueError as ve:
            return str(ve)

        record = self.address_book.find(name)
        if record:
            return str(record)
        else:
            return f'Contact {name} not found'

    def handle_contact_get_all(self, *_):
        if not self.address_book.data:
            return 'No contacts found'

        result = ''
        for record in self.address_book.data.values():
            birthday_info = ''
            if record.birthday:
                days_left = record.days_to_birthday()
                birthday_info = f', Days until birthday: {days_left}'
            result += str(record) + birthday_info + '\n'

        return result

    @input_error
    def handle_search_contacts(self, command):
        search_query = " ".join(command)
        results = []
        for record in self.address_book.data.values():
            if search_query.lower() in record.name.value.lower():
                results.append(str(record))
            else:
                for phone in record.phones:
                    if search_query in phone.value:
                        results.append(str(record))
                        break
        if results:
            return '\n'.join(results)
        else:
            return 'No matching contacts found'

    def get_handler(self, command: str) -> tuple:
        user_command = command.lower().split()
        user_command_data = command.split()

        handler = self.command_handlers.get(user_command[0], None)
        user_data_list = user_command_data[1:]

        if not handler and len(user_command) > 1:
            two_words_command = user_command[0] + ' ' + user_command[1]
            handler = self.command_handlers.get(two_words_command, None)
            user_data_list = user_command_data[2:]

        return (handler, user_data_list) if handler is not None \
            else (self.handle_invalid_command, [])


def main():
    address_book = AddressBook()
    command_handler = CommandHandler(address_book)

    while True:
        user_input = input('Enter command: ')

        if not user_input:
            print(command_handler.handle_invalid_command())
            continue

        handler, user_command_data = command_handler.get_handler(user_input)

        answer = handler(user_command_data)

        print(answer)

        if answer == 'Good bye!':
            break


if __name__ == '__main__':
    main()
