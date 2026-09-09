from django import forms

TEXT_INPUT_CLASSES = (
    "w-full border border-navy/20 rounded-lg px-4 py-2.5 font-body text-sm "
    "focus:outline-none focus:ring-2 focus:ring-gold"
)
CHECKBOX_CLASSES = "rounded border-navy/30 text-gold focus:ring-gold"


class TailwindStyledFormMixin:
    """
    Applies consistent dashboard form styling to every field
    automatically on __init__, so individual ModelForms don't need
    per-field widget attrs written out by hand. Reused across every
    dashboard content form from this step onward.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = f"{existing} {CHECKBOX_CLASSES}".strip()
            elif isinstance(widget, forms.ClearableFileInput):
                pass  # leave file inputs as browser default — styling these well needs more than a class
            else:
                widget.attrs["class"] = f"{existing} {TEXT_INPUT_CLASSES}".strip()