# Generated by Django 5.1.1 on 2024-09-26 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.tag'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.tag'),
        ),
    ]
