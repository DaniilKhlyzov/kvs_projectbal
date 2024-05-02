import unittest

from storagemain import Storage


class TestStorage(unittest.TestCase):

    def test_init(self):
        storage = Storage('test')
        self.assertEqual(storage.data, {})
        storage.exit()

    def test_add(self):
        storage = Storage('test')
        storage.add('a', 'b')
        storage.save()
        self.assertEqual(storage.data, {"a": "b"})
        storage.exit()

    def test_get(self):
        storage = Storage('test')
        storage.add('some', 'res')
        self.assertEqual(storage.get('some'), 'res')
        storage.exit()

    def test_delete(self):
        storage = Storage('test')
        storage.add('none', 'res')
        storage.delete('none')
        self.assertEqual(storage.data, {})
        storage.exit()

    def test_exists_yes(self):
        storage = Storage('test')
        storage.add('zero', 'some')
        self.assertEqual(
            storage.exists('zero'),
            'The key "zero" is in data file "test"')
        storage.exit()

    def test_keys(self):
        storage = Storage('test')
        storage.add('7', '9')
        storage.add('hello', 'world')
        self.assertEqual(storage.keys(), '7 hello')
        storage.exit()

    def test_values(self):
        storage = Storage('test')
        storage.add('a', 'b')
        storage.add('1', '3')
        self.assertEqual(storage.values(), 'b 3')
        storage.exit()

    def test_change_storage(self):
        storage = Storage('test')
        storage.add('a', 'b')
        storage.change_storage('data')
        self.assertEqual(storage.data, {})
        storage.exit()

    def test_exit(self):
        storage = Storage('test')
        self.assertEqual(storage.exit(), None)

    def test_save_load(self):
        storage = Storage('test')
        storage.add('hello', 'python')
        storage.save()
        storage = Storage('test')
        storage.save()
        self.assertEqual(storage.data, {})

    def test_save(self):
        storage = Storage('test')
        storage.save()
        self.assertEqual(storage.data, {})
        storage.exit()


class TestFails(unittest.TestCase):

    def test_delete_exception(self):
        storage = Storage('test')
        storage.add('2', '0')
        self.assertEqual(storage.delete('1'),
                         'There is no data with the key 1 in data file test')
        storage.exit()

    def test_add_exception(self):
        storage = Storage('test')
        storage.add('0', '7')
        self.assertEqual(storage.add('0', '1'), 'The key 0 is already used')
        storage.exit()

    def test_get_exception(self):
        storage = Storage('test')
        storage.add('0', '7')
        self.assertEqual(storage.get('3'),
                         'There is no data with the key 3 in data file test')
        storage.exit()


if __name__ == '__main__':
    unittest.main()
