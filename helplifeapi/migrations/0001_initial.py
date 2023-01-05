# Generated by Django 4.1.3 on 2023-01-05 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CareTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_tip_label', models.CharField(max_length=50)),
                ('description_of_tip', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='HelpLifeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('profile_image_url', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=False)),
                ('new_plant_care', models.CharField(max_length=250)),
                ('plant_age', models.CharField(max_length=50)),
                ('plant_name', models.CharField(max_length=50)),
                ('plant_image', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlantPlantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helplifeapi.plant')),
                ('plant_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helplifeapi.planttype')),
            ],
        ),
        migrations.CreateModel(
            name='PlantCareTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('care_tip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helplifeapi.caretip')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helplifeapi.plant')),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='care_tips',
            field=models.ManyToManyField(related_name='SpecificPlantCareTip', through='helplifeapi.PlantCareTip', to='helplifeapi.caretip'),
        ),
        migrations.AddField(
            model_name='plant',
            name='plant_types',
            field=models.ManyToManyField(related_name='SpecificPlantType', through='helplifeapi.UserPlantPlantType', to='helplifeapi.planttype'),
        ),
        migrations.AddField(
            model_name='plant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helplifeapi.helplifeuser'),
        ),
    ]
