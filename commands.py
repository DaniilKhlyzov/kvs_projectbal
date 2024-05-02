import storagemain


class Commands(object):

    def __init__(self):
        self.commands = {
            'add': self.add,
            'del': self.delete,
            'exists': self.exists,
            'get': self.get,
            'save': self.save,
            'change': self.change_storage,
            'all': self.get_all,
            'clone': self.clone_storage,
            'exit': self.close_app,
            'size': self.get_size,
            'keys': self.keys,
            'values': self.values,
            'prefix': self.prefix_search  # Added prefix command
        }

    def handle_command(self, command, *args):
        return self.commands[command](*args)

    def execute_command(self, storage, input_data):
        command, arg1, arg2 = self.parse_args(input_data)
        try:
            return self.handle_command(command, storage, arg1, arg2)
        except KeyError:
            return 'Unknown command'

    @staticmethod
    def add(storage, key, value):
        try:
            storage.add(key, value)
            return f"Key '{key}' was added successfully."
        except Exception as e:
            return str(e)

    @staticmethod
    def get(storage, key):
        try:
            return storage.get(key)
        except KeyError:
            return f"There is no data with the key '{key}' in data file '{storage.name}'."

    @staticmethod
    def delete(storage, key):
        try:
            storage.delete(key)
            return f"Key '{key}' was deleted successfully."
        except KeyError:
            return "Key not found."

    @staticmethod
    def exists(storage, key):
        return str(storage.exists(key))

    @staticmethod
    def all_keys(storage):

        try:
            return storage.keys()
        except Exception as e:
            return str(e)

    @staticmethod
    def values(storage):

        try:
            return storage.values()
        except Exception as e:
            return str(e)

    @staticmethod
    def get_all(storage):

        try:
            return storage.all_items()
        except Exception as e:
            return str(e)

    @staticmethod
    def get_size(storage):
        return str(storage.get_file_size())

    @staticmethod
    def close_app(storage):
        storage.save()
        return f"Goodbye. Thanks for using the '{storage.name}' KV-Storage."

    @staticmethod
    def save(storage):
        try:
            storage.save()
            return f"Your '{storage.name}' KV-Storage was successfully saved."
        except Exception as e:
            return str(e)

    @staticmethod
    def change_storage(storage, name):
        try:
            storage.change_storage(name)
            return f"Changed to '{name}' KV-Storage."
        except Exception as e:
            return str(e)

    @staticmethod
    def clone_storage(storage):
        try:
            new_name = storage.name + '-Clone'
            new_storage = storagemain.Storage(new_name)
            new_storage.data = storage.data
            new_storage.save()
            return f"Clone '{new_name}' KV-Storage was created."
        except Exception as e:
            return str(e)

    @staticmethod
    def prefix_search(storage, prefix):
        try:
            return [key for key in storage.keys() if key.startswith(prefix)]
        except Exception as e:
            return str(e)

    @staticmethod
    def parse_args(args):
        args = args.split(maxsplit=2)
        if len(args) == 0:
            command = None
        else:
            command = args[0]
        arg1 = None
        arg2 = None
        if len(args) == 2:
            arg1 = args[1]
        if len(args) > 2:
            arg1 = args[1]
            arg2 = args[2]
        return command, arg1, arg2
