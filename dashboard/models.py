from django.db import models

from twilio.rest import Client
# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.score >= 70:
            account_sid = ''
            auth_token = ''
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"Congratulations {self.name}, your score is {self.score}",
                from_='',
                to=''
            )
        else:
            account_sid = ''
            auth_token = ''
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"Sorry {self.name}, your score is {self.score}. Try again",
                from_='',
                to=''
            )

        print(message.sid)
        return super().save(*args, **kwargs)