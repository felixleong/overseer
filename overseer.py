#! /usr/bin/env python

import os.path as op
import signal
import sys
import time

from base import HandlerCache, FileTransformProcessor, ChangeListener
import settings

def on_exit(sig, frame):
    print 'Exiting program'
    sys.exit(0)

def print_usage():
    print >> sys.stderr, 'USAGE: {0} src_dir [dest_dir]'.format(sys.argv[0])
    print >> sys.stderr, ''
    print >> sys.stderr, 'src_dir   The source directory to watch'
    print >> sys.stderr, 'dest_dir  (optional) The destination directory to write to'

if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    argc = len(sys.argv)
    if argc < 2:
        print_usage()
        sys.exit(1)

    src_dir = sys.argv[1]
    if argc >= 3:
        dest_dir = sys.argv[2]
    else:
        dest_dir = '.'
    if not op.isdir(src_dir):
        print >> sys.stderr, 'ERROR: Source directory does not exists'
        sys.exit(1)
    if not op.isdir(dest_dir):
        print >> sys.stderr, 'ERROR: Destination directory does not exists'
        sys.exit(1)

    handler_cache = HandlerCache(settings.HANDLERS)
    if len(settings.HANDLERS) <= 0:
        print >> sys.stderr, 'No handler specified, quitting'
        sys.exit(0)

    print 'Listening for changes...'
    transform_processor = FileTransformProcessor(handler_cache, src_dir,
            dest_dir)
    listener = ChangeListener(transform_processor,
            handler_cache.get_regex_list(), src_dir)
    listener.loop()
