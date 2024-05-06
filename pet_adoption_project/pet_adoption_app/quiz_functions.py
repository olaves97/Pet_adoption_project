from pet_adoption_app.models import Pet


class QuizManager:
    def __init__(self):
        self.responses = []
        self.pets_from_db_matching_the_responses = []
        self.matched_pets = []
        self.top_three_dogs = []

    def prepare_a_list_of_responses(self, request):
        for value in request.POST.items():
            self.responses.append(list(value))
        del self.responses[0]
        return self.responses

    def search_database(self, responses, parameters):
        iterator = 0

        for parameter in parameters:
            if responses[iterator][1] != "Doesn't matter":
                for value_from_db in Pet.objects.values_list('id', parameter):
                    value_from_db = list(value_from_db)
                    if parameter == 'age':
                        self.check_the_age(value_from_db)
                    if parameter == 'breed':
                        self.check_the_breed(value_from_db)
                    if value_from_db[1] == responses[iterator][1]:
                        self.pets_from_db_matching_the_responses.append(value_from_db[0])
            else:
                for i in list(Pet.objects.values_list('id', flat=True)):
                    self.pets_from_db_matching_the_responses.append(i)

            iterator = iterator + 1

        return self.try_to_find_three_best_dogs(self.pets_from_db_matching_the_responses)

    def check_the_age(self, value_from_db):
        if value_from_db[1] > 5:
            value_from_db[1] = 'Old'
        else:
            value_from_db[1] = 'Young'
        return value_from_db

    def check_the_breed(self, value_from_db):
        if value_from_db[1] is not '':
            value_from_db[1] = 'Purebred'
        else:
            value_from_db[1] = 'Non-purebred'
        return value_from_db

    def try_to_find_three_best_dogs(self, matching_dogs):
        for i in range(0, 3):
            dog_id_and_number_of_matched_parameters = self.check_the_most_matching_dog(matching_dogs)
            self.top_three_dogs.append(dog_id_and_number_of_matched_parameters)
        return self.top_three_dogs

    def check_the_most_matching_dog(self, matching_dogs):
        try:
            if len(matching_dogs) != 0:
                perfect_dog = max(set(matching_dogs), key=matching_dogs.count)
                number_of_matched_parameters = matching_dogs.count(perfect_dog)
                matching_dogs[::] = [i for i in matching_dogs if i != perfect_dog]
                return perfect_dog, number_of_matched_parameters
            else:
                raise EmptyListError
        except EmptyListError:
            print('ERROR')
            return None, None

    def find_three_best_dogs_ids(self, top_three_dogs):
        for i in range(0, len(top_three_dogs)):
            self.matched_pets.append(Pet.objects.get(id=top_three_dogs[i][0]))
        return self.matched_pets


class EmptyListError(Exception):
    pass
