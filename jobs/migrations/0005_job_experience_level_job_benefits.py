from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0004_usersettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="benefits",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="job",
            name="experience_level",
            field=models.CharField(
                choices=[
                    ("entry-level", "Entry level"),
                    ("mid-level", "Mid level"),
                    ("senior", "Senior"),
                ],
                default="mid-level",
                max_length=20,
            ),
        ),
    ]