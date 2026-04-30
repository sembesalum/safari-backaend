from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("safari", "0003_package_tour_image_urls"),
    ]

    operations = [
        migrations.CreateModel(
            name="PackageImage",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("image", models.ImageField(blank=True, null=True, upload_to="packages/gallery/")),
                ("image_url", models.URLField(blank=True, max_length=2000)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "package",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gallery_images", to="safari.package"),
                ),
            ],
            options={
                "ordering": ["sort_order", "created_at"],
            },
        ),
        migrations.CreateModel(
            name="TourImage",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("image", models.ImageField(blank=True, null=True, upload_to="tours/gallery/")),
                ("image_url", models.URLField(blank=True, max_length=2000)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "tour",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gallery_images", to="safari.tour"),
                ),
            ],
            options={
                "ordering": ["sort_order", "created_at"],
            },
        ),
    ]
