# Generated by Django 5.0.6 on 2024-06-25 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizgame', '0006_customuser_is_staff_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
