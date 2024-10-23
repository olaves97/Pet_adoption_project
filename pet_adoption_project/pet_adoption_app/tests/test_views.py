from unittest.mock import patch

from django.contrib.auth.models import User, Group
from django.http import Http404
from django.test import TestCase, Client
from django.urls import reverse

from pet_adoption_app.models import Pet


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.pet1 = Pet.objects.create(id=1, name='Buddy', species='dog', breed='', age=1, sex='M', size='Medium',
                                      temperament='Calm', personality='Distant', kid_friendly='Y', dog_friendly='Y',
                                      cat_friendly='Y', neutered='N', submitter='Grace Hall',
                                      submission_date='2022-04-18 07:00')

        self.pet2 = Pet.objects.create(id=2, name='Fox', species='dog', breed='', age=2, sex='M', size='Medium',
                                      temperament='Calm', personality='Distant', kid_friendly='Y', dog_friendly='Y',
                                      cat_friendly='Y', neutered='N', submitter='Grace Hall',
                                      submission_date='2022-04-18 07:00')

        self.pet3 = Pet.objects.create(id=3, name='Buddy', species='dog', breed='', age=3, sex='M', size='Medium',
                                      temperament='Calm', personality='Distant', kid_friendly='Y', dog_friendly='Y',
                                      cat_friendly='Y', neutered='N', submitter='Grace Hall',
                                      submission_date='2022-04-18 07:00')

        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator_user = User.objects.create_user(username='moderator', password='password')
        self.moderator_user.groups.add(self.moderator_group)

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_pets_GET(self):
        response = self.client.get(reverse('pets'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets.html')

    def test_quiz_GET(self):
        response = self.client.get(reverse('quiz_main_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_main_page.html')

    @patch('pet_adoption_app.views.QuizManager.prepare_a_list_of_responses')
    @patch('pet_adoption_app.views.QuizManager.search_database')
    @patch('pet_adoption_app.views.QuizManager.find_three_best_dogs_ids')
    def test_submit_form_success(self, mock_find_three_best_dogs_ids, mock_search_database,
                                 mock_prepare_a_list_of_responses):

        mock_prepare_a_list_of_responses.return_value = ['Small', 'Young', 'Male', 'Purebred', 'Calm', 'Cuddly', 'Yes', 'Yes', 'Yes', 'Yes']
        mock_search_database.return_value = ['dog1', 'dog2', 'dog3']

        mock_find_three_best_dogs_ids.return_value = [self.pet1, self.pet2, self.pet3]

        response = self.client.get(reverse('quiz_results'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_results.html')
        self.assertEqual(response.context['matched_pets'], [self.pet1, self.pet2, self.pet3])


    @patch('pet_adoption_app.views.QuizManager.prepare_a_list_of_responses')
    def test_submit_form_too_few_answers(self, mock_prepare_a_list_of_responses):
        mock_prepare_a_list_of_responses.return_value = ['Small']

        response = self.client.post(reverse('quiz_results'), {
            'quiz_answer_1': mock_prepare_a_list_of_responses.return_value,
        })

        self.assertEqual(response.status_code, 404)


    def test_pet_detail_when_pet_exists(self):
        response = self.client.get(reverse('pet_detail', args = [self.pet1.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pet_detail.html')


    def test_pet_detail_when_pet_does_not_exist(self):
        response = self.client.get(reverse('pet_detail', args=[9999]))
        self.assertEquals(response.status_code, 404)

    def test_signup_view_get(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign_up.html/')
        self.assertIn('form', response.context)

    def test_signup_view_post_valid_data(self):

        form = {
            'username': 'newuser',
            'password1': 'Pass123@',
            'password2': 'Pass123@',
            'email': 'newuser@example.com',
        }
        response = self.client.post(reverse('sign_up'), data=form)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')

        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)

    def test_signup_view_post_missing_fields(self):

        form = {
            'username': '',
            'password1': 'Pass123@',
            'password2': 'Pass123@',
            'email': 'newuser@example.com',
        }
        response = self.client.post(reverse('sign_up'), data=form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign_up.html/')

        user_exists = User.objects.filter(username='').exists()
        self.assertFalse(user_exists)

    def test_signup_view_post_invalid_fields(self):

        form = {
            'username': 'newuser',
            'password1': 'Pass123@',
            'password2': 'Pass456@',
            'email': 'invalid_email',
        }
        response = self.client.post(reverse('sign_up'), data=form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign_up.html/')

        self.assertIn('form', response.context)
        errors = response.context['form'].errors

        self.assertIn('email', errors)
        self.assertIn('Enter a valid email address.', errors['email'])

        self.assertIn('password2', errors)
        self.assertIn("The two password fields didn’t match.", errors['password2'])

        user_exists = User.objects.filter(username='newuser').exists()
        self.assertFalse(user_exists)

    def test_moderator_dashboard_access_for_moderator(self):

        self.client.login(username='moderator', password='password')
        response = self.client.get(reverse('moderator_dashboard'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'moderator_dashboard.html')

        database_table = response.context['database_table']
        self.assertEqual(database_table.count(), 3)
        self.assertEqual(database_table[0].name, self.pet1.name)
        self.assertEqual(database_table[1].name, self.pet2.name)
        self.assertEqual(database_table[2].name, self.pet3.name)

    def test_moderator_dashboard_access_for_non_moderator(self):

        regular_user = User.objects.create_user(username='regular_user', password='password')
        self.client.login(username='regular_user', password='password')
        response = self.client.get(reverse('moderator_dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/moderator/')

    def test_moderator_dashboard_access_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('moderator_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/moderator/')

    def test_edit_a_pet_record_by_moderator(self):

        self.client.login(username='moderator', password='password')
        response = self.client.get(reverse('edit', args=[self.pet1.id]))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'database_actions/edit.html')

        # database_table = response.context['database_table']
        # self.assertEqual(database_table.count(), 3)
        # self.assertEqual(database_table[0].name, self.pet1.name)
        # self.assertEqual(database_table[1].name, self.pet2.name)
        # self.assertEqual(database_table[2].name, self.pet3.name)