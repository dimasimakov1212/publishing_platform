# Generated by Django 4.2.7 on 2023-11-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_description',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Краткое описание'),
        ),
    ]
