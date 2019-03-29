from django.db import models


# A model of provide processing history
class ProcessingHistory(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    processing_image = models.FileField(db_column='processing_image')
    created_at = models.DateTimeField(db_column='created_at')


# A model of provide processing result
class ProcessingResult(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    history_id = models.ForeignKey(ProcessingHistory, on_delete=models.CASCADE)
    type = models.TextField(db_column='type')
    content = models.TextField(db_column='content')
