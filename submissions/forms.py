from django import forms
from .models import Submission, Genre


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['song_title', 'artist_name', 'genre', 'description', 'audio_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell the producer about this song...'}),
            'song_title': forms.TextInput(attrs={'placeholder': 'Song title'}),
            'artist_name': forms.TextInput(attrs={'placeholder': 'Your artist/stage name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].queryset = Genre.objects.filter(is_active=True)

    def clean_audio_file(self):
        audio = self.cleaned_data.get('audio_file')
        if audio:
            ext = audio.name.split('.')[-1].lower()
            if ext not in ['mp3', 'wav', 'flac', 'aiff']:
                raise forms.ValidationError('Only MP3, WAV, FLAC, or AIFF files are accepted.')
            if audio.size > 52428800:
                raise forms.ValidationError('File size must be under 50MB.')
        return audio
