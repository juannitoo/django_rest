# Generated by Django 4.2.7 on 2023-11-19 14:26

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children",
                to="api.category",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(verbose_name="Slug"),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="categories",
            field=models.ManyToManyField(
                related_name="categories", to="api.category", verbose_name="categories"
            ),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="slug",
            field=models.SlugField(verbose_name="Slug"),
        ),
    ]
