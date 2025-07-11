from django import forms
from .models import Blog
from .models import Commentaire

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titre', 'description', 'type', 'photo'] 

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu', 'evaluation']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'}),
            'evaluation': forms.RadioSelect(
                attrs={'class': 'star-rating'},
                choices=[(i, '★') for i in range(1, 6)]
            ),
        } 