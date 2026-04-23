import fitz  # PyMuPDF

def split_pdf_into_quadrants(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    new_doc = fitz.open()

    for page_num in range(len(doc)):
        page = doc[page_num]
        rect = page.rect

        width = rect.width
        height = rect.height

        quadrants = [
            fitz.Rect(0, 0, width/2, height/2),
            fitz.Rect(width/2, 0, width, height/2),
            fitz.Rect(0, height/2, width/2, height),
            fitz.Rect(width/2, height/2, width, height)
        ]

        for quad in quadrants:
            new_page = new_doc.new_page(width=quad.width, height=quad.height)
            new_page.show_pdf_page(new_page.rect, doc, page_num, clip=quad)

    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()