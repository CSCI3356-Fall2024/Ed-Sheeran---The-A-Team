# Generated by Django 5.1 on 2024-11-18 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_rename_rewards_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='link',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]