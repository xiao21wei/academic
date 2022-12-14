from django.db import models
from django import forms

# Create your models here.


class User(models.Model):  # User is a class that inherits from models.Model
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256, unique=False)
    password = models.CharField(max_length=256, unique=False)
    email = models.CharField(max_length=256, unique=True)
    address = models.CharField(max_length=256, unique=False, default='未填写')
    identity = models.IntegerField(unique=False, default=0)
    intro = models.CharField(max_length=256, unique=False, default='未填写')
    penalty = models.BooleanField(default=False)
    birthday = models.DateField(null=True)
    team_id = models.IntegerField(unique=False, null=True)
    real_name = models.CharField(max_length=256, unique=False, default='未填写')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'  # 指明数据库表名
        ordering = ['user_id']  # 按照id排序
        verbose_name = 'user'  # 单数形式
        verbose_name_plural = 'users'  # 复数形式

    def to_json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'address': self.address,
            'identity': self.identity,
            'intro': self.intro,
            'penalty': self.penalty,
            'birthday': self.birthday,
            'team_id': self.team_id,
            'real_name': self.real_name,
        }


class Admin(models.Model):  # Admin is a class that inherits from models.Model
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=False)
    password = models.CharField(max_length=256, unique=False)
    email = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'admin'  # 指明数据库表名
        ordering = ['admin_id']  # 按照id排序
        verbose_name = 'admin'  # 单数形式
        verbose_name_plural = 'admins'  # 复数形式


class Achievement(models.Model):  # Achievement is a class that inherits from models.Model
    achievement_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    author = models.CharField(max_length=256, unique=False)
    intro = models.CharField(max_length=256, unique=False, default='未填写')
    url = models.CharField(max_length=256, unique=False, default='未填写')
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(unique=False, default=0)
    area = models.CharField(max_length=256, unique=False, default='未填写')
    hot = models.IntegerField(unique=False, default=0)
    recommend = models.IntegerField(unique=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'achievement'  # 指明数据库表名
        ordering = ['achievement_id']  # 按照id排序
        verbose_name = 'achievement'  # 单数形式
        verbose_name_plural = 'achievements'  # 复数形式


class Team(models.Model):  # Team is a class that inherits from models.Model
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    intro = models.CharField(max_length=256, unique=False, default='未填写')
    create_time = models.DateTimeField(auto_now_add=True)
    user_list = models.CharField(max_length=256, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'team'  # 指明数据库表名
        ordering = ['team_id']  # 按照id排序
        verbose_name = 'team'  # 单数形式
        verbose_name_plural = 'teams'  # 复数形式


class Like(models.Model):  # Like is a class that inherits from models.Model
    like_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=False)
    achievement_id = models.IntegerField(unique=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'like'  # 指明数据库表名
        ordering = ['like_id']  # 按照id排序
        verbose_name = 'like'  # 单数形式
        verbose_name_plural = 'likes'  # 复数形式


class Follow(models.Model):  # Follow is a class that inherits from models.Model
    follow_id = models.AutoField(primary_key=True)
    user1_id = models.IntegerField(unique=False)
    user2_id = models.IntegerField(unique=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'follow'  # 指明数据库表名
        ordering = ['follow_id']  # 按照id排序
        verbose_name = 'follow'  # 单数形式
        verbose_name_plural = 'follows'  # 复数形式


class Collection(models.Model):  # Collection is a class that inherits from models.Model
    collection_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=False)
    achievement_id = models.IntegerField(unique=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'collection'  # 指明数据库表名
        ordering = ['collection_id']  # 按照id排序
        verbose_name = 'collection'  # 单数形式
        verbose_name_plural = 'collections'  # 复数形式


class Chat(models.Model):  # Chat is a class that inherits from models.Model
    chat_id = models.AutoField(primary_key=True)
    send = models.IntegerField(unique=False)
    receive = models.IntegerField(unique=False)
    content = models.CharField(max_length=256, unique=False)
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat'  # 指明数据库表名
        ordering = ['chat_id']  # 按照id排序
        verbose_name = 'chat'  # 单数形式
        verbose_name_plural = 'chats'  # 复数形式


class Report(models.Model):  # Report is a class that inherits from models.Model
    report_id = models.AutoField(primary_key=True)
    send = models.IntegerField(unique=False)
    achievement_id = models.IntegerField(unique=False)
    content = models.CharField(max_length=256, unique=False)
    admin = models.IntegerField(unique=False)
    time = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(unique=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'report'  # 指明数据库表名
        ordering = ['report_id']  # 按照id排序
        verbose_name = 'report'  # 单数形式
        verbose_name_plural = 'reports'  # 复数形式


class Comment(models.Model):  # Comment is a class that inherits from models.Model
    comment_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=False)
    achievement_id = models.IntegerField(unique=False)
    content = models.CharField(max_length=256, unique=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'comment'  # 指明数据库表名
        ordering = ['comment_id']  # 按照id排序
        verbose_name = 'comment'  # 单数形式
        verbose_name_plural = 'comments'  # 复数形式


class VerificationCode(models.Model):  # VerificationCode is a class that inherits from models.Model
    code_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=256, unique=False)
    code = models.CharField(max_length=256, unique=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'verification_code'  # 指明数据库表名
        ordering = ['code_id']  # 按照id排序
        verbose_name = 'verification_code'  # 单数形式
        verbose_name_plural = 'verification_codes'  # 复数形式
