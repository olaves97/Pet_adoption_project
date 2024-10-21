from unittest.mock import patch

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
