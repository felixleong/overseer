import os.path as op
import pprint
import re
import subprocess
from observer.gitignore import GitIgnore
from observer.tree import TreeObserver

class ChangeListener(TreeObserver):
    """Observer for file changes within the directory tree."""

    executor = None

    def __init__(self, executor, patterns, basedir):
        super(ChangeListener, self).__init__(basedir, re.compile(r'|'.join(patterns.keys())), GitIgnore(basedir))
        self.executor = executor

    def action(self, entries):
        for filename in entries:
            if op.isfile(filename):
                self.executor.process(filename)


class FileTransformProcessor(object):
    """Handles all file transformations."""

    handler = {}
    source_dir = ''
    dest_dir = ''

    def __init__(self, handler, source_dir, dest_dir):
        self.handler = handler
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def process(self, filename):
        print 'Process', filename
