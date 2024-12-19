from django.db import models
from django.contrib.auth.models import User
from django.db import models, connection


class FolderManager(models.Manager):
    def fetch_by_user(self, user_id):
        # Raw SQL query
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM drive_folder WHERE owner_id = %s", [user_id])
            return cursor.fetchall()

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = FolderManager()

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
