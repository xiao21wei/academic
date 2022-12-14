# Generated by Django 4.1.3 on 2022-12-13 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="achievement", old_name="author_id", new_name="author",
        ),
        migrations.AddField(
            model_name="achievement", name="hot", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="achievement",
            name="recommend",
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name="user", name="birthday", field=models.DateField(null=True),
        ),
    ]
