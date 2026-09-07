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