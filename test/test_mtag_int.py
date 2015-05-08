import unittest
import shutil
import tempfile
import subprocess
import os

import id3parse

MP3FILE_PROTOTYPE = 'test/data/test.mp3'

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.scratchdir = tempfile.mkdtemp()
        self.test_mp3 = os.path.join(self.scratchdir, 'test.mp3')
        shutil.copy(MP3FILE_PROTOTYPE, self.test_mp3)

    def tearDown(self):
        shutil.rmtree(self.scratchdir, ignore_errors=False)

    def verify_empty(self):
        id3 = id3parse.ID3.from_file(self.test_mp3)
        self.assertEqual(0, len(id3.frames))

    def test_integration_simple(self):
        root = os.path.join(os.path.dirname(__file__), '..')
        executable = os.path.join(root, 'mtag.py')
        config_file = os.path.join(root, 'test', 'data', 'test_integration_simple.yml')
        proc = subprocess.Popen(
            ['python', executable, config_file],
            cwd=self.scratchdir)
        proc.wait()
        self.assertEqual(0, proc.returncode)

        id3 = id3parse.ID3.from_file(self.test_mp3)
        # artist field (TPE1)
        artist = id3.find_frame_by_name('TPE1').text
        self.assertEqual('Whitney Houston', artist)
        # title field (TIT2)
        title = id3.find_frame_by_name('TIT2').text
        self.assertEqual('Flying Home', title)
        # album field (TALB)
        album = id3.find_frame_by_name('TALB').text
        self.assertEqual('Neverending Story Soundtrack', album)
        # track field (TRCK)
        track = id3.find_frame_by_name('TRCK').text
        self.assertEqual('3', track)
        # year field (TYER)
        year = id3.find_frame_by_name('TYER').text
        self.assertEqual('1999', year)
        # genre field (TCON)
        genre = id3.find_frame_by_name('TCON').text
        self.assertEqual('Alternative', genre)
