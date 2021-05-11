from django.db import models
from django.conf import settings  
from PIL import Image  


        
SEX = [ ('', 'Choose....'),
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

MARITAL_STATUS = [  ('', 'Choose....'),
                    ('Married', 'Married'),
                    ('Single', 'Single')
            ]

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpeg', upload_to='users/%Y/%m/%d', blank=True, null=True)
    sex = models.CharField(max_length=50, choices=SEX, null=True, blank=True)
    educational_background = models.CharField(max_length=200, blank=True, null=True)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS, blank=True, null=True)
    home_address = models.CharField(max_length=200, null=True, blank=True, default='e.g No 2 Aba Rd, Uyo, Akwa Ibom State')
    phone_no = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f' profile for {self.user.username}'.title()
    
    # I am using this to overide the save method of this model and to resize my image once it is uploaded.

    # def save(self):
    #     super().save()

    #     img = Image.open(self.profile_pic.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)



