# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from .models import Patient
from .models import Diagnostic
from .models import Images
import datetime

class PatientForm(forms.Form):
    nom = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom",
                "class": "form-control"
            }
        ))

    prenom = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Prénom",
                "class": "form-control"
            }
        ))

    CHOICES = [('M','M'),('F','F')]
    sexe = forms.CharField(
        label='Sexe',
        widget=forms.RadioSelect(choices=CHOICES),
        initial='M'
        )

    age = forms.IntegerField(
        label='Age',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Age",
                "class": "form-control"
            }
        ))

    tel = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Telephone",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Patient
        fields = ('nom', 'prenom', 'sexe', 'age', 'tel')




class DiagnosticForm(forms.Form):
    
    libelle = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Libelle",
                "class": "form-control"
            }
        ))


    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control"
            }
        ),
        initial=datetime.date.today)
    #date = forms.DateField(initial=datetime.date.today)


    class Meta:
        model = Diagnostic
        fields = ('libelle', 'date', 'parasitemie', 'patient')





class ImageForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"multiple": True,
                    "class": "form-control",
                    }))    

    class Meta:
        model = Images
        fields = ('image', 'diagnostic')