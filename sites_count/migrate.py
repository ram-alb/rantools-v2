import csv
from datetime import datetime

from sites_count.models import (
    Operator,
    Region,
    SitesByOperator,
    SitesByRegion,
    SitesByVendor,
    Technology,
    Vendor,
)

OPERATORS = {
    "kcell": "Kcell",
    "tele2": "Tele2",
    "beeline": "Beeline"
}

TECHNOLOGIES = {
    "gsm": "GSM",
    "wcdma": "WCDMA",
    "lte": "LTE",
    "nr5g": "NR",
    "iot": "IoT",
    'total': "Total",
}

VENDORS = {
    'ericsson': 'Ericsson',
    'huawei': 'Huawei',
    'zte': 'ZTE',
    'nokia': 'Nokia',
}

REGIONS = {
    "abay_region": "Abai-region",
    "akmola_region": "Akmola-region",
    "aktobe_region": "Aktobe-region",
    "almaty_city": "Almaty-city",
    "almaty_region": "Almaty-region",
    "astana": "Astana",
    "atyrau_region": "Atyrau-region",
    "east_kz_region": "East-Kazakhstan-region",
    "zhetysu_region": "Jetysu-region",
    "karaganda_region": "Karaganda-region",
    "kostanay_region": "Kostanay-region",
    "kyzylorda_region": "Kyzylorda-region",
    "mangystau_region": "Mangystau-region",
    "north_kz_region": "North-Kazakhstan-region",
    "pavlodar_region": "Pavlodar-region",
    "shymkent": "Shymkent",
    "turkestan_region": "Turkestan-region",
    "ulytau_region": "Ulytau-region",
    "west_kz_region": "West-Kazakhstan-region",
    "zhambyl_region": "Zhambyl-region",
}



def migrate_by_operators():
    for name in OPERATORS.values():
        Operator.objects.get_or_create(name=name)

    for tech in TECHNOLOGIES.values():
        Technology.objects.get_or_create(name=tech)

    operators = {op.name: op for op in Operator.objects.all()}
    technologies = {tech.name: tech for tech in Technology.objects.all()}

    with open('sites_by_operators.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = []

        for row in reader:
            created_at = datetime.strptime(row['CREATED_AT'], '%Y-%m-%d %H:%M:%S.%f').date()
            for op_key, op_name in OPERATORS.items():
                for tech_key, tech_name in TECHNOLOGIES.items():
                    column_name = f'{op_key}_{tech_key}'.upper()
                    try:
                        site_count = int(row[column_name]) if row[column_name] else 0
                    except KeyError:
                        site_count = 0

                    records.append(SitesByOperator(
                        created_at=created_at,
                        operator=operators[op_name],
                        technology=technologies[tech_name],
                        site_count=site_count,
                    ))

    SitesByOperator.objects.bulk_create(records)


def migrate_by_vendors():
    for name in VENDORS.values():
        Vendor.objects.get_or_create(name=name)

    vendors = {v.name: v for v in Vendor.objects.all()}
    technologies = {tech.name: tech for tech in Technology.objects.all()}

    with open('sites_by_vendors.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = []

        for row in reader:
            created_at = datetime.strptime(row['CREATED_AT'], '%Y-%m-%d %H:%M:%S.%f').date()
            for v_key, v_name in VENDORS.items():
                for tech_key, tech_name in TECHNOLOGIES.items():
                    column_name = f'{v_key}_{tech_key}'.upper()
                    try:
                        site_count = int(row[column_name]) if row[column_name] else 0
                    except KeyError:
                        site_count = 0

                    records.append(SitesByVendor(
                        created_at=created_at,
                        vendor=vendors[v_name],
                        technology=technologies[tech_name],
                        site_count=site_count,
                    ))

    SitesByVendor.objects.bulk_create(records)


def migrate_by_regions():
    for name in REGIONS.values():
        Region.objects.get_or_create(name=name)

    regions = {reg.name: reg for reg in Region.objects.all()}
    technologies = {tech.name: tech for tech in Technology.objects.all()}

    with open('sites_by_regions.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = []

        for row in reader:
            created_at = datetime.strptime(row['CREATED_AT'], '%Y-%m-%d %H:%M:%S.%f').date()
            for reg_key, reg_name in REGIONS.items():
                for tech_key, tech_name in TECHNOLOGIES.items():
                    column_name = f'{reg_key}_{tech_key}'.upper()
                    try:
                        site_count = int(row[column_name]) if row[column_name] else 0
                    except KeyError:
                        site_count = 0

                    records.append(SitesByRegion(
                        created_at=created_at,
                        region=regions[reg_name],
                        technology=technologies[tech_name],
                        site_count=site_count,
                    ))

    SitesByRegion.objects.bulk_create(records)
