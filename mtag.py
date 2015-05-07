#!/usr/bin/env python3

import argparse
import yaml
import id3parse
import glob

def get_args():
    parser = argparse.ArgumentParser(
        description='',
        epilog='',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    parser.add_argument('config',
                        help='YAML config file')
    return parser.parse_args()

class MediaFiles:
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

if __name__ == '__main__':
    args = get_args()
    mediafiles = MediaFiles.from_config_file(args.config)
