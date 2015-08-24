import unittest
import mtag
import yaml

class TestPatternsAndFiles(unittest.TestCase):
    def test_main(self):
        yaml_data = yaml.load('''
- pattern: 'stuff*.mp3'
  album: The Best Stuff
  artist: Xavier Speed
  year: 2082
  tracks: auto

- file: stuff1.mp3
  title: 'The Stuff Of Greatness'

- file: stuff2.mp3
  title: 'Marvelous Stuff'

- file: stuff3.mp3
  title: 'Stuff Forever! Live From Manchester'
''')
        expected_patterns = [{
            'pattern' : 'stuff*.mp3',
            'album' : 'The Best Stuff',
            'artist' : 'Xavier Speed',
            'year' : '2082',
            'tracks' : 'auto',
            }]
        expected_explicit_files = [
            {'file': 'stuff1.mp3',
             'title': 'The Stuff Of Greatness',
             },
            {'file': 'stuff2.mp3',
             'title': 'Marvelous Stuff',
             },
             {'file': 'stuff3.mp3',
             'title': 'Stuff Forever! Live From Manchester',
             },
            ]
        patterns_and_files = mtag.PatternsAndFiles(yaml_data)
        self.assertEqual(expected_patterns, list(patterns_and_files.patterns))
        self.assertEqual(expected_explicit_files, list(patterns_and_files.explicit_files))
        

class TestMTag(unittest.TestCase):
    def test_find_files(self):
        patterns = [{
            'pattern' : 'stuff*.mp3',
            'album' : 'The Best Stuff',
            'artist' : 'Xavier Speed',
            'year' : '2082',
            'tracks' : 'auto',
            }]
        explicit_files = [
            {'file': 'stuff1.mp3',
             'title': 'The Stuff Of Greatness',
             },
            {'file': 'stuff2.mp3',
             'title': 'Marvelous Stuff',
             },
             {'file': 'stuff3.mp3',
             'title': 'Stuff Forever! Live From Manchester',
             },
            ]
        # test version of glob.iglob. TODO: use mock instead
        files_on_fs = [
            'stuff1.mp3',
            'stuff2.mp3',
            'stuff3.mp3',
            ]
        def test_iglob(glob_pattern):
            self.assertEqual('stuff*.mp3', glob_pattern)
            for item in files_on_fs:
                yield item

        expected = {
            'stuff1.mp3': {
                'title': 'The Stuff Of Greatness',
                'track': '1/3',
                'album' : 'The Best Stuff',
                'artist' : 'Xavier Speed',
                'year' : '2082',
            },
            'stuff2.mp3': {
                'title': 'Marvelous Stuff',
                'track': '2/3',
                'album' : 'The Best Stuff',
                'artist' : 'Xavier Speed',
                'year' : '2082',
            },
            'stuff3.mp3': {
                'title': 'Stuff Forever! Live From Manchester',
                'track': '3/3',
                'album' : 'The Best Stuff',
                'artist' : 'Xavier Speed',
                'year' : '2082',
            },
        }
        actual = mtag.find_files(patterns, explicit_files, files_by_glob_pattern = test_iglob)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(sorted(expected.keys()), sorted(actual.keys()))
        for filename, expected_info in expected.items():
            actual_info = actual[filename]
            with self.subTest(filename=filename):
                self.assertEqual(expected_info, actual_info)
