# Generated by Django 3.2.14 on 2022-07-28 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0017_auto_20220623_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyapplicationticket',
            name='apply_permission_name',
            field=models.CharField(max_length=128, verbose_name='Permission name'),
        ),
        migrations.AlterField(
            model_name='applyassetticket',
            name='apply_permission_name',
            field=models.CharField(max_length=128, verbose_name='Permission name'),
        ),
    ]