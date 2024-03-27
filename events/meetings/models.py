from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Tags(models.Model):
    tag_name = models.CharField(max_length=25,
                                help_text="Введите название тега",
                                verbose_name="Имя тега")

    def __str__(self):
        return self.tag_name


class Place(models.Model):
    office = models.CharField(max_length=50,
                              help_text="Введите место проведения мероприятия",
                              verbose_name="Место проведения мероприятия")
    max_participant = models.IntegerField(null=True, blank=True,
                                          help_text="Введите колличество мест",
                                          verbose_name="Колличество мест")

    def __str__(self):
        return self.office


class Timetable(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              help_text="Выберите место проведения мероприятия",
                              verbose_name="Место проведения мероприятия")
    event_date = models.DateField(help_text="Введите дату проведения мероприятия",
                                  verbose_name="Дата проведения мероприятия")
    start_time = models.TimeField(help_text="Введите время начала мероприятия",
                                  verbose_name="Время начала мероприятия")
    end_time = models.TimeField(help_text="Введите время окончания мероприятия",
                                verbose_name="Время окончания мероприятия")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                               help_text="Выберите автора записи на мероприятие",
                               verbose_name="Автор записи мероприятия")

    def __str__(self):
        return f'{self.event_date} {self.start_time} - {self.end_time}'


class Chat(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True,
                            help_text="Введите название чата",
                            verbose_name="Название чата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='author_chat')
    created_at = models.DateTimeField(auto_now_add=True, null=True,
                                      verbose_name="Дата создания мероприятия")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='users_now_in_chat')

    def __str__(self):
        return self.name

    def connect_user(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        else:
            is_user_added = True
        return is_user_added

    def disconnect_user(self,user):
        is_user_removed = False
        if not user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        else:
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f"PublicChatRoom-{self.id}"


class Meeting(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,
                             help_text="Введите название мероприятия",
                             verbose_name="Название мероприятия")
    body = models.TextField(max_length=1000, null=True, blank=True,
                            help_text="Введите информацию о мероприятит",
                            verbose_name="Информация о мероприятии")
    tags = models.ManyToManyField(Tags, related_name='meetings_list', blank=True,
                                  help_text="Выберите теги для мероприятия",
                                  verbose_name="Теги мероприятия")
    seats = models.IntegerField(default=1, null=True,
                                verbose_name="Колличество свободных мест на мероприятии")
    seats_bool = models.BooleanField(default=True, null=True,  verbose_name="Наличие свободных мест на мероприятии")
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, null=True, blank=True,
                                help_text="Выберите чат для мероприятия",
                                verbose_name="Чат мероприятия")
    timetable = models.OneToOneField(Timetable, null=True, on_delete=models.CASCADE, verbose_name="Запись мероприятия")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания мероприятия")
    update_at = models.DateTimeField(auto_now=True,
                                     verbose_name="Дата последнего изменения мероприятия")

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, help_text="Укажите вашу дату рождения",
                                verbose_name="Дата рождения")
    info = models.TextField(max_length=500, null=True, blank=True,
                            help_text="Введите информацию о вас",
                            verbose_name="Информация о вас")
    # profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    telegram = models.CharField(max_length=50, null=True, blank=True,
                                help_text="Напишите свой Telegtam",
                                verbose_name="Telegtam")
    meetings = models.ManyToManyField(Meeting, related_name='meetings', blank=True,
                                      help_text="Выберете мероприятия, которые хотите поситить",
                                      verbose_name="Мероприятия")
    tags = models.ManyToManyField(Tags, blank=True,
                                  help_text="Выберите интересующие теги",
                                  verbose_name="Ваши теги")
    chats = models.ManyToManyField(Chat, related_name='profile', blank=True,
                                   help_text="Выберете чаты",
                                   verbose_name="Ваши чаты")

    def get_tags_list(self):
        return self.tags.all()

    def __str__(self):
        return str(self.user)


class ChatMessageManager(models.Manager):
    def by_room(self, chat):
        qs = Message.objects.filter(chat=chat).order_by("-timestamp")
        return qs


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200,
                               help_text="Введите сообщение",
                               verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания сообщения")

    def __str__(self):
        return f'{self.message} {self.created_at}'


class Voting(models.Model):
    name = models.CharField(max_length=50, null=True,
                            help_text="Введите название голосования",
                            verbose_name="Название голосования")
    meeting = models.ForeignKey(Meeting, null=True, blank=True, related_name='voting', on_delete=models.CASCADE,
                                help_text="Выберите мероприятие",
                                verbose_name="Мероприятие")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=50,
                            help_text="Введите название поля",
                            verbose_name="Название поля")
    users = models.ManyToManyField(User, related_name='fields', blank=True,
                                   verbose_name="Список выбравших это поле")
    vote = models.ForeignKey(Voting, null=True, blank=True, related_name='fields', on_delete=models.CASCADE,
                             help_text="Выберите голосование",
                             verbose_name="Голосование")
    count_votes = models.IntegerField(default=0, help_text="Введите количество голосов",
                                      verbose_name="Количество голосов")

    def __str__(self):
        return self.name
