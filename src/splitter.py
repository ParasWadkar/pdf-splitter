from pypdf import PdfReader, PdfWriter
from copy import deepcopy

def split_pdf_into_quadrants(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        # Get page dimensions
        mediabox = page.mediabox
        width = float(mediabox.width)
        height = float(mediabox.height)

        # Define quadrants (x1, y1, x2, y2)
        quadrants = [
            (0, height/2, width/2, height),           # Top-left
            (width/2, height/2, width, height),       # Top-right
            (0, 0, width/2, height/2),                # Bottom-left
            (width/2, 0, width, height/2)             # Bottom-right
        ]

        for x1, y1, x2, y2 in quadrants:
            # Create a copy of the page and crop it
            new_page = deepcopy(page)
            new_page.cropbox.lower_left = (x1, y1)
            new_page.cropbox.upper_right = (x2, y2)
            writer.add_page(new_page)

    # Write to output file
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)