from django.db import models

# Create your models here.
class Dict_Words(models.Model):

    word = models.CharField(max_length=100, default="")
    class Meta:
        verbose_name_plural = "Dict_Words"
        app_label = "randLang"

    def __str__(self):

        return self.word
class User_Created(models.Model):

    user_word = models.CharField(max_length=100, default="")
    definition = models.CharField(max_length=100, default="")
    language = models.CharField(db_index=True, max_length=100, default="")
    class Meta:
        verbose_name_plural = "User_Created"
    def __str__(self):

        return self.user_word
