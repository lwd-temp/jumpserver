# Generated by Django 4.1.10 on 2023-08-10 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0065_session_command_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applet',
            name='edition',
        ),
        migrations.AddField(
            model_name='applet',
            name='enterprise',
            field=models.BooleanField(default=False, verbose_name='Enterprise'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(choices=[('kill_session', 'Kill Session'), ('lock_session', 'Lock Session'), ('unlock_session', 'Unlock Session')], max_length=128, verbose_name='Name'),
        ),
    ]
