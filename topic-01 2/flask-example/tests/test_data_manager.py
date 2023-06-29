import os
import unittest

from data_manager import SimpleDataManager

test_user_names = ['Ant', 'Bob', 'Cat', 'Dan', 'Emma', 'Fatima', 'Gregg', 'Hanns', 'Ingrid', 'Jules']

class MyTestCase(unittest.TestCase):

    def test_something(self):
        data = SimpleDataManager()
        data.load_users(os.path.join('../','flaskr','res','user_data.csv'))
        for names in data.users:
            if names not in test_user_names:
                self.fail()

        self.assertEqual(10, len(data.users))


if __name__ == '__main__':
    unittest.main()
