# Generated by Django 5.1.3 on 2025-06-24 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=150, null=True)),
                ('first', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email Address')),
                ('message', models.TextField(null=True, verbose_name='Your comment, question, or proposal')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
