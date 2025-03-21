# Generated by Django 3.2 on 2025-03-12 22:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Оценка должна быть от 1 до 10'), django.core.validators.MaxValueValidator(10, message='Оценка должна быть от 1 до 10')], verbose_name='Оценка'),
        ),
    ]
