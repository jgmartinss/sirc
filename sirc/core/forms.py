from django import forms

from . import models


class ContatoForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": True,
                "placeholder": "Nome",
                "required": True,
                "data-validation-required-message": "Por favor, insira seu nome.",
            }
        ),
    )

    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "required": True,
                "data-validation-required-message": "Por favor, insira o seu e-mail.",
            }
        ),
    )

    assunto = forms.CharField(
        label="Assunto",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Assunto",
                "required": True,
                "data-validation-required-message": "Por favor, insira o assunto de contato.",
            }
        ),
    )

    menssagem = forms.CharField(
        label="Menssagem",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Menssagem",
                "required": True,
                "data-validation-required-message": "Por favor, insira a sua menssagem.",
                "rows": 5,
            }
        ),
    )

    class Meta:
        model = models.Contato
        fields = "__all__"
