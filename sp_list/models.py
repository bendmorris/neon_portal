from django.db import models
from django import forms
from django.contrib.auth.models import User
from neon_portal.settings import APP_HOME_DIR
import os

# Create your models here.

class SpListDocument(models.Model):
    docfile = models.FileField(
        upload_to=os.path.join(APP_HOME_DIR, 'documents/'),
        verbose_name='Select a file',
        help_text='File should be a properly formatted species list CSV. Max size 50mb.',
        #allow_empty_file=False,
    )

    def filename(self):
        return os.path.basename(self.docfile.name)
    
    CHOICES = [('mammals', 'Mammals'), ('birds', 'Birds'), ('plants', 'Plants'), ('inverts', 'Invertebrates'), ('herps', 'Herps')]
    tax_group = models.CharField(max_length = max([len(l[0]) for l in CHOICES]), choices=CHOICES, default=CHOICES[0][1])
    
    comments = models.TextField(max_length=255, blank=True)
    
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by')
    upload_time = models.DateTimeField(auto_now_add=True)
    
    
class ProcessingJob(models.Model):
    user = models.ForeignKey(User, related_name='user')
    start_time = models.DateTimeField(auto_now_add=True)
    documents = models.CharField(max_length=255, blank=False)
    status = models.CharField(max_length=255, default='Pending')
