# Generated by Django 3.0.3 on 2020-02-08 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200208_0457'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorreading',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sensorreading',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='sensorreading',
            unique_together={('name', 'updated')},
        ),
    ]
