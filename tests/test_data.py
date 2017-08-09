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

    def test_read_data_in_chunk(self):
        config = {
            'data_path': self.data_path,
            'data_chunk': True
        }
        data = read(config)
        expected = [
            b'data1a\ndata1b\ndata1c\n',
            b'data2a\n',
            b'data3a\ndata3b\n'
        ]
        self.assertListEqual(
            data,
            expected
        )
