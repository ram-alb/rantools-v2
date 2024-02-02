from django import forms


class UploadNeighborsForm(forms.Form):
    """A form for uploading sites from the file."""

    neighbors_excel = forms.FileField()
