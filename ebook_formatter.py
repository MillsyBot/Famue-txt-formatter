"""
E-book Text Formatter
Formats text files to fit specific e-reader display constraints.
Display: 15 characters per row, 8 rows per page
Words are not split across line breaks.
"""

import os
from pathlib import Path

def strip_gutenberg_header(text):
    marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    marker_index = text.find(marker)
    if marker_index == -1:
        return text

    newline_index = text.find("\n", marker_index)
    if newline_index == -1:
        return ""

    return text[newline_index + 1:]


def format_ebook(input_file, output_file, chars_per_line=21, rows_per_page=8):
    """
    Format an e-book text file for a small e-reader device.
    
    Args:
        input_file: Path to the input text file
        output_file: Path to the output formatted file
        chars_per_line: Maximum characters per line (default: 21)
        rows_per_page: Number of rows per page (default: 8)
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Remove Gutenberg header block if present
        text = strip_gutenberg_header(text)

        # Split text into words
        words = text.split()
        
        formatted_lines = []
        current_line = ""
        row_count = 0
        
        for word in words:
            # Check if adding this word would exceed the line limit
            if current_line:
                test_line = current_line + " " + word
            else:
                test_line = word
            
            if len(test_line) <= chars_per_line:
                # Word fits on current line
                current_line = test_line
            else:
                # Current line is complete, save it
                if current_line:
                    formatted_lines.append(current_line)
                
                # Start new line with current word
                current_line = word
        
        # Add the last line if it exists
        if current_line:
            formatted_lines.append(current_line)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(formatted_lines))
        
        print(f"✓ Successfully formatted '{input_file}'")
        print(f"✓ Output saved to '{output_file}'")
        print(f"✓ Total lines: {len(formatted_lines)}")
        
    except FileNotFoundError:
        print(f"✗ Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def sanitize_title(title):
    cleaned = "".join(ch if ch.isalnum() or ch.isspace() else "" for ch in title)
    return "_".join(cleaned.split())


def extract_title_from_file(input_path):
    prefix = "The Project Gutenberg eBook of"
    title_prefix = "Title:"
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(title_prefix):
                return line[len(title_prefix):].strip()
            if line.startswith(prefix):
                return line[len(prefix):].strip()
    return None


def build_output_path(input_path, output_dir=None, gutenberg=False):
    if gutenberg:
        title = extract_title_from_file(input_path)
        if title:
            sanitized = sanitize_title(title)
            if sanitized:
                filename = f"{sanitized}.txt"
            else:
                filename = f"{input_path.stem}_formatted{input_path.suffix}"
        else:
            filename = f"{input_path.stem}_formatted{input_path.suffix}"
    else:
        filename = f"{input_path.stem}_formatted{input_path.suffix}"

    if output_dir:
        return Path(output_dir) / filename

    return input_path.with_name(filename)


def format_directory(
    input_dir,
    output_dir,
    chars_per_line=21,
    rows_per_page=8,
    gutenberg=False,
):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"✗ Error: Directory '{input_dir}' not found.")
        return

    output_path.mkdir(parents=True, exist_ok=True)

    files = []
    for root, _, filenames in os.walk(input_path):
        for filename in filenames:
            if "txt" in filename.lower():
                files.append(Path(root) / filename)

    if not files:
        print(f"✗ Error: No input files found in '{input_dir}'.")
        return

    for file_path in files:
        output_file = build_output_path(
            file_path,
            output_dir=output_path,
            gutenberg=gutenberg,
        )
        format_ebook(file_path, output_file, chars_per_line, rows_per_page)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Format text files for a small e-reader device."
    )
    parser.add_argument("--input-dir", default="input_dir", help="Directory of input files to format")
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        help="Directory to write formatted files",
    )
    parser.add_argument(
        "--gutenberg",
        dest="gutenberg",
        action="store_true",
        help="Use Gutenberg project metadata for output filename",
    )
    args = parser.parse_args()

    output_dir = args.output_dir or "output_dir"
    format_directory(args.input_dir, output_dir, gutenberg=args.gutenberg)
