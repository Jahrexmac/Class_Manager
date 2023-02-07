# Generated by Django 4.0.8 on 2023-02-04 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('form_teacher', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('parent_name', models.CharField(max_length=50)),
                ('parent_phone_number', models.CharField(max_length=11)),
                ('house_address', models.CharField(max_length=200)),
                ('religion', models.CharField(max_length=15)),
                ('profile_picture', models.ImageField(default='', upload_to='images')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('first_test', models.IntegerField()),
                ('second_test', models.IntegerField()),
                ('exam', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.student')),
            ],
        ),
    ]
