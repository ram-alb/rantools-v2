from django import forms


class SelectTables(forms.Form):
    """A form for uploading sites from the file."""

    choices = (
        ('lte', 'LTE Cells'),
        ('wcdma', 'WCDMA Cells'),
        ('gsm', 'GSM Cells'),
        ('nr', 'NR Cells'),
    )

    tech = forms.BooleanField(choices=choices, required=False)
