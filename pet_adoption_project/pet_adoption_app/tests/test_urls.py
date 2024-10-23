from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse, resolve

from pet_adoption_app.models import Pet
from pet_adoption_app.views import home, pets, quiz, pet_detail, submit_form, sign_up, moderator_dashboard, \
    create_a_record, edit, PetDeleteView


class TestUrls(TestCase):

    def setUp(self):
        self.pet = Pet.objects.create(id=1, name='Buddy', species='dog', breed='', age=1, sex='M', size='Medium',
                                 temperament='Calm', personality='Distant', kid_friendly='Y', dog_friendly='Y',
                                 cat_friendly='Y', neutered='N', submitter='Grace Hall',
                                 submission_date='2022-04-18 07:00')

        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator = User.objects.create_user(username='moderator', password='password')
        self.moderator.groups.add(self.moderator_group)
        self.client.login(username='moderator', password='password')

    def test_blank_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_pets_url_is_resolved(self):
        url = reverse('pets')
        self.assertEquals(resolve(url).func, pets)

    def test_quiz_url_is_resolved(self):
        url = reverse('quiz_main_page')
        self.assertEquals(resolve(url).func, quiz)

    def test_pet_detail_url_is_resolved(self):
        url = reverse('pet_detail', args = [self.pet.id])
        self.assertEquals(resolve(url).func, pet_detail)

    def test_invalid_pet_detail_url_is_resolved(self):
        pet_id = 9999
        url = reverse('pet_detail', args=[pet_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_quiz_results_url_is_resolved(self):
        url = reverse('quiz_results')
        self.assertEquals(resolve(url).func, submit_form)

    def test_sign_up_url_is_resolved(self):
        url = reverse('sign_up')
        self.assertEquals(resolve(url).func, sign_up)

    def test_moderator_dashboard_url_is_resolved(self):
        url = reverse('moderator_dashboard')
        self.assertEquals(resolve(url).func, moderator_dashboard)

    def test_create_a_record_url_is_resolved(self):
        url = reverse('create')
        self.assertEquals(resolve(url).func, create_a_record)

    def test_edit_url_is_resolved(self):
        url = reverse('edit', args = [self.pet.id])
        self.assertEquals(resolve(url).func, edit)

    def test_invalid_edit_url_is_resolved(self):
        self.client.login(username='moderator', password='password')
        pet_id = 9999
        url = reverse('edit', args=[pet_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_pet_url_is_resolved(self):
        url = reverse('pet_delete', args = [self.pet.id])
        self.assertEquals(resolve(url).func.view_class, PetDeleteView)

    def test_invalid_delete_url_is_resolved(self):
        pet_id = 9999
        url = reverse('pet_delete', args=[pet_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
