# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productfeatued_make_backround_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatued',
            name='text_css_color',
            field=models.CharField(null=True, max_length=6, blank=True),
        ),
    ]
