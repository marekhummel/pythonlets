import os
from pathlib import Path

from fpdf import FPDF
from pdf2image import convert_from_path  # type: ignore
from PIL import Image, ImageChops
from pypdf import PdfReader, PdfWriter


def merge_pdfs(root: Path, files: list[str], output: str) -> None:
    """Merge pdf files to one"""
    pdf_writer = PdfWriter()

    for path in files:
        pdf_reader = PdfReader(root / path, strict=False)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    with open(root / output, "wb") as fh:
        pdf_writer.write(fh)


def split_pdf(file: Path, slices: list[list[int]]) -> None:
    """Split pdf files to multiple"""
    pdf_reader = PdfReader(file, strict=False)

    for i, page_slice in enumerate(slices):
        pdf_writer = PdfWriter()
        for page_idx in page_slice:
            pdf_writer.add_page(pdf_reader.pages[page_idx])

        with open(file.with_stem(f"{file.stem}_slice{i}"), "wb") as fh:
            pdf_writer.write(fh)


def rotate_pdf(file: Path, angle_cw: int):
    file_in, file_out = _backup_original(file)

    # Read and rotate
    with open(file_in, "rb") as pdf_in:
        pdf_reader = PdfReader(pdf_in, strict=False)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            page.rotate(angle_cw)
            pdf_writer.add_page(page)

        # Write
        with open(file_out, "wb") as pdf_out:
            pdf_writer.write(pdf_out)


def images_to_pdf(root: Path, image_files: list[str], output: str) -> None:
    """List of jpg files to pdf"""
    pdf = FPDF(unit="pt")

    for page in image_files:
        img_path = root / page

        cover = Image.open(img_path)
        width, height = cover.size
        pdf.add_page(format=(width, height))
        pdf.image(img_path, 0, 0)

    pdf.output(str(root / output))


def trim_pages_pdf(file: Path, deleteTempFiles: bool = True, bbox: tuple[int, int, int, int] | None = None):
    """Applies the trim function on pages of a pdf"""
    pdf_file_in, pdf_file_out = _backup_original(file)
    directory = file.parent

    dpi = 300
    pages = convert_from_path(str(pdf_file_in), dpi)
    images: list[str] = []
    trimmed_images: list[str] = []
    for i, page in enumerate(pages):
        img_name = f"page{i}.jpg"
        images.append(img_name)
        page.save(pdf_file_in.parent / img_name, "JPEG")

        trimmed_image_file = _trim_image(directory / img_name, (dpi, dpi), bbox)
        trimmed_images.append(trimmed_image_file.name if trimmed_image_file else img_name)

    images_to_pdf(pdf_file_in.parent, trimmed_images, pdf_file_out.name)
    if deleteTempFiles:
        for img in set(images + trimmed_images):
            os.remove(img)


def _trim_image(file: Path, dpi=None, bbox_man: tuple[int, int, int, int] | None = None) -> Path | None:
    """Trim background from image"""
    im = Image.open(file)
    dpi = dpi or im.info["dpi"]

    if bbox_man:
        width, height = im.size
        left, upper, right, lower = bbox_man
        bbox = (left * width, upper * height, right * width, lower * height)
    else:
        bg = Image.new(im.mode, im.size, im.getpixel((im.size[0] - 1, im.size[1] - 1)))
        diff = ImageChops.difference(im, bg)
        # diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()

    if bbox:
        im = im.crop(bbox)
        trimmed_file = file.with_stem(f"{file.stem}_trimmed")
        im.save(trimmed_file, dpi=dpi)
        return trimmed_file

    return None


def rotate_image(file: Path, angle: int) -> None:
    """Rotate jpg by x degrees"""
    file_in, file_out = _backup_original(file)

    im = Image.open(file_in)
    dpi = im.info["dpi"]
    im.rotate(angle, expand=True).save(file_out, dpi=dpi)


def _backup_original(file: Path) -> tuple[Path, Path]:
    orig_file = file.with_stem(f"{file.stem}_orig")
    file.rename(orig_file)
    return orig_file, file


if __name__ == "__main__":
    root = Path(r".\\")
    # ...
