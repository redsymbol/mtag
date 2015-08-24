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
        
