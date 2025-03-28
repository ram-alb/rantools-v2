from django.db import models  # type: ignore


class RadioEquipmentClockReference(models.Model):
    """Represent RadioEquipmentClockReference MO data."""

    enm_max_len = 6
    max_len = 50

    enm = models.CharField(max_length=enm_max_len)
    node_id = models.CharField(max_length=max_len)
    radio_equipment_clock_reference_id = models.IntegerField()
    reference_status = models.CharField(max_length=max_len)
    sync_ref_type = models.CharField(max_length=max_len)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["enm", "node_id", "radio_equipment_clock_reference_id"],
            ),
        ]

    def __str__(self):
        """Return string representation of RadioEquipmentClockReference."""
        return (
            f"{self.node_id}-{self.sync_ref_type}: {self.reference_status}"
            f"(Updated: {self.updated_at})"
        )
