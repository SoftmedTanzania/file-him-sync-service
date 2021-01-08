from django.db import models


# Create your models here.
class Mediator(models.Model):
    def __str__(self):
        return '%s' %self.mediator_name

    mediator_name = models.CharField(max_length=255)
    details = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Mediators'

class File(models.Model):
    def __str__(self):
        return '%d' %self.id

    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=255)
    end_point = models.TextField()

    class Meta:
        db_table = 'Files'


class FilePath(models.Model):
    def __str__(self):
        return '%d' %self.id

    In = 'in_dir'
    Out = 'out_dir'
    Err = 'err_dir'
    Root = 'root_dir'

    PATH_CHOICES = (
        (In, 'Input Directory'),
        (Out, 'Output Directory'),
        (Err, 'Error Directory'),
        (Root, 'Root Directory')
    )

    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE, null=True, blank=True)
    file_path = models.TextField()
    path_type = models.CharField(max_length=100, choices=PATH_CHOICES)

    class Meta:
        db_table = 'FilePaths'




