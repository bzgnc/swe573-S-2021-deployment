# Generated by Django 3.2.4 on 2021-06-26 22:57

import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastName', models.CharField(max_length=128)),
                ('ForeName', models.CharField(max_length=128, null=True)),
                ('Initials', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISSN', models.CharField(max_length=16)),
                ('Title', models.CharField(max_length=256)),
                ('ISOAbbreviation', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('KeywordText', models.TextField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WikiID', models.CharField(max_length=64)),
                ('Label', models.CharField(max_length=64)),
                ('Description', models.TextField(max_length=1024, null=True)),
                ('Tokens', models.TextField(max_length=1024, null=True)),
                ('SearchIndex', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PMID', models.CharField(max_length=16)),
                ('Title', models.TextField(max_length=512)),
                ('Abstract', models.TextField(max_length=5000, null=True)),
                ('PublicationDate', models.DateField(null=True)),
                ('Tokens', models.TextField(max_length=100000)),
                ('SearchIndex', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('Authors', models.ManyToManyField(to='medtagger.Author')),
                ('Journal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='medtagger.journal')),
                ('Keywords', models.ManyToManyField(to='medtagger.Keyword')),
                ('Tags', models.ManyToManyField(to='medtagger.Tag')),
            ],
        ),
    ]