#! /usr/bin/env python

import os.path as op
import signal
import sys

from lib import FileTransformProcessor, ChangeListener
import settings

def on_exit(signal, frame):
    print 'Exiting program'
    sys.exit(0)

def print_usage():
    print >> sys.stderr, 'USAGE: {0} src_dir dest_dir'.format(sys.argv[0])
    print >> sys.stderr, ''
    print >> sys.stderr, 'src_dir   The source directory to watch'
    print >> sys.stderr, 'dest_dir  The destination directory to write to'

if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    if not op.isdir(src_dir):
        print >> sys.stderr, 'ERROR: Source directory does not exists'
        sys.exit(1)
    if not op.isdir(dest_dir):
        print >> sys.stderr, 'ERROR: Destination directory does not exists'
        sys.exit(1)

    print 'Listening for changes...'
    transform_processor = FileTransformProcessor(settings.HANDLERS, src_dir,
            dest_dir)
    ChangeListener(transform_processor, settings.HANDLERS, src_dir).loop()
