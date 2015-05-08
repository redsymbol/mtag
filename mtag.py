#!/usr/bin/env python3

import argparse
import collections
import glob

import yaml
import id3parse

def get_args():
    parser = argparse.ArgumentParser(
        description='',
        epilog='',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    parser.add_argument('config',
                        help='YAML config file')
    return parser.parse_args()

class TagDefinitions:
    @classmethod
    def from_config_file(cls, path):
        with open(path) as config:
            data = yaml.load(config)
            return cls(data)

    @property
    def patterns(self):
        for item in self.data:
            if 'pattern' in item:
                yield dict(item)

    @property
    def explicit_files(self):
        for item in self.data:
            if 'file' in item:
                yield dict(item)

    def files(self, fetch_files_by_pattern = glob.iglob):
        media_files = dict()
        for pattern_data in self.patterns:
            pattern = pattern_data['pattern']
            del pattern_data['pattern']
            for path in fetch_files_by_pattern(pattern):
                if path not in media_files:
                    media_files[path] = dict()
                media_files[path].update(pattern_data)
        for file_data in self.explicit_files:
            path = file_data['file']
            del file_data['file']
            if path not in media_files:
                media_files[path] = dict()
            media_files[path].update(file_data)
        return media_files

    # private ctor
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data

frames2labels = {
    'TIT2' : 'title',
    'TPE1' : 'artist',
    'TALB' : 'album',
    'TRCK' : 'track',
    'TYER' : 'year',
    'TCON' : 'genre',
    #'COMM' : 'comment'
}

labels2frames = dict((value, key) for key, value in frames2labels.items())


class MediaFile:
    def __init__(self, path):
        self.path = path
        with open(path) as handle:
            self.id3 = id3parse.ID3.from_file(path)
            
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.path)

    def update(self, **tags):
        changed = False
        if 'tracks' in tags:
            tracks = str(tags['tracks'])
            del tags['tracks']
        else:
            tracks = None
        def convert_track(value):
            value = str(value)
            if (tracks is not None) and ('/' not in value):
                value += '/' + tracks
            return value
        def identity(x): return x
        converters = collections.defaultdict(lambda: identity)
        converters.update({
            'year' : str,
            'track' : convert_track,
               })
        for name, value in tags.items():
            value = converters[name](value)
            frame_name = labels2frames[name]
            try:
                frame = self.id3.find_frame_by_name(frame_name)
            except ValueError:
                new_frame = id3parse.ID3TextFrame.from_scratch(frame_name, value)
                self.id3.add_frame(new_frame)
                changed = True
                continue
            if frame.text != value:
                frame.text = value
                changed = True
        if changed:
            self.id3.to_file()

if __name__ == '__main__':
    args = get_args()
    tagdefs = TagDefinitions.from_config_file(args.config)
    for path, tags in tagdefs.files().items():
        mediafile = MediaFile(path)
        mediafile.update(**tags)
