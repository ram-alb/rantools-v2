from datetime import date
from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from sites_count import views


def fake_get_site_data(table_type, requested_date=None):
    """Fake get_site_data function for tests."""
    site_data = {
        'operator': [['Kcell', 100, 200, 400, 50, 500]],
        'vendor': [['Ericsson', 10, 20, 30, 5, 50]],
    }
    return site_data[table_type]


class SitesCountViewTestCase(TestCase):
    """Tests for SitesCountView view."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.url = reverse('sites_count')
        self.past_year = 2022
        self.future_year = 2100
        self.month = 5
        self.day = 17
        views.get_site_data = fake_get_site_data

    def test_get(self):
        """Test get request."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'sites_count/sites_count.html')
        self.assertContains(response, '<td>Kcell</td>')
        self.assertContains(response, '<td>100</td>')

    def test_post_valid_form(self):
        """Test post request with valid form."""
        response = self.client.post(
            self.url,
            data={'date': date.today(), 'table_type': 'vendor'},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Kcell sites devided by Vendor')
        self.assertContains(response, '<td>Ericsson</td>')
        self.assertContains(response, '<td>50</td>')

    def test_post_invalid_form_past_date(self):
        """Test post request with wrong date in the past."""
        response = self.client.post(
            self.url,
            data={
                'date': date(self.past_year, self.month, self.day),
                'table_type': 'vendor',
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "No data before 15 May 2023",
        )

    def test_post_invalid_form_future_date(self):
        """Test post request with wrong date in the future."""
        response = self.client.post(
            self.url,
            data={
                'date': date(self.future_year, self.month, self.day),
                'table_type': 'vendor',
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "No data from the future :)",
        )
