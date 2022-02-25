from fpdf import FPDF
from PIL import Image, ImageChops
from PyPDF2 import PdfFileReader, PdfFileWriter


def makePdf(pdfFileName, listPages, path):
    ''' List of jpg files to pdf '''
    cover = Image.open(path + str(listPages[0]) + '.jpg')
    width, height = cover.size

    pdf = FPDF(unit='pt', format=[width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(path + str(page) + '.jpg', 0, 0)

    pdf.output(path + pdfFileName + '.pdf', 'F')


def mergePdf(files, output):
    ''' Merge pdf files to one '''
    pdf_writer = PdfFileWriter()

    for path in files:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output, 'wb') as fh:
        pdf_writer.write(fh)


def trim(path, file):
    ''' Trim background from image '''
    im = Image.open(path + file + '.jpg')
    dpi = im.info['dpi']

    bg = Image.new(im.mode, im.size, im.getpixel((im.size[0] - 1, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save(path + file + '_trimmed.jpg', dpi=dpi)
    return bool(bbox)


def rotate(path, file, angle):
    ''' Rotate jpg by x degrees '''
    im = Image.open(path + file + '.jpg')
    dpi = im.info['dpi']
    im.rotate(angle).save(path + file + '_rotated.jpg', dpi=dpi)


path = r'.'
# trim(path, 'CCF11092018_00001')
# rotate(path, 'CCF11092018_00001', 180)
# mergePdf((path + file for file in ('x.pdf', 'y.pdf')), 'xy_merge.pdf')
# makePdf('xy', ['x.jpg', 'y.jpg'], path)
