from datetime import date, datetime
from django.db import models

# Create your models here.


class Employee(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    direction = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)


class DeptDirector(Employee):
    department = models.CharField(max_length=200)


class OfficeClerk(Employee):
    department = models.CharField(max_length=200)
    office = models.CharField(max_length=200)


class Activity(models.Model):
    activityId = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    releaseDate = models.DateField(default=date.today)
    deadline = models.DateField()
    complete = models.BooleanField()
    senderId = models.CharField(max_length=100)


class Task(Activity):
    receiverId = models.CharField(max_length=100)
    projectId = models.IntegerField()
    approved = models.BooleanField()


class Project(Activity):
    numberOfTasks = models.IntegerField()


class Direction(models.Model):
    directionId = models.CharField(max_length=200, unique=True)
    directionName = models.CharField(max_length=200, unique=True)


class Department(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, )
    departmentId = models.CharField(max_length=200)
    departmentName = models.CharField(max_length=200)


class Office(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, )
    officeId = models.CharField(max_length=200)
    officeName = models.CharField(max_length=200)


class Notification(models.Model):
    notId = models.IntegerField()
    message = models.CharField(max_length=1000)
    activityId = models.IntegerField()
    notDate = models.DateField(default=date.today)
    receiverId = models.CharField(max_length=200)
    isShown = models.BooleanField(default=False)


class Comment(models.Model):
    activity = models.ForeignKey(Task, on_delete=models.CASCADE, )
    commentId = models.IntegerField()
    message = models.CharField(max_length=2000)
    sentBySender = models.BooleanField()
    time = models.DateTimeField(default=datetime.now, blank=True)
