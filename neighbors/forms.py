from django import forms


class UploadNeighborsForm(forms.Form):
    """A form for uploading sites from the file."""

    choices = (
        ('', '----------'),
        ('ENM2', 'ENM2'),
        ('ENM4', 'ENM4'),
    )

    enm = forms.ChoiceField(choices=choices, required=True)
    neighbors_excel = forms.FileField()
