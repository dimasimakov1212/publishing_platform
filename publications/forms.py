from django import forms

from publications.models import Publication


class PublicationForm(forms.ModelForm):
    """ Создает форму для создания товара """

    class Meta:
        """ Определяет параметры формы """

        model = Publication

        fields = ('publication_title', 'publication_text', 'publication_photo', 'is_public', 'publication_price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
