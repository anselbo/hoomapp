# Generated by Django 3.1.5 on 2021-04-09 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homapp', '0007_auto_20210409_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(blank=True, default='No category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='homapp.taskcategory'),
        ),
    ]
