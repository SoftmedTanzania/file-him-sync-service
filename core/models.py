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

    mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE, null=True, blank=True)
    directory_path = models.TextField()

    class Meta:
        db_table = 'FilePaths'




