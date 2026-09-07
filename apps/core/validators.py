import os

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_SIZE_MB = 3


def validate_image_file(file):
    """
    Validates an uploaded image by:
      1. Extension allow-list (rejects .svg, .php, .exe renamed to .jpg, etc.)
      2. File size cap (per §28 — church sites accumulate a lot of photos;
         cap keeps storage and page-load performance sane)
      3. Actually opening the file with Pillow and verifying it decodes as
         a real image — this is our "magic bytes" check per §37/§27. A
         file with a .jpg extension that is actually an executable or a
         script will fail here even though the extension check passed.

    Raises ValidationError with a clear message if any check fails.
    Use on any ImageField across the project: `validators=[validate_image_file]`.
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '{ext}'. Allowed types: "
            f"{', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}."
        )

    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if file.size > max_bytes:
        raise ValidationError(f"Image must be smaller than {MAX_IMAGE_SIZE_MB}MB.")

    try:
        file.seek(0)
        image = Image.open(file)
        image.verify()  # raises if the content isn't a genuine, undamaged image
    except (UnidentifiedImageError, OSError):
        raise ValidationError(
            "This file isn't a valid image, even though its extension suggests it is."
        )
    finally:
        file.seek(0)  # reset pointer so Django can still save the file afterward

MAX_PDF_SIZE_MB = 20


def validate_pdf_file(file):
    """
    Validates an uploaded PDF (sermon notes, per §16's 'download
    permitted resources'). Extension allow-list + size cap + a real
    file-signature check — PDFs start with the bytes '%PDF-', so a
    renamed .exe or .html file wearing a .pdf extension is rejected
    even though the extension check alone would pass it.
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext != ".pdf":
        raise ValidationError(f"Unsupported file type '{ext}'. Only PDF files are allowed.")

    max_bytes = MAX_PDF_SIZE_MB * 1024 * 1024
    if file.size > max_bytes:
        raise ValidationError(f"PDF must be smaller than {MAX_PDF_SIZE_MB}MB.")

    file.seek(0)
    header = file.read(5)
    file.seek(0)
    if header != b"%PDF-":
        raise ValidationError(
            "This file isn't a valid PDF, even though its extension suggests it is."
        )


ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav"}
MAX_AUDIO_SIZE_MB = 50


def validate_audio_file(file):
    """
    Validates uploaded sermon audio. Extension allow-list + size cap.
    (No deep content-signature check here, unlike images/PDFs — audio
    container formats vary too much for a simple magic-bytes check to
    be reliable without an extra dependency; extension + size is the
    practical, proportionate control for this file type.)
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise ValidationError(
            f"Unsupported audio type '{ext}'. Allowed types: "
            f"{', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}."
        )
    max_bytes = MAX_AUDIO_SIZE_MB * 1024 * 1024
    if file.size > max_bytes:
        raise ValidationError(f"Audio file must be smaller than {MAX_AUDIO_SIZE_MB}MB.")