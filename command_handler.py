from models import AddressBook, Record


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
            'show all': self.handle_contact_get_all
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
    def handle_contact_add(self, command):
        name, phone = command
        record = Record(name)
        record.add_phone(phone)
        self.address_book.add_record(record)
        return f'Contact {name} added with phone number {phone}'

    @input_error
    def handle_contact_change(self, command):
        name, phone = command
        record = self.address_book.find(name)
        if record:
            record.add_phone(phone)
            return f'Phone number for {name} changed to {phone}'
        else:
            return f'Contact {name} not found'

    @input_error
    def handle_contact_get_by_name(self, command):
        name = command[0]
        record = self.address_book.find(name)
        if record:
            return str(record)
        else:
            return f'Contact {name} not found'

    def handle_contact_get_all(self, *_):
        if not self.address_book.data:
            return 'No contacts found'

        result = '\n'.join(str(record) for record in self.address_book.data.values())
        return f'   Name: Phone number\n{result}\n'

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
