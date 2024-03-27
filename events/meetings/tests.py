from django.test import TestCase
from django.contrib.auth.models import User
from .models import Meeting, Place
import json

class MeetingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('==Тест создания мероприятия==')
    #Create a user
        testuser_1 = User.objects.create_user(
            username='testuser_1',
            password='abc123',)
        testuser_1.save()
        print('- Пользователь создан')
        test_place = Place.objects.create(
            office='test_office'
        )
        print('- Место проведения создано')
    #Create a meeting
        test_meeting = Meeting.objects.create(
            author=testuser_1,
            title='Meeting title',
            body='Body content...',
            place=test_place,)
        test_meeting.save()
        print('- Мероприятие создано')

    def responce_pattern_content(self, token: str, parameters: dict):
        response = self.client.post("/meeting-api/v1/meeting/", parameters,
                                    HTTP_AUTHORIZATION='Token {0}'.format(token))
        #print('- Аунтефикация по токену успешна')
        response_content = json.loads(response.content.decode('utf-8'))
        #print('- Декодирование JSON успешно')
        return response_content

    def test_meeting_content(self):
        meeting = Meeting.objects.get(id=1)
        author = f'{meeting.author}'
        title = f'{meeting.title}'
        body = f'{meeting.body}'
        place = f'{meeting.place}'
        self.assertEqual(author, 'testuser_1')
        self.assertEqual(title, 'Meeting title')
        self.assertEqual(body, 'Body content...')
        self.assertEqual(place, 'test_office')

        response = self.client.post("/auth/token/login/", {"username": "testuser_1", "password": "abc123"})
        self.assertEqual(response.status_code, 200, "Токен должен быть успешно возвращен.")
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content["auth_token"]
        print('- Токен получен')

        print("Запрос на создание мероприятия без параметров")
        content = self.responce_pattern_content(token, {})
        self.assertEqual(content['author'][0], "Обязательное поле.",
                         "Обязательное поле, которое надо заполнить")
        self.assertEqual(content['title'][0], "Обязательное поле.",
                         "Обязательное поле, которое надо заполнить")
        self.assertEqual(content['place'][0], "Обязательное поле.",
                         "Обязательное поле, которое надо заполнить")
        print('= Успешно')

        print("Запрос на создание мероприятия без обязательного параметра\n- author")
        content = self.responce_pattern_content(token, {"title": ["Body content..."],
                                                        "place": [1]})
        self.assertEqual(content['author'][0], "Обязательное поле.",
                         "Обязательное поле, которое надо заполнить")

        print("- title")
        content = self.responce_pattern_content(token, {"author": [1],
                                                        "place": [1]})
        self.assertEqual(content['title'][0], "Обязательное поле.",
                         "Обязательное поле, которое надо заполнить")

        print("- place")
        content = self.responce_pattern_content(token, {"author": [1],
                                                        "title": ["Body content..."]})
        self.assertEqual(content['place'][0], "Обязательное поле.",
                         "Обязательное поле, которое надо заполнить")
        print('= Успешно')

        print("Запрос на создание мероприятия c неверным параметраметром\n- author")
        content = self.responce_pattern_content(token, {"author": ["dadasdasdas"],
                                                        "title": ["Body content..."],
                                                        "place": ["test_office"]})
        self.assertEqual(content['author'][0],
                         "Некорректный тип. Ожидалось значение первичного ключа, получен str.",
                         "Обязательное поле, которое надо заполнить")

        print("- title")
        content = self.responce_pattern_content(token, {"author": [1],
                                                        "title": "",
                                                        "place": [1]})
        self.assertEqual(content['title'][0], "Это поле не может быть пустым.")

        print("- place")
        content = self.responce_pattern_content(token, {"author": [1],
                                                        "title": ["Body content..."],
                                                        "place": ""})
        self.assertEqual(content['place'][0], "Это поле не может быть пустым.",
                         "Обязательное поле, которое надо заполнить")
        print('= Успешно')


        print('Конец теста')



class TokenTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('\n==Тест токена==')
        testuser_2 = User.objects.create_user(
            username='testuser_2',
            password='abc123',)
        testuser_2.save()
        print('- Пользователь создан')
        test_place = Place.objects.create(
            office='test_office'
        )
        print('- Место проведения создано')
        test_meeting = Meeting.objects.create(
            author= testuser_2,
            title='Meeting title',
            body='Body content...',
            place=test_place,)
        test_meeting.save()
        print('- Мероприятие создано')

    def responce_pattern_content_token(self, token: str):
        response = self.client.get("/meeting-api/v1/meeting/", {},
                                    HTTP_AUTHORIZATION=f'{token}')
        response_content = json.loads(response.content.decode('utf-8'))
        return response_content

    def test_get_token(self):
        response = self.client.post("/auth/token/login/", {"username": "testuser_2", "password": "abc123"})
        self.assertEqual(response.status_code, 200, "Токен должен быть успешно возвращен.")
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content["auth_token"]
        print('- Токен получен')

        print('Аунтефикация правильным токеном')
        content = self.responce_pattern_content_token(f'Token {token}')
        self.assertEqual(content[0]['title'], "Meeting title",
                         "Пользователь должен иметь возможность получить доступ к этой конечной точке.")
        print('= Успешно')

        content = self.responce_pattern_content_token('Token 88f0683404e4e2c77faf9197')
        self.assertEqual(content['detail'], "Недопустимый токен.",
                         "Пользователь должен иметь возможность получить доступ к этой конечной точке.")

        content = self.responce_pattern_content_token('Token')
        self.assertEqual(content['detail'], "Недопустимый заголовок токена. Не предоставлены учетные данные.")

        content = self.responce_pattern_content_token("")
        self.assertEqual(content['detail'], "Учетные данные не были предоставлены.")

