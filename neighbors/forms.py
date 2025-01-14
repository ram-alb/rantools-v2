from django import forms


class UploadNeighborsForm(forms.Form):
    """A form for uploading sites from the file."""

    choices = (
        ('', '----------'),
        ('ENM_2', 'ENM_2'),
        ('ENM_4', 'ENM_4'),
    )

    enm = forms.ChoiceField(choices=choices, required=True)
    neighbors_excel = forms.FileField()
