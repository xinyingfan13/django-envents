# Generated by Django 5.0.1 on 2024-03-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0008_voting_author_alter_message_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(help_text='Укажите вашу дату рождения', null=True, verbose_name='Дата рождения'),
        ),
    ]
