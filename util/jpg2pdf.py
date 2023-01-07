import os

from fpdf import FPDF
from pdf2image import convert_from_path
from PIL import Image, ImageChops
from PyPDF2 import PdfFileReader, PdfFileWriter


def makePdf(pdfFileName, listPages, path):
    """List of jpg files to pdf"""
    pdf = FPDF(unit="pt")

    for page in listPages:
        cover = Image.open(path + str(page))
        width, height = cover.size
        pdf.add_page(format=(width, height))
        pdf.image(path + str(page), 0, 0)

    pdf.output(path + pdfFileName)


def pdfTrimPages(path, pdfFileName, deleteTempFiles=True):
    """Applies the trim function on pages of a pdf"""
    dpi = 300
    pages = convert_from_path(path + pdfFileName, dpi)
    images = []
    for i, page in enumerate(pages):
        images.append(f"out{i}.jpg")
        page.save(path + f"out{i}.jpg", "JPEG")

    for img in images:
        trim(path, img, (dpi, dpi))

    trimmed_images = [img.replace(".jpg", "_trimmed.jpg") for img in images]
    makePdf(pdfFileName.replace(".pdf", "_trimmed.pdf"), trimmed_images, path)

    if deleteTempFiles:
        for img in images + trimmed_images:
            os.remove(path + img)


def mergePdf(files, output):
    """Merge pdf files to one"""
    pdf_writer = PdfFileWriter()

    for path in files:
        pdf_reader = PdfFileReader(path, strict=False)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output, "wb") as fh:
        pdf_writer.write(fh)


def splitPdf(path, file, slices):
    """Split pdf files to multiple"""
    pdf_reader = PdfFileReader(path + file + ".pdf", strict=False)

    for i, pages in enumerate(slices):
        pdf_writer = PdfFileWriter()
        for page in pages:
            pdf_writer.addPage(pdf_reader.getPage(page))

        with open(path + file + "slice" + str(i) + ".pdf", "wb") as fh:
            pdf_writer.write(fh)


def trim(path, file, dpi=None):
    """Trim background from image"""
    im = Image.open(path + file)
    dpi = dpi or im.info["dpi"]

    bg = Image.new(im.mode, im.size, im.getpixel((im.size[0] - 1, im.size[1] - 1)))
    diff = ImageChops.difference(im, bg)
    # diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save(path + file.replace(".jpg", "_trimmed.jpg"), dpi=dpi)
    return bool(bbox)


def rotate(path, file, angle):
    """Rotate jpg by x degrees"""
    im = Image.open(path + file + ".jpg")
    dpi = im.info["dpi"]
    im.rotate(angle).save(path + file + "_rotated.jpg", dpi=dpi)


if __name__ == "__main__":
    path = r".\\"
    # ...
