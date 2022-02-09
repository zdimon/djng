import json

from django.test import LiveServerTestCase
from django.urls import reverse
from account.models import UserProfile
from moderation.models import Moderation
from settings.models import MailTemplates


class WomanTest(LiveServerTestCase):
    def test_registration(self):
        data = {
            'name': 'test name',
            'photo': 'test photo',
        }

        response = self.client.post(reverse('account-register-woman'), data=data)

        woman = Moderation.objects.first()
        self.assertEqual(woman.name, 'Woman registration')
        self.assertEqual(json.loads(woman.data), data)

        self.assertEqual(json.loads(response.content.decode()), {'status': 0, 'message': 'Ok', 'id': woman.id})


class ManTest(LiveServerTestCase):
    def test_registration(self):
        MailTemplates.objects.create(alias='man-registration')

        data = {
            'email': 'test@mail.ru',
        }

        response = self.client.post(reverse('account-register-man'), data=data)

        man = UserProfile.objects.first()
        self.assertEqual(man.username, data['email'])
        self.assertEqual(man.email, data['email'])
        self.assertTrue(man.is_active)

        self.assertEqual(json.loads(response.content.decode()), {'status': 0, 'message': 'Ok'})


class AgencyTest(LiveServerTestCase):
    def test_registration(self):
        data = {
            'test': 'test data',
        }

        response = self.client.post(reverse('account-register-agency'), data)

        agency = Moderation.objects.first()
        self.assertEqual(agency.name, 'Agency registration')
        self.assertEqual(agency.type_obj, 'agency')
        self.assertEqual(json.loads(agency.data), data)

        self.assertEqual(json.loads(response.content.decode()), {'status': 0, 'message': 'Ok', 'id': agency.id})
