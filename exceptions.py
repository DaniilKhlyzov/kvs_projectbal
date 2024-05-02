class UsedKeyError(BaseException):
    def __init__(self, key):
        self.error = f'The key {key} is already used'

    def __str__(self):
        return self.error


class NoSuchKeyError(BaseException):
    def __init__(self, file, key):
        self.error = (f'There is no data with the '
                      f'key {key} in data file {file}')

    def __str__(self):
        return self.error


# Изменено название
class OutOfMemoryError(BaseException):
    def __init__(self, file):
        self.error = (f'There is no memory for your data in '
                      f'data file {file} now.\n'
                      f'Delete something to add your data')

    def __str__(self):
        return self.error
