from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, valid_email2, valid_password2
import os

pf = PetFriends()

def test_successful1_add_new_pet_simple(name='Нефотканный', animal_type='фантомас',
                                     age="4"):
    """Проверяем метод на добавление питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful2_add_new_pet_simple(name='Боря', animal_type1='кот',
                                     age1="4",animal_type2='пес', age2="2"):
    """Проверяем метод на добавление 2х питомцев с одинаковыми именами"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    pf.add_new_pet_simple(auth_key, name, animal_type1, age1)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type2, age2)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_fail1_add_new_pet_simple(name='Нефотканный', animal_type='фантомас',
                                     age='пять'):
    """Проверяем метод на добавление питомца без фото с неправильным вводом - возраст в нечисловом формате
    Тест проходит неуспешно. Возможно добавить питомца с таким возрастом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name


def test_successful_add_photo(pet_photo='images\cat1.jpg'):
    """Проверяем возможность добавления фотографии питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить ему фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There are no my pets")

def test_fail1_add_photo(pet_photo='images\cat1.jpg'):
    """Проверяем возможность добавления фотографии неправильным data-type в методе"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить ему фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo_incorrect(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 400
        assert status == 400
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There are no my pets")

def test_fail2_add_photo(pet_photo='images\panda.bmp'):
    """Проверяем возможность добавления фотографии питомца в неверном формате
    Тест проходит неуспешно. Получаем 500 ошибку вместо 403"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить ему фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 403
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There are no my pets")



def test_success_delete_not_my_pet(name="Чужой", animal_type="Пришелец", age="666", pet_photo='images\Alien.jpg'):
    """Проверяем возможность удаления чужого питомца
    С моей точки зрения баг - нельзя давать удалить чужого питомца. Но в документации нигде не сказано о данном ограничении.
    Поэтому проверка на код 200"""

    """Cначала добавим питомца через акк2"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email2, valid_password2)
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Добавляем питомца и получаем его id
    pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    """Потом попытаемся удалить через акк1"""
    # Запрашиваем ключ api и список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_fail1_get_key():
    """Проверяем метод на получение ключа для несуществующего логина"""
    status, result = pf.get_api_key(invalid_email, valid_password)
    # Проверяем что статус ответа = 403
    assert status == 403

def test_fail2_get_key():
    """Проверяем метод на получение ключа для существующего логина но с неверным паролем"""
    status, result = pf.get_api_key(valid_email, invalid_password)
    # Проверяем что статус ответа = 403
    assert status == 403

def test_add_new_pet_with_very_long_name(name='яхрthпSи@heMщиDm@$@а%4gXщ9C7mщнn!ыbгEVpsщU@)S*J^lHхKс!fISфшkh5*xjвUKиV6Mе5юyфpплгоuфl1ьбзFV5NжsJбbзAv6сл!4о2f@IмJnп3bх2JqкtVfзLXfU)ш5frP!g9Qv$fVcRIkнQ1Yц3йr0*O&PkоDD)PdJdyrOxчgiьADsWUсмяlBрhвQN(8KvDpq8B!тuг$0FLZKRхят3цAh9@лAi(е7aIISGhp6N*pеъоZMзй((лflyуOу!C',
                                         animal_type='NQaN!ч72NъpGjWп2Aын%аqFxxсоhдAlаtxхD1MAxfррoaсаn^тяз9e7Kн1wQF*ugMqцgкLpvтщщjkй@яda(Gi6YjRх1n%WDтj#еTKVw26уkюIэ)ч7ji5xщxh9GмсeGR2эвийuNеAMsгбsмl5RsYоhъjdцаw#3е%MыauTdubj#1южi5ctafyqъL)еm%в*plRQT8NдWez9зzыXIuL5iKiNMъпH#wчвмjXfJXPцXh#kk7xь1(щшэzхiюIк%rgр6fhrе*',
                                     age='4', pet_photo='images\P1040103.jpg'):
    """Проверяем что можно добавить питомца с очень длинным именем и знаками в нем (257 знаков)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
