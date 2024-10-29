# Generated by Django 5.1.1 on 2024-10-04 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('code', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
