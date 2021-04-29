from django.db import models
from django.conf import settings 
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import pre_save
from homapp_project.utils import unique_slug_generator
from PIL import Image
from decimal import Decimal

# class ClotheCategory(models.Model):
#     category_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=250, unique_for_date='activete')
#     date_added = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#     activete = models.DateTimeField(default=timezone.now)


#     class Meta:
#         ordering = ('-activete',)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('homapp:clothes_list_by_category', args=[self.slug]) 

# class Status(models.Model):
#     name = models.CharField(max_length=250)

#     def __str__(self):
#         return self.name

class WearCategory(models.Model):
    category_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    category_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self):
        return self.category_name


class Wear(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='wear/%Y/%m/%d', blank=True, null='')
    description = models.TextField(blank=True, null='')
    category = models.ForeignKey(WearCategory, related_name='wears', on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0, blank=True)
    date_bought = models.DateTimeField(auto_now=True, blank=True, null='')
    bought_from = models.CharField(max_length=250, blank=True, null='')
    activate = models.BooleanField(default=True)
    expenses = models.BooleanField(default=False)
    
    
   

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f'{self.name} for {self.user.username}'.title()
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.photo.path)

    #     if img.height > 100 or img.weight > 100:
    #         output_size = (100,100)
    #         img.thumbnail(output_size)
    #         img.save(self.photo.path)


class FinanceCategory(models.Model):
    category_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    category_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f'{self.category_name}'.title()

class Finance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null='')
    photo = models.ImageField(upload_to='finance/%Y/%m/%d', blank=True, null='')
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True, default=0)
    category = models.ForeignKey(FinanceCategory, related_name='finance', on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)
    expenses = models.BooleanField(default=True)
    

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f'{self.title} for {self.user.username}'.title()

class TaskCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return self.name  

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(default='Add some description', blank=True)
    complete = models.BooleanField(default=False)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, default='No category', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    due = models.DateTimeField(default=timezone.now, blank=False, null=False)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return self.name 

    @property
    def is_overdue(self):
        if self.due and timezone.now() >= self.due:
            return True
        return False
    
  



# class Clothe(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=250, unique_for_date='activate', blank=True, null=True)
#     activate = models.DateTimeField(default=timezone.now)
#     photo = models.ImageField(upload_to='clothes/%Y/%m/%d', blank=True, null='')
#     description = models.TextField(blank=True, null='')
#     category = models.ForeignKey(ClotheCategory, related_name='clothes', on_delete=models.CASCADE)
#     date_registered = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#     clothe_amount = models.DecimalField(max_digits=19, decimal_places=2, default=0, blank=True, null='')
#     date_bought = models.DateTimeField(auto_now=True, blank=True, null='')
#     bought_from = models.CharField(max_length=250, blank=True, null='')
#     status = models.ForeignKey(Status, on_delete=models.CASCADE)

#     class Meta:
#         ordering = ('-activate',)
#         index_together = (('id', 'slug'),)
    

#     def __str__(self):
#         return f'{self.name} for {self.user.username}'.title()
    
#     def get_absolute_url(self):
#         return reverse('homapp:clothe_detail', 
#                                 args=[  self.slug,
#                                         self.activate.year,
#                                         self.activate.month,
#                                         self.activate.day,
#                                         self.id
#                                         ])
                                        

# def slug_generator(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
        
        


# pre_save.connect(slug_generator, sender=Clothe)
