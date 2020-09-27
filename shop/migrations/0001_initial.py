# Generated by Django 3.0.8 on 2020-09-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=100)),
                ('description', models.CharField(default='', max_length=100)),
                ('image', models.ImageField(upload_to='products/images/')),
            ],
        ),
    ]
