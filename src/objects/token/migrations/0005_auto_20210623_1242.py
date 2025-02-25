# Generated by Django 2.2.20 on 2021-06-23 10:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("token", "0004_auto_20210315_1537"),
    ]

    operations = [
        migrations.AddField(
            model_name="permission",
            name="fields",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=30, verbose_name="field"),
                blank=True,
                default=list,
                help_text="Fields allowed for this token. Supports only first level of the `record.data` properties",
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="permission",
            name="use_fields",
            field=models.BooleanField(
                default=False,
                help_text="Use field-based authorization",
                verbose_name="use fields",
            ),
        ),
    ]
