#!/usr/bin/env python3
"""Create a minimal valid PDF for testing without external dependencies."""

# Minimal PDF structure - this is valid PDF format
pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R >>
endobj
5 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 50 750 Td (Page 1) Tj ET
endstream
endobj
6 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 50 750 Td (Page 2) Tj ET
endstream
endobj
xref
0 7
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000214 00000 n 
0000000313 00000 n 
0000000407 00000 n 
trailer
<< /Size 7 /Root 1 0 R >>
startxref
501
%%EOF
"""

# Write the PDF file
with open("input.pdf", "wb") as f:
    f.write(pdf_content)

print("✅ Test PDF created: input.pdf")
