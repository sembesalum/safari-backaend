from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from safari.models import Tour
from safari.seed_data.tours_seed import TOUR_SEED_DATA


class Command(BaseCommand):
    help = "Import/upsert frontend Tours page content into Tour table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-missing",
            action="store_true",
            help="Set status=draft for tours that are not in the frontend seed list.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        updated = 0
        seen_titles: set[str] = set()

        for item in TOUR_SEED_DATA:
            title = item["title"].strip()
            seen_titles.add(title)

            defaults = {
                "category": item.get("category", "General").strip() or "General",
                "description": item.get("description", "").strip(),
                "includes": item.get("includes", "").strip(),
                "highlights": item.get("highlights", []),
                "bonuses": item.get("bonuses", []),
                "prices": item.get("prices", []),
                "from_price": item.get("from_price", "").strip(),
                "status": item.get("status", Tour.Status.ACTIVE),
                "hero_image_url": item.get("hero_image_url", "").strip(),
            }

            obj, was_created = Tour.objects.update_or_create(title=title, defaults=defaults)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.title}"))
            else:
                updated += 1
                self.stdout.write(f"Updated: {obj.title}")

        if options.get("reset_missing"):
            drafted_count = (
                Tour.objects.exclude(title__in=seen_titles).exclude(status=Tour.Status.DRAFT).update(status=Tour.Status.DRAFT)
            )
            self.stdout.write(self.style.WARNING(f"Set missing tours to draft: {drafted_count}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Tour import complete."))
        self.stdout.write(f"- Created: {created}")
        self.stdout.write(f"- Updated: {updated}")
        self.stdout.write(f"- Total in seed: {len(TOUR_SEED_DATA)}")
