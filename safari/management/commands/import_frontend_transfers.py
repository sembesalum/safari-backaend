from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from safari.models import TransferService
from safari.seed_data.transfers_seed import TRANSFER_SEED_DATA


class Command(BaseCommand):
    help = "Import/upsert frontend Transfers page content into TransferService table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-missing",
            action="store_true",
            help="Set status=draft for transfers that are not in the frontend seed list.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        updated = 0
        seen_keys: set[tuple[str, str]] = set()

        for item in TRANSFER_SEED_DATA:
            title = item["title"].strip()
            segment = item["segment"].strip()
            seen_keys.add((title, segment))

            defaults = {
                "summary": item.get("summary", "").strip(),
                "description": item.get("description", "").strip(),
                "from_price": item.get("from_price", "").strip(),
                "status": item.get("status", TransferService.Status.ACTIVE),
                "pricing_payload": item.get("pricing_payload", {}),
            }

            obj, was_created = TransferService.objects.update_or_create(
                title=title,
                segment=segment,
                defaults=defaults,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.title} [{obj.segment}]"))
            else:
                updated += 1
                self.stdout.write(f"Updated: {obj.title} [{obj.segment}]")

        if options.get("reset_missing"):
            all_ids = list(TransferService.objects.values_list("id", "title", "segment"))
            ids_to_draft = [pk for pk, t, s in all_ids if (t, s) not in seen_keys]
            drafted_count = (
                TransferService.objects.filter(id__in=ids_to_draft)
                .exclude(status=TransferService.Status.DRAFT)
                .update(status=TransferService.Status.DRAFT)
            )
            self.stdout.write(self.style.WARNING(f"Set missing transfers to draft: {drafted_count}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Transfer import complete."))
        self.stdout.write(f"- Created: {created}")
        self.stdout.write(f"- Updated: {updated}")
        self.stdout.write(f"- Total in seed: {len(TRANSFER_SEED_DATA)}")
