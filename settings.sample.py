HANDLERS = (
    # Format: (r'File pattern regex to match', 'Resulting command to execute')
    (r'.*\.png$', 'optipng -out "$OUTPUT_FILE" "$INPUT_FILE"'),
    (r'.*\.jpe*g$', 'jpegoptim -p --strip-all --dest="$OUTPUT_DIR" "$INPUT_FILE"'),
)
