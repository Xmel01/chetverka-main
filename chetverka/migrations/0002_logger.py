# Generated by Django 4.0.4 on 2022-06-16 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chetverka', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='logger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Время записи')),
                ('log', models.CharField(max_length=500, verbose_name='Лог')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]