# Generated by Django 4.0.9 on 2023-02-10 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='perm',
            field=models.IntegerField(choices=[(0, 'USER'), (1, 'ADMIN'), (2, 'HELPER')], default=0),
        ),
        migrations.DeleteModel(
            name='ChangedPassword',
        ),
        migrations.DeleteModel(
            name='Code',
        ),
    ]
