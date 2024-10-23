from django.test import TestCase


from pet_adoption_app.forms import RegisterForm, PetInDatabase


class TestForms(TestCase):

    def test_register_form_valid_data(self):

        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Pass123@',
            'password2': 'Pass123@',
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_missing_fields(self):

        form = RegisterForm(data={
            'username': '',
            'email': '',
            'password1': 'Pass123@',
            'password2': 'Pass123@',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_register_form_invalid_email(self):

        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'notanemail',
            'password1': 'Pass123@',
            'password2': 'Pass123@',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_register_form_passwords_mismatch(self):

        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Pass123@',
            'password2': 'differentpassword',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


    def test_pet_in_database_valid_data(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Big',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })
        self.assertTrue(pet.is_valid())

    def test_pet_in_database_invalid_missing_fields(self):
        pet = PetInDatabase(data={
            'name': '',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Big',
            'temperament': '',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('name', pet.errors)
        self.assertIn('temperament', pet.errors)

    def test_pet_in_database_invalid_age(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': 'wrong_data',
            'sex': 'Male',
            'size': 'Big',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('age', pet.errors)

    def test_pet_in_database_invalid_sex(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'wrong_data',
            'size': 'Big',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('sex', pet.errors)

    def test_pet_in_database_invalid_size(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'wrong_data',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('size', pet.errors)

    def test_pet_in_database_invalid_temperament(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'wrong_data',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('temperament', pet.errors)

    def test_pet_in_database_invalid_personality(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'Calm',
            'personality': 'wrong_data',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('personality', pet.errors)

    def test_pet_in_database_invalid_answer_to_kid_friendly(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'wrong_answer',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('kid_friendly', pet.errors)

    def test_pet_in_database_invalid_answer_to_dog_friendly(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'wrong_data',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('dog_friendly', pet.errors)

    def test_pet_in_database_invalid_answer_to_cat_friendly(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'wrong_data',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('cat_friendly', pet.errors)

    def test_pet_in_database_invalid_answer_to_neutered(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'wrong_data',
            'submitter': 'Someone',
            'submission_date':'2022-04-18 07:00',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('neutered', pet.errors)

    def test_pet_in_database_invalid_submission_date(self):
        pet = PetInDatabase(data={
            'name': 'Name',
            'species': 'dog',
            'breed': 'somebreed',
            'age': '10',
            'sex': 'Male',
            'size': 'Small',
            'temperament': 'Calm',
            'personality': 'Cuddly',
            'kid_friendly': 'Yes',
            'dog_friendly': 'Yes',
            'cat_friendly': 'Yes',
            'neutered': 'Yes',
            'submitter': 'Someone',
            'submission_date':'18-04-2022',
        })

        self.assertFalse(pet.is_valid())
        self.assertIn('submission_date', pet.errors)