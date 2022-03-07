# Generated by Django 3.1.14 on 2022-02-23 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0006_auto_20190304_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('view_resourcestatistics', 'Can view resource statistics')],
                'verbose_name': 'Common permission'
            },
        ),
    ]