# Generated by Django 3.1.5 on 2021-10-15 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20211015_0746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='Emai_Id',
            new_name='email_id',
        ),
    ]
