# Generated by Django 5.0.3 on 2024-10-23 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rag', '0002_chun'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='choice',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
