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
    parser.add_argument('--quiet', action='store_true', default=False,
                        help='Be more silent in output')
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
                data = dict(item)
                for k, v in data.items():
                    if type(v) != str:
                        data[k] = str(v)
                yield data

    @property
    def explicit_files(self):
        for item in self.data:
            if 'file' in item:
                data = dict(item)
                for k, v in data.items():
                    if type(v) != str:
                        data[k] = str(v)
                yield data

    def files(self, fetch_files_by_pattern = glob.iglob):
        media_files = dict()
        for pattern_info in self.patterns:
            tracks = None
            pattern_file_info = {}
            for key, value in pattern_info.items():
                if key == 'tracks':
                    tracks = value
                elif key == 'pattern':
                    pattern = value
                else:
                    # will copy to file
                    pattern_file_info[key] = value
            for index, path in enumerate(fetch_files_by_pattern(pattern), 1):
                if path not in media_files:
                    media_files[path] = dict()
                media_files[path].update(pattern_file_info)
                if tracks == 'auto':
                    # This assumes only one pattern matching all files.
                    # Will need to do a little more work to properly support multiple patterns.
                    media_files[path]['auto_track_index'] = index
                elif tracks is not None:
                    media_files[path]['tracks'] = tracks
        for file_info in self.explicit_files:
            path = file_info['file']
            del file_info['file']
            if path not in media_files:
                media_files[path] = dict()
            media_files[path].update(file_info)
        have_auto_track = [file_info for file_info in media_files.values()
                           if 'auto_track_index' in file_info]
        for file_info in have_auto_track:
            file_info['track'] = '{}/{}'.format(file_info['auto_track_index'], len(have_auto_track))
            del file_info['auto_track_index']
        inherit_tracks = [file_info for file_info in media_files.values()
                          if 'tracks' in file_info]
        for file_info in inherit_tracks:
            tracks = file_info['tracks']
            del file_info['tracks']
            if 'track' in file_info and '/' not in file_info['track']:
                file_info['track'] += '/' + tracks
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

def convert_track(value, tracks):
    value = str(value)
    if (tracks is not None) and ('/' not in value):
        value += '/' + tracks
    return value

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
        for name, value in tags.items():
            if name == 'track':
                value = convert_track(value, tracks)
            elif name == 'year':
                value = str(value)
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
        if not args.quiet:
            print(path)
        mediafile = MediaFile(path)
        mediafile.update(**tags)
