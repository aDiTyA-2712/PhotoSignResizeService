# Generated by Django 5.0.1 on 2024-09-15 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='uploads/')),
                ('desired_width', models.IntegerField()),
                ('desired_height', models.IntegerField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_resized', models.BooleanField(default=False)),
            ],
        ),
    ]
