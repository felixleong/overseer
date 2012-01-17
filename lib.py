import os.path as op
import pprint
import re
import sys
import subprocess
from observer.gitignore import GitIgnore
from observer.tree import TreeObserver

class HandlerCache(object):
    regexes = []
    handlers = {}

    def __init__(self, config):
        self.regexes = [ (re.compile(regex_str), regex_str)
                for regex_str, command in config ]
        self.handlers = { regex_str: command for regex_str, command in config }

    def get_command(self, filename):
        """Retrieve the processing command based on its file match."""
        for regex, key in self.regexes:
            if regex.search(filename):
                return self.handlers[key]

        return

    def get_regex_list(self):
        return self.handlers.keys()


class ChangeListener(TreeObserver):
    """Observer for file changes within the directory tree."""

    executor = None

    def __init__(self, executor, regex_list, basedir):
        super(ChangeListener, self).__init__(basedir,
                re.compile(r'|'.join(regex_list)), GitIgnore(basedir))
        self.executor = executor

    def action(self, entries):
        for filename in entries:
            self.executor.process(filename)


class FileTransformProcessor(object):
    """Handles all file transformations."""

    source_dir = ''
    dest_dir = ''
    regexes = {
        'input_file': re.compile(r'\$INPUT_FILE'),
        'output_file': re.compile(r'\$OUTPUT_FILE'),
        'input_dir': re.compile(r'\$INPUT_DIR'),
        'output_dir': re.compile(r'\$OUTPUT_DIR'),
    }

    def __init__(self, handler, source_dir, dest_dir):
        self.handler = handler
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def _update_required(self, source_file, dest_file):
        """Check whether an update is required."""

        if not op.isfile(source_file):
            return False

        if not op.exists(dest_file):
            return True

        if not op.isfile(dest_file):
            return False

        return (op.getmtime(source_file) > op.getmtime(dest_file))

    def _translate_command(self, command, data):
        """Perform string substitution on the configured command"""

        result = command
        for key, regex in self.regexes.iteritems():
            result = re.sub(regex, data[key], result)
        return result

    def _get_command(self, filename):
        pass

    def process(self, filename):
        source_file = op.join(self.source_dir, filename)
        dest_file = op.join(self.dest_dir, filename)

        if self._update_required(source_file, dest_file):
            print 'Processing', filename
            data = {
                'input_file': source_file,
                'output_file': dest_file,
                'input_dir': self.source_dir,
                'output_dir': self.dest_dir,
            }
            command = self._translate_command(
                    self.handler.get_command(filename), data)
            try:
                subprocess.check_output(command, shell=True)
            except subprocess.CalledProcessError:
                print >> stderr, 'ERROR: failure occured with', command

