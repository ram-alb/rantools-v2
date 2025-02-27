from django.db import models  # type: ignore

MAX_LENGTH = 30


class Operator(models.Model):
    """Represent a mobile network operator."""

    name = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        """Return the string representation of the operator (its name)."""
        return self.name


class Technology(models.Model):
    """Represent a mobile network technology."""

    name = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        """Return the string representation of the technology (its name)."""
        return self.name


class Vendor(models.Model):
    """Represent an equipment vendor."""

    name = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        """Return the string representation of the vendor (its name)."""
        return self.name


class Region(models.Model):
    """Represent a region."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return the string representation of the region (its name)."""
        return self.name


class SitesByOperator(models.Model):
    """Represent the number of sites grouped by operator."""

    created_at = models.DateField()
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.IntegerField()

    class Meta:
        unique_together = ('created_at', 'operator', 'technology')

    def __str__(self):
        """Return a string representation of the operator, technology, and site count."""
        return f"{self.operator}-{self.technology}: {self.site_count}"


class SitesByVendor(models.Model):
    """Represent the number of sites grouped by vendor."""

    created_at = models.DateField()
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.IntegerField()

    class Meta:
        unique_together = ('created_at', 'vendor', 'technology')

    def __str__(self):
        """Return a string representation of the vendor, technology, and site count."""
        return f"{self.vendor}-{self.technology}: {self.site_count}"


class SitesByRegion(models.Model):
    """Represent the number of sites grouped by region."""

    created_at = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.IntegerField()

    class Meta:
        unique_together = ('created_at', 'region', 'technology')

    def __str__(self):
        """Return a string representation of the region, technology, and site count."""
        return f"{self.region}-{self.technology}: {self.site_count}"


class SitesByOperatorAndRegion(models.Model):
    """Represent the number of sites grouped by operator and region."""

    created_at = models.DateField()
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('created_at', 'operator', 'region', 'technology')

    def __str__(self):
        """Return a string representation of the operator, region, technology, and site count."""
        return f"{self.operator}-{self.region}-{self.technology}: {self.site_count}"
