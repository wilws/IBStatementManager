# Generated by Django 4.0.2 on 2022-05-19 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statementReader', '0018_alter_document_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='document',
        ),
        migrations.RemoveField(
            model_name='document',
            name='uploaded_at',
        ),
        migrations.AddField(
            model_name='document',
            name='a',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
