from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("safari", "0002_expand_cms_and_booking_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="package",
            name="image_urls",
            field=models.JSONField(blank=True, default=list, help_text='Additional image URLs: ["https://...", ...]'),
        ),
        migrations.AddField(
            model_name="tour",
            name="image_urls",
            field=models.JSONField(blank=True, default=list, help_text='Additional image URLs: ["https://...", ...]'),
        ),
    ]
