# Generated by Django 2.1.7 on 2019-03-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitterapp', '0005_auto_20190322_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dweeter',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='_dweeter_follows_+', to='dwitterapp.Dweeter'),
        ),
    ]
