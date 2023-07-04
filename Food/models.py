from django.db import models
#from djongo import models

class Food(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ': ' + self.description
    
    class Meta:
        verbose_name_plural = 'Food'
    
    
class CourseMealCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ': ' + self.description
    
    class Meta:
        verbose_name_plural = 'Course Meal Categories'