# Generated by Django 2.2.1 on 2019-05-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textualquestion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
