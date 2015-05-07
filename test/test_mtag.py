import unittest
import mtag

def mk_iglob(mapping=None):
    if mapping is None:
        mapping = {}
    def f(pattern):
        if pattern in mapping:
            matches = mapping[pattern]
        else:
            matches = []
        for match in matches:
            yield match
    return f

class TestMediaFiles(unittest.TestCase):
    def test_empty(self):
        mfiles = mtag.MediaFiles.from_config_file('test/data/empty.yml')
        files = mfiles.files(fetch_files_by_pattern=mk_iglob())
        self.assertEqual({}, files)

    def test_single_file(self):
        mfiles = mtag.MediaFiles.from_config_file('test/data/a.yml')
        files = mfiles.files(fetch_files_by_pattern=mk_iglob())
        expected = {
            'foo03.mp3' : {'title': 'Foo The Never',
                           'track': 3,
                           'album': 'The Foo Album',
                           'artist': 'Footallica',
                           'tracks': 10,
                           'genre': 'Hip hop',
                           'year': 1907,
            },
        }
        self.assertEqual(expected, files)

    def test_single_file_with_pattern(self):
        mfiles = mtag.MediaFiles.from_config_file('test/data/b.yml')
        iglob = mk_iglob({'foo*.mp3' : ['foo03.mp3']})
        files = mfiles.files(fetch_files_by_pattern=iglob)
        expected = {
            'foo03.mp3' : {'title': 'Foo The Never',
                           'track': 3,
                           'album': 'The Foo Album',
                           'artist': 'Footallica',
                           'tracks': 10,
                           'genre': 'Hip hop',
                           'year': 1907,
            },
        }
        self.assertEqual(expected, files)

    def test_single_explicit_file_pattern_two_files(self):
        mfiles = mtag.MediaFiles.from_config_file('test/data/b.yml')
        iglob = mk_iglob({'foo*.mp3' : ['foo03.mp3', 'foo07.mp3']})
        files = mfiles.files(fetch_files_by_pattern=iglob)
        expected = {
            'foo03.mp3' : {'title': 'Foo The Never',
                           'track': 3,
                           'album': 'The Foo Album',
                           'artist': 'Footallica',
                           'tracks': 10,
                           'genre': 'Hip hop',
                           'year': 1907,
            },
            'foo07.mp3' : {'album': 'The Foo Album',
                           'artist': 'Footallica',
                           'tracks': 10,
                           'genre': 'Hip hop',
                           'year': 1907,
            },
        }
        self.assertEqual(expected, files)

    def test_explicit_file_pattern_two_files(self):
        mfiles = mtag.MediaFiles.from_config_file('test/data/c.yml')
        iglob = mk_iglob({'foo*.mp3' : ['foo03.mp3', 'foo07.mp3']})
        files = mfiles.files(fetch_files_by_pattern=iglob)
        expected = {
            'foo03.mp3' : {'title': 'Foo The Never',
                           'track': 3,
                           'album': 'The Foo Album',
                           'artist': 'Footallica',
                           'tracks': 10,
                           'genre': 'Hip hop',
                           'year': 1907,
            },
            'foo07.mp3' : {'title': 'Fade to Foo',
                           'track': 7,
                           'album': 'The Foo Album',
                           'artist': 'Footallica',
                           'tracks': 10,
                           'genre': 'Hip hop',
                           'year': 1907,
            },
        }
        self.assertEqual(expected, files)
