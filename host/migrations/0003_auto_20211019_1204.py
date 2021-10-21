# Generated by Django 3.1.5 on 2021-10-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0002_auto_20211015_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100)),
                ('quizId', models.IntegerField()),
                ('gameId', models.TextField()),
                ('gameTime', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameId', models.CharField(max_length=10)),
                ('quizId', models.IntegerField()),
                ('marks', models.TextField()),
                ('playername', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='quiz',
            name='answer',
            field=models.CharField(max_length=5),
        ),
    ]