# Generated by Django 3.1.5 on 2021-04-02 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homapp', '0002_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default='Add some description'),
        ),
    ]
