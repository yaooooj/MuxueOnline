# Generated by Django 2.0.2 on 2018-04-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180412_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')], default='pxjg', max_length=20, verbose_name='类别'),
        ),
    ]
