# Overseer - Watcher Of The Directory

Overseer watches over the directory it's being told to and executes handling
commands to these files based on regex rules that we've defined.

## Configuration

Rename `settings.sample.py` to `settings.py` and have fun tinkering with it!

There are four argument macros that will be replaced with actual named
arguments with each execution:
- `$INPUT_FILE` - The input file, i.e. the changed file
- `$OUTPUT_FILE` - The output file, which is equivalent to `$OUTPUT_DIR/$INPUT_FILE`
- `$INPUT_DIR` - The input directory, i.e. the directory that is being watched
- `$OUTPUT_DIR` - The destination directory to write the files to if specified when executing the script

