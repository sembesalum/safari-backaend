from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from safari.models import Package
from safari.seed_data.packages_seed import PACKAGE_SEED_DATA


class Command(BaseCommand):
    help = "Import/upsert frontend Packages page content into Package table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-missing",
            action="store_true",
            help="Archive packages that are not in the frontend seed list.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        updated = 0
        seen_titles: set[str] = set()

        for item in PACKAGE_SEED_DATA:
            title = item["title"].strip()
            seen_titles.add(title)

            defaults = {
                "subtitle": item.get("subtitle", "").strip(),
                "description": item.get("description", "").strip(),
                "duration_days": int(item.get("duration_days", 1) or 1),
                "status": item.get("status", Package.Status.ACTIVE),
                "base_price": item.get("base_price", "").strip(),
                "highlights": item.get("highlights", []),
                "itinerary": item.get("itinerary", []),
                "prices": item.get("prices", []),
                "price_groups": item.get("price_groups", []),
                "special_offers": item.get("special_offers", []),
                "important_info": item.get("important_info", []),
                "hero_image_url": item.get("hero_image_url", "").strip(),
            }

            obj, was_created = Package.objects.update_or_create(title=title, defaults=defaults)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.title}"))
            else:
                updated += 1
                self.stdout.write(f"Updated: {obj.title}")

        if options.get("reset_missing"):
            archived_count = (
                Package.objects.exclude(title__in=seen_titles)
                .exclude(status=Package.Status.ARCHIVED)
                .update(status=Package.Status.ARCHIVED)
            )
            self.stdout.write(self.style.WARNING(f"Archived missing packages: {archived_count}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Package import complete."))
        self.stdout.write(f"- Created: {created}")
        self.stdout.write(f"- Updated: {updated}")
        self.stdout.write(f"- Total in seed: {len(PACKAGE_SEED_DATA)}")
