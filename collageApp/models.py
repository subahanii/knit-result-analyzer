from django.db import models
from django.utils import timezone
# Create your models here.
class Students(models.Model):

	roll=models.CharField(max_length=20,primary_key=True)
	name=models.CharField(max_length=30)
	fname=models.CharField(max_length=30)
	course=models.CharField(max_length=30)


class Marks(models.Model):

	roll=models.CharField(max_length=20)
	semester=models.CharField(max_length=20)
	year_of_result=models.CharField(max_length=20)
	obtain_marks=models.FloatField(default=0)
	total_marks=models.FloatField(default=10.0)
	status=models.CharField(max_length=20)
	carry_over_status=models.IntegerField()
	dinank=models.DateTimeField(default=timezone.now)
	class Meta:
		unique_together = ('roll', 'semester',)


class Carryover(models.Model):

	roll=models.CharField(max_length=20)
	subject_code=models.CharField(max_length=20)
	obtain_marks=models.FloatField(default=0)
	year_of_result=models.CharField(max_length=20)
	semester=models.CharField(max_length=10)







