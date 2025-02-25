from django.db import models  # type: ignore


class Operator(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SitesByOperator(models.Model):
    created_at = models.DateField()
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.IntegerField()

    class Meta:
        unique_together = ('created_at', 'operator', 'technology')

    def __str__(self):
        return f"{self.operator}-{self.technology}: {self.site_count}"


class SitesByVendor(models.Model):
    created_at = models.DateField()
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.IntegerField()

    class Meta:
        unique_together = ('created_at', 'vendor', 'technology')

    def __str__(self):
        return f"{self.vendor}-{self.technology}: {self.site_count}"


class SitesByRegion(models.Model):
    created_at = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.IntegerField()

    class Meta:
        unique_together = ('created_at', 'region', 'technology')

    def __str__(self):
        return f"{self.region}-{self.technology}: {self.site_count}"


class SitesByOperatorAndRegion(models.Model):
    created_at = models.DateField()
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    technology = models.ForeignKey(Technology, on_delete=models.PROTECT)
    site_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('created_at', 'operator', 'region', 'technology')

    def __str__(self):
        return f"{self.operator}-{self.region}-{self.technology}: {self.site_count}"
