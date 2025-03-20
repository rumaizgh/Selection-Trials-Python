from django.db import models

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=50)

class Player(models.Model):
    name=models.CharField(max_length=50)
    dob=models.DateField()
    gender=models.CharField(max_length=20)
    height=models.FloatField()
    weight=models.FloatField()
    photo=models.CharField(max_length=100)
    hname=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    status=models.CharField(max_length=20,default="status")
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Academy(models.Model):
    name=models.CharField(max_length=50)
    logo=models.CharField(max_length=100)
    place=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    website=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    insta_id=models.CharField(max_length=50)
    since=models.DateField()
    proof=models.CharField(max_length=100)
    status=models.CharField(max_length=20)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Coach(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    dob = models.DateField()
    h_name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    photo = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    status = models.CharField(max_length=20,default='pending')
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Game(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=100)
    description=models.CharField(max_length=1000)

class Trials(models.Model):
    name=models.CharField(max_length=50)
    date=models.DateField()
    venue=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    age=models.CharField(max_length=20)
    GAME=models.ForeignKey(Game,on_delete=models.CASCADE)
    ACADEMY=models.ForeignKey(Academy,on_delete=models.CASCADE)

class Trial_Request(models.Model):
    TRIALS= models.ForeignKey(Trials,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=50)
    PLAYER=models.ForeignKey(Player,on_delete=models.CASCADE)

class Chat(models.Model):
    FROM=models.ForeignKey(Login,on_delete=models.CASCADE,related_name="fromid")
    TO = models.ForeignKey(Login, on_delete=models.CASCADE,related_name="toid")
    msg = models.CharField(max_length=200)
    date = models.DateField()

class Complaint(models.Model):
    date = models.DateField()
    complaint = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    reply = models.CharField(max_length=200)

class Reviews(models.Model):
    date = models.DateField()
    review = models.CharField(max_length=100)
    rating = models.BigIntegerField()
    PLAYER = models.ForeignKey(Player, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class Certificates(models.Model):
    COACH = models.ForeignKey(Coach, on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=100)
    file = models.CharField(max_length=500)
    date = models.DateField()

class Achievements(models.Model):
    COACH = models.ForeignKey(Coach, on_delete=models.CASCADE)
    achievement=models.CharField(max_length=100)
    event = models.CharField(max_length=100)

class Experience(models.Model):
    COACH = models.ForeignKey(Login, on_delete=models.CASCADE,related_name="added")
    academy_name=models.CharField(max_length=50)
    from_year=models.DateField()
    to_year=models.DateField()
    position=models.CharField(max_length=20)

class Tips(models.Model):
    COACH = models.ForeignKey(Coach, on_delete=models.CASCADE)
    tip_title=models.CharField(max_length=20)
    tip_description=models.CharField(max_length=300)

class Video(models.Model):
    COACH = models.ForeignKey(Coach, on_delete=models.CASCADE)
    date = models.DateField()
    video_title=models.CharField(max_length=20)
    video_file=models.CharField(max_length=100)
    video_details=models.CharField(max_length=200)

class Follow(models.Model):
    COACH = models.ForeignKey(Coach, on_delete=models.CASCADE)
    PLAYER = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)


