# Generated by Django 3.2.12 on 2022-07-24 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_profiles_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profil'),
        ),
    ]
