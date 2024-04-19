from pet_adoption_app.models import Pet

PARAMETERS = ['size', 'age', 'sex', 'breed', 'temperament', 'personality', 'kid_friendly', 'dog_friendly',
              'cat_friendly', 'neutered']


def search_database(responses):
    iterator = 0
    matching_dogs = []

    for parameter in PARAMETERS:
        if responses[iterator][1] != "Doesn't matter":
            for value_from_db in Pet.objects.values_list('id', parameter):
                value_from_db = list(value_from_db)
                # print(value_from_db)
                if parameter == 'age':
                    check_the_age(value_from_db)
                if parameter == 'breed':
                    check_the_breed(value_from_db)
                if value_from_db[1] == responses[iterator][1]:
                    matching_dogs.append(value_from_db[0])
        else:
            for i in list(Pet.objects.values_list('id', flat=True)):
                matching_dogs.append(i)

        iterator = iterator + 1

    return try_to_find_three_best_dogs(matching_dogs)


def check_the_age(value_from_db):
    if value_from_db[1] > 5:
        value_from_db[1] = 'Old'
    else:
        value_from_db[1] = 'Young'
    return value_from_db


def check_the_breed(value_from_db):
    if value_from_db[1] is not '':
        value_from_db[1] = 'Purebred'
    else:
        value_from_db[1] = 'Non-purebred'
    return value_from_db


class EmptyListError(Exception):
    pass


def check_the_most_matching_dog(matching_dogs):
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


def try_to_find_three_best_dogs(matching_dogs):
    top_three_dogs = []
    for i in range(0, 3):
        dog_id_and_number_of_matched_parameters = check_the_most_matching_dog(matching_dogs)
        top_three_dogs.append(dog_id_and_number_of_matched_parameters)
    return top_three_dogs
