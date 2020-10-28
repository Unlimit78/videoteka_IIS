from django.forms import ModelForm

from .models import VideoCasets

class VideoForm(ModelForm):
    class Meta:
        model = VideoCasets
        fields='__all__'
