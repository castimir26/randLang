# Generated by Django 2.2.2 on 2019-07-28 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('randLang', '0004_auto_20190728_1032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dict_words',
            options={'verbose_name_plural': 'Dict_Words'},
        ),
        migrations.AlterModelOptions(
            name='user_created',
            options={'verbose_name_plural': 'User_Created'},
        ),
    ]