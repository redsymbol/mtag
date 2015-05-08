#!/usr/bin/env python3

import argparse

import id3parse

from mtag import frames2labels

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('media_files', nargs='*')
    return parser.parse_args()

def tags_from_file(path):
    tags = dict()
    id3 = id3parse.ID3.from_file(path)
    for frame, field in frames2labels.items():
        try:
            value = id3.find_frame_by_name(frame).text
        except ValueError:
            continue
        tags[field] = value
    return tags

def print_tags(filename, tags):
    print('{}:'.format(filename))
    for name in sorted(tags.keys()):
        print('{}: {}'.format(name, tags[name]))
    print()

if __name__ == '__main__':
    args = get_args()
    for media_file in args.media_files:
        tags = tags_from_file(media_file)
        print_tags(media_file, tags)
