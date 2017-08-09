import unittest

from pathlib import Path

from fuzza.data import read


class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = Path(__file__) / '..' / '_testdata' / 'data' / '*'
        path = str(path.resolve())
        cls.data_path = path

    def test_able_to_read_data_from_files(self):
        config = {
            'data_path': self.data_path
        }
        data = read(config)
        expected = [
            b'data1a', b'data1b', b'data1c',
            b'data2a', b'data3a', b'data3b'
        ]
        self.assertListEqual(
            data,
            expected
        )
