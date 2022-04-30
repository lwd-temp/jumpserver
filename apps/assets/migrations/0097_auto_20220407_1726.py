# Generated by Django 3.1.14 on 2022-04-07 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0096_auto_20220406_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='base',
            new_name='type',
        ),
        migrations.AddField(
            model_name='platform',
            name='category',
            field=models.CharField(choices=[('host', 'Host'), ('network', 'Networking'), ('database', 'Database'), ('remote_app', 'Remote app'), ('cloud', 'Clouding')], default='host', max_length=16, verbose_name='Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='platform',
            name='type',
            field=models.CharField(choices=[('linux', 'Linux'), ('windows', 'Windows'), ('unix', 'Unix'), ('bsd', 'BSD'), ('macos', 'MacOS'), ('mainframe', 'Mainframe'), ('other_host', 'Other host'), ('switch', 'Switch'), ('router', 'Router'), ('firewall', 'Firewall'), ('other_network', 'Other device'), ('mysql', 'MySQL'), ('mariadb', 'MariaDB'), ('postgresql', 'PostgreSQL'), ('oracle', 'Oracle'), ('sqlserver', 'SQLServer'), ('mongodb', 'MongoDB'), ('redis', 'Redis'), ('chrome', 'Chrome'), ('vmware_client', 'vSphere client'), ('mysql_workbench', 'MySQL workbench'), ('general_remote_app', 'Custom'), ('k8s', 'Kubernetes')], default='Linux', max_length=32, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='systemuser',
            name='protocol',
            field=models.CharField(choices=[('ssh', 'SSH'), ('rdp', 'RDP'), ('telnet', 'Telnet'), ('vnc', 'VNC'), ('mysql', 'MySQL'), ('mariadb', 'MariaDB'), ('oracle', 'Oracle'), ('postgresql', 'PostgreSQL'), ('sqlserver', 'SQLServer'), ('redis', 'Redis'), ('mongodb', 'MongoDB'), ('k8s', 'K8S')], default='ssh', max_length=16, verbose_name='Protocol'),
        ),
    ]