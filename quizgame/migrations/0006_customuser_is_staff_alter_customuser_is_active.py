# Generated by Django 5.0.6 on 2024-06-25 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizgame', '0005_alter_leaderboard_score_alter_scores_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
