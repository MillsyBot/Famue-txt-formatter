"""
E-book Text Formatter 
Formats text files to fit specific e-reader display constraints.
Display: 15 characters per row, 8 rows per page
Words are not split across line breaks.
"""

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


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ebook_formatter.py <input_file> [output_file]")
        print("Example: python ebook_formatter.py mybook.txt mybook_formatted.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Use custom output filename or generate one
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Generate output filename
        if input_file.endswith('.txt'):
            output_file = input_file.replace('.txt', '_formatted.txt')
        else:
            output_file = input_file + '_formatted.txt'
    
    format_ebook(input_file, output_file)
