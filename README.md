# E-book Text Formatter

A Python script to format text files for small e-reader devices with limited display capabilities.

## Device Specifications
- **Characters per row:** 21
- **Rows per page:** 8
- **Words are not split** across line breaks

## Usage

### Basic Usage
```bash
python ebook_formatter.py input_files
```
This will scan the directory (recursively) for files with `txt` in the name.

### Output Directory
```bash
python ebook_formatter.py input_files --output-dir output_files
```

### Batch with Title-Based Filenames
```bash
python ebook_formatter.py input_files --output-dir output_files --search-title
```

### Example
```bash
python ebook_formatter.py input_files --output-dir output_files
```

## Features
- ✓ Formats text to fit exactly 21 characters per line
- ✓ Keeps words intact (no word splitting)
- ✓ Preserves text content and order
- ✓ UTF-8 encoding support

## How It Works
1. Reads your input text file
2. Splits text into individual words
3. Builds lines by adding words without exceeding 21 characters
4. Saves the formatted output to a new file

## Files Included
- `ebook_formatter.py` - Main formatting script
- `sample_ebook.txt` - Example input file for testing
- `README.md` - This file

## Requirements
- Python 3.6 or higher
- No external dependencies required
