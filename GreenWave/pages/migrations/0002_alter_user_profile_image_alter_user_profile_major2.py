# Generated by Django 5.1 on 2024-10-21 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='image',
            field=models.ImageField(upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='major2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]