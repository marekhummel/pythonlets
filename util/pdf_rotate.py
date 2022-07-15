from PyPDF2 import PdfFileReader, PdfFileWriter
from os import rename


file = r'.'


# Read and rotate
with open(file, 'rb') as pdf_in:
    pdf_reader = PdfFileReader(pdf_in, strict=False)
    pdf_writer = PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(90)
        pdf_writer.addPage(page)

    # Write
    with open(file.replace('.pdf', '_rot.pdf'), 'wb') as pdf_out:
        pdf_writer.write(pdf_out)

# backup
rename(file, file.replace('.pdf', '_orig.pdf'))
rename(file.replace('.pdf', '_rot.pdf'), file)
