# Generated by Django 3.2.7 on 2022-02-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsite', '0004_remove_comment_temporary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='remarks',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='备注信息'),
        ),
    ]
