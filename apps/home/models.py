# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
from django.db import models

# Create your models here.

def get_upload_path(instance, filename):
    return os.path.join(
      "user_%d" % instance.owner.id, "car_%s" % instance.slug, filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def get_image_filename(instance, filename):
    title = instance.diagnostic.patient.id
    return 'images_{0}/{1}/{2}'.format(instance.diagnostic.patient.id, instance.diagnostic.id, filename)


class Patient(models.Model):
    nom = models.CharField(max_length = 50)
    prenom = models.CharField(max_length = 50)
    sexe = models.CharField(max_length = 1)
    age = models.CharField(max_length = 20)
    tel = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.nom, self.prenom)

    class Meta :
        db_table = "patient"


class Diagnostic(models.Model):
    libelle = models.CharField(max_length = 20)
    date = models.DateField()
    parasitemie = models.IntegerField()
    patient = models.ForeignKey('Patient', default = 1,on_delete=models.CASCADE,)

    def __str__(self):
        return self.libelle
   
    class Meta :
        db_table = "diagnostic"


class Images(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, default=None,on_delete=models.DO_NOTHING,)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
    #image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.diagnostic

    class Meta :
        db_table = "images"