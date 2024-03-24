# Generated by Django 5.0.3 on 2024-03-24 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('admin_mobile', models.IntegerField(default=True, unique=True)),
                ('pin', models.IntegerField()),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]