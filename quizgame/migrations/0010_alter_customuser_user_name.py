# Generated by Django 5.0.6 on 2024-06-26 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizgame', '0009_delete_googlecredential'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_name',
            field=models.CharField(max_length=70, unique=True),
        ),
    ]
