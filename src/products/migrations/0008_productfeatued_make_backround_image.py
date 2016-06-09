# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productfeatued'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatued',
            name='make_backround_image',
            field=models.BooleanField(default=False),
        ),
    ]
