from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime, timezone

from .models import *

# Create your views here.
def login(request):
    return render(request,"login.html")

def login_post(request):
    uname=request.POST['textfield']
    password=request.POST['textfield2']
    print(request.POST)

    loginobj= Login.objects.filter(username=uname,password=password)
    if loginobj.exists():
        ll=Login.objects.get(username=uname,password=password)
        request.session['login_id']=ll.id

        if ll.type == 'admin':
            return HttpResponse('''<script>alert("welcome Admin");window.location='/myapp/adm_home/'</script>''')
        elif ll.type=='Academy':
            return HttpResponse('''<script>alert("welcome Academy");window.location='/myapp/acd_home/'</script>''')
        else:
            return HttpResponse('''<script>alert("Not allowed");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert("Not allowed");window.location='/myapp/login/'</script>''')


def adm_add_game(request):
    return render(request, "Admin/adm_add_game.html")

def adm_add_game_post(request):
    game_name=request.POST['textfield']
    description=request.POST['textfield2']
    picture=request.FILES['fileField']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
    fs.save(date, picture)
    path = fs.url(date)

    gameobj = Game()
    gameobj.name = game_name
    gameobj.photo = path
    gameobj.description = description

    gameobj.save()

    return HttpResponse('''<script>alert("Game Added!!");window.location='/myapp/adm_home/'</script>''')

def adm_view_game(request):
    data = Game.objects.all()
    return render(request, "Admin/adm_view_game.html",{'htmldata':data})


def adm_change_password(request):
    return render(request, "Admin/adm_change_password.html")

def adm_change_password_post(request):
    current_password=request.POST['textfield']
    new_password = request.POST['textfield2']
    confirm_password = request.POST['textfield3']
    loginobj = Login.objects.filter(id=request.session['login_id'], password=current_password)
    if loginobj.exists():
        if new_password==confirm_password:
            Login.objects.filter(id=request.session['login_id'], password=current_password).update(password=new_password)
            return HttpResponse('''<script>alert("Password Changed Successfully!!");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert("Password doesn't match!!");window.location='/myapp/adm_change_password/'</script>''')
    else:
        return HttpResponse('''<script>alert("User not found!!");window.location='/myapp/adm_change_password/'</script>''')


def adm_edit_game(request,tid):
    data=Game.objects.get(id=tid)
    return render(request, "Admin/adm_edit_game.html",{'htmldata':data})

def adm_edit_game_post(request):
    game_name=request.POST['textfield']
    description=request.POST['textfield2']
    id=request.POST['uid']


    gameobj=Game.objects.get(id=id)
    if 'fileField' in request.FILES:
        picture = request.FILES['fileField']
        if picture != '':
            fs = FileSystemStorage()
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs.save(date, picture)
            path = fs.url(date)
            gameobj.photo = path

    gameobj.name = game_name
    gameobj.description = description
    gameobj.save()
    return HttpResponse('''<script>alert("Game Edited!!");window.location='/myapp/adm_view_game/'</script>''')


def adm_delete_game_post(request,tid):
    Game.objects.filter(id=tid).delete()
    return redirect('/myapp/adm_view_game/')


def adm_home(request):
    return render(request, "Admin/adm_home.html")


def adm_sent_reply(request,id):
    return render(request, "Admin/adm_sent_reply.html",{'id':id})

def adm_sent_reply_post(request):
    reply_field=request.POST['textfield']
    id=request.POST['uid']
    Complaint.objects.filter(id=id).update(status='Replied',reply=reply_field)
    return HttpResponse('''<script>alert("Reply Sent!!");window.location='/myapp/adm_view_complaints_sent_reply/'</script>''')


def adm_view_verify_academy(request):
    data=Academy.objects.filter(status='pending')
    return  render(request, "Admin/adm_view_verify_academy.html",{'data':data})

def adm_view_verify_academy_post(request):
    search=request.POST['textfield']
    data = Academy.objects.filter(status='pending',name__icontains=search)
    return render(request, "Admin/adm_view_verify_academy.html", {'data': data})

def adm_approve_academy(request,id):
    Academy.objects.filter(LOGIN_id=id).update(status='Approved')
    Login.objects.filter(id=id).update(type='Academy')
    return HttpResponse('''<script>alert("Academy Approved!!");window.location='/myapp/adm_view_verify_academy/'</script>''')


def adm_reject_academy(request,id):
    Academy.objects.filter(LOGIN_id=id).update(status='Rejected')
    Login.objects.filter(id=id).update(type='Rejected')
    return HttpResponse('''<script>alert("Academy Rejected!!");window.location='/myapp/adm_view_verify_academy/'</script>''')

def adm_view_rejected_academy_post(request):
    search=request.POST['textfield']
    data=Academy.objects.filter(status='rejected',name__icontains=search)
    return render(request, "Admin/adm_view_rejected_academy.html",{'data':data})


def adm_view_approved_academy(request):
    data=Academy.objects.filter(status='approved')
    return render(request, "Admin/adm_view_approved_academy.html",{'data':data})


def adm_view_approved_academy_post(request):
    search = request.POST['textfield']
    data=Academy.objects.filter(status='Approved',name__icontains=search)
    return render(request, "Admin/adm_view_approved_academy.html", {'data': data})


def adm_view_approved_coaches(request):
    data=Coach.objects.filter(status='approved')
    return render(request,"Admin/adm_view_approved_Coaches.html",{'data':data})

def adm_view_approved_coaches_post(request):
    search=request.POST['textfield']
    data=Coach.objects.filter(status='approved',name__icontains=search)
    return render(request,"Admin/adm_view_approved_Coaches.html",{'data':data})


def adm_approve_coaches(request,id):
    Coach.objects.filter(LOGIN_id=id).update(status='Approved')
    Login.objects.filter(id=id).update(type='Coach')
    return HttpResponse('''<script>alert("Coach Approved!!");window.location='/myapp/adm_view_coach_approve_reject/'</script>''')

def adm_reject_coaches(request,id):
    Coach.objects.filter(LOGIN_id=id).update(status='Rejected')
    Login.objects.filter(id=id).update(type='Coach')
    return HttpResponse('''<script>alert("Coach Rejected!!");window.location='/myapp/adm_view_coach_approve_reject/'</script>''')


def adm_view_coach_approve_reject(request):
    data=Coach.objects.filter(status='pending')
    return render(request, "Admin/adm_view_coach_approve_reject.html",{'data':data})

def adm_view_complaints_sent_reply(request):
    data=Complaint.objects.all()
    l=[]
    for i in data:
        ll=Login.objects.get(id=i.LOGIN.id)
        if ll.type == "Coach":
            name=Coach.objects.get(LOGIN_id=i.LOGIN.id).name
            l.append({
                "id":i.id,
                "date":i.date,
                "complaint":i.complaint,
                "reply":i.reply,
                "status":i.status,
                "name":name
            })
        elif ll.type=="Academy":
            name = Academy.objects.get(LOGIN_id=i.LOGIN.id).name
            l.append({
                "id": i.id,
                "date": i.date,
                "complaint": i.complaint,
                "reply": i.reply,
                "status": i.status,
                "name": name
            })
        elif ll.type=="Player":
            name = Player.objects.get(LOGIN_id=i.LOGIN.id).name
            l.append({
                "id": i.id,
                "date": i.date,
                "complaint": i.complaint,
                "reply": i.reply,
                "status": i.status,
                "name": name
            })
    return render(request, "Admin/adm_view_complaints_sent_reply.html",{'htmldata':l})

def adm_view_complaints_sent_reply_post(request):
    searchFrom=request.POST["textfield"]
    searchTo=request.POST["textfield2"]
    data=Complaint.objects.filter(date__range=[searchFrom,searchTo])
    l = []
    for i in data:
        ll = Login.objects.get(id=i.LOGIN.id)
        if ll.type == "coach":
            name = Coach.objects.get(LOGIN_id=i.LOGIN.id).name
            l.append({
                "id": i.id,
                "date": i.date,
                "complaint": i.complaint,
                "reply": i.reply,
                "status": i.status,
                "name": name
            })
        elif ll.type == "Academy":
            name = Academy.objects.get(LOGIN_id=i.LOGIN.id).name
            l.append({
                "id": i.id,
                "date": i.date,
                "complaint": i.complaint,
                "reply": i.reply,
                "status": i.status,
                "name": name
            })
        elif ll.type == "Player":
            name = Player.objects.get(LOGIN_id=i.LOGIN.id).name
            l.append({
                "id": i.id,
                "date": i.date,
                "complaint": i.complaint,
                "reply": i.reply,
                "status": i.status,
                "name": name
            })
    return render(request, "Admin/adm_view_complaints_sent_reply.html", {'htmldata': l})


def adm_view_rejected_academy(request):
    data=Academy.objects.filter(status='rejected')
    return render(request, "Admin/adm_view_rejected_academy.html",{'data':data})

def adm_view_rejected_coaches(request):
    data=Coach.objects.filter(status='rejected')
    return render(request, "Admin/adm_view_rejected_coaches.html",{'data':data})

def adm_view_rejected_coaches_post(request):
    search=request.POST['textfield']
    data = Coach.objects.filter(status='rejected', name__icontains=search)
    return render(request, "Admin/adm_view_rejected_coaches.html",{'data':data})


def adm_view_reviews_about_academy(request,id):
    data=Reviews.objects.filter(LOGIN_id=id)
    request.session['acd_lid']=id
    return render(request, "Admin/adm_view_reviews_about_academy_coach.html",{'htmldata':data})

def adm_view_reviews_about_academy_post(request):
    searchFrom = request.POST["textfield"]
    searchTo = request.POST["textfield2"]
    data=Reviews.objects.filter(LOGIN_id= request.session['acd_lid'],date__range=[searchFrom,searchTo])

    return render(request, "Admin/adm_view_reviews_about_academy_coach.html",{'htmldata':data})

def adm_view_reviews_about_coach(request,id):
    data=Reviews.objects.filter(LOGIN_id=id)
    request.session['coach_lid']=id

    return render(request, "Admin/adm_view_reviews_about_coach.html",{'htmldata':data})

def adm_view_reviews_about_coach_post(request):
    searchFrom = request.POST["textfield"]
    searchTo = request.POST["textfield2"]
    data = Reviews.objects.filter(LOGIN_id=request.session['coach_lid'], date__range=[searchFrom, searchTo])
    return render(request, "Admin/adm_view_reviews_about_coach.html",{'htmldata':data})


def adm_view_trails(request):
    data=Trials.objects.all()
    return render(request, "Admin/adm_view_trails.html",{'htmldata':data})

def adm_view_trails_post(request):
    searchFrom=request.POST['textfield']
    searchTo=request.POST['textfield2']
    data = Trials.objects.filter(date__range=[searchFrom,searchTo])
    return render(request, "Admin/adm_view_trails.html", {'htmldata': data})



#============Academy===============



def acd_home(request):
    return render(request,"Academy/home_index.html")

def acd_call_for_trials(request) :
    data=Game.objects.all()
    return  render(request, 'Academy/acd_call_for_trials.html',{'data':data})

def acd_call_for_trials_post(request) :
    game=request.POST['gameid']
    print(game)
    due_date=request.POST['textfield2']
    venue=request.POST['textfield3']
    age=request.POST['textfield4']
    description=request.POST['textfield5']
    id=request.session['login_id']

    trial_obj=Trials()
    trial_obj.ACADEMY=Academy.objects.get(LOGIN_id=id)
    trial_obj.name=game
    trial_obj.date=due_date
    trial_obj.age=age
    trial_obj.venue=venue
    trial_obj.description=description
    trial_obj.GAME_id=game
    trial_obj.save()

    return  HttpResponse('''<script>alert("Trial Called!!");window.location='/myapp/acd_home/'</script>''')


def acd_change_password(request) :
    return  render(request, "Academy/acd_change_password.html")

def acd_change_password_post(request) :

    current_password = request.POST['textfield']
    new_password = request.POST['textfield2']
    confirm_password = request.POST['textfield3']
    loginobj = Login.objects.filter(id=request.session['login_id'], password=current_password)
    if loginobj.exists():
        if new_password == confirm_password:
            Login.objects.filter(id=request.session['login_id'], password=current_password).update(
                password=new_password)
            return HttpResponse(
                '''<script>alert("Password Changed Successfully!!");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert("Password doesn't match!!");window.location='/myapp/acd_change_password/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert("User not found!!");window.location='/myapp/acd_change_password/'</script>''')



def acd_edit_profile(request,id) :
    data=Academy.objects.get(id=id)
    return  render(request, "Academy/edit_profile_intex.html",{"htmldata":data})

def acd_edit_profile_post(request) :
    name = request.POST['textfield']
    place = request.POST['textfield2']
    district = request.POST['textfield3']
    state = request.POST['select']
    nationality = request.POST['select2']
    phone = request.POST['textfield4']
    email = request.POST['textfield5']
    website = request.POST['textfield6']
    instaid = request.POST['textfield7']
    since = request.POST['textfield8']
    id = request.POST['id']

    acdobj=Academy.objects.get(id=id)

    if 'filefield1' in request.FILES:
        logo = request.FILES['filefield1']
        if logo != '':

            fs=FileSystemStorage()
            date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
            fs.save(date,logo)
            path=fs.url(date)
            acdobj.logo = path
            acdobj.save()


    if 'filefield' in request.FILES:
        proof = request.FILES['filefield']
        if proof != '':
            fs1=FileSystemStorage()
            date1=datetime.now().strftime('%Y%m%d-%H%M%S')+'-1.jpg'
            fs1.save(date1,proof)
            path1=fs1.url(date1)
            acdobj.proof = path1
            acdobj.save()


    acdobj.name=name
    acdobj.place=place
    acdobj.district=district
    acdobj.state=state
    acdobj.country=nationality
    acdobj.phone=phone
    acdobj.email=email
    acdobj.website=website
    acdobj.insta_id=instaid
    acdobj.since=since

    acdobj.save()
    return HttpResponse(''''<script>alert("Profile Edited!!");window.location='/myapp/acd_view_profile/'</script>''')


def acd_signup(request):
    return render(request, "Academy/acd_signup.html")

def acd_signup_post(request):
    name = request.POST['textfield']
    place = request.POST['textfield2']
    district = request.POST['textfield3']
    state = request.POST['select']
    nationality = request.POST['select2']
    phone = request.POST['textfield4']
    email = request.POST['textfield5']
    website = request.POST['textfield6']
    instaid = request.POST['textfield7']
    since = request.POST['textfield8']
    proof = request.FILES['filefield']
    logo = request.FILES['filefield2']
    password = request.POST['textfield9']
    confirmpassword = request.POST['textfield10']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
    fs.save(date,logo)
    path=fs.url(date)

    fs1=FileSystemStorage()
    date1=datetime.now().strftime('%Y%m%d-%H%M%S')+'-1.jpg'
    fs1.save(date1,proof)
    path1=fs1.url(date1)

    if password == confirmpassword:

        ll=Login()
        ll.username=email
        ll.password=password
        ll.type='pending'
        ll.save()

        acdobj=Academy()
        acdobj.name=name
        acdobj.logo=path
        acdobj.place=place
        acdobj.district=district
        acdobj.state=state
        acdobj.country=nationality
        acdobj.phone=phone
        acdobj.email=email
        acdobj.website=website
        acdobj.insta_id=instaid
        acdobj.since=since
        acdobj.proof=path1
        acdobj.status='pending'
        acdobj.LOGIN=ll

        acdobj.save()


        return HttpResponse(''''<script>alert("Welcome to our Project");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse(''''<script>alert("Incorrect Password!!");window.location='/myapp/acd_signup/'</script>''')


def acd_edit_trials(request,tid) :
    data=Trials.objects.get(id=tid)
    return  render(request, "Academy/edit_trials_index.html",{'htmldata':data})

def acd_edit_trials_post(request) :
    game=request.POST['textfield']
    due_date=request.POST['textfield2']
    venue=request.POST['textfield3']
    age=request.POST['textfield4']
    description=request.POST['textfield5']
    id = request.POST['uid']

    trialobj=Trials.objects.get(id=id)

    trialobj.name=game
    trialobj.date=due_date
    trialobj.venue=venue
    trialobj.age=age
    trialobj.description=description
    trialobj.save()

    return  HttpResponse('''<script>alert("Trial Edited!!");window.location='/myapp/acd_view_trials/'</script>''')

def acd_delete_trials_post(request,tid):
    Trials.objects.filter(id=tid).delete()
    return redirect('/myapp/acd_view_trials/')

def acd_message_with_players(request) :
    return  render(request, "Academy/acd_message_with_players.html")

def acd_message_with_players_post(request) :
    message=request.POST['textfield']
    return  HttpResponse('''<script>alert("Message Sent!!");window.location='/myapp/acd_home/'</script>''')


def acd_send_complaint(request) :
    return  render(request, "Academy/acd_send_complaint.html")

def acd_send_complaint_post(request) :
    complaint=request.POST['textfield']
    complobj=Complaint()
    complobj.date=datetime.now().today()
    complobj.complaint=complaint
    complobj.status='pending'
    complobj.reply='pending'
    complobj.LOGIN_id=request.session['login_id']
    complobj.save()
    return  HttpResponse('''<script>alert("Complaint Sent");window.location='/myapp/acd_home'</script>''')

def acd_view_reply(request):
    data = Complaint.objects.filter(LOGIN__id=request.session['login_id'])
    return render(request,"Academy/acd_view_reply.html",{'htmldata':data})

def acd_view_reply_post(request):
    searchFrom = request.POST['textfield']
    searchTo = request.POST['textfield2']
    data = Trial_Request.objects.filter(date__range=[searchFrom, searchTo])
    return render(request, 'Academy/acd_view_reply.html', {'htmldata': data})


def acd_view_player_for_trials(request) :
    data=Trial_Request.objects.filter(status='pending')
    return  render(request, "Academy/acd_view_player_for_trials.html",{'htmldata':data})

def acd_view_player_for_trials_post(request) :
    searchFrom = request.POST['textfield']
    searchTo = request.POST['textfield2']
    data = Trial_Request.objects.filter( date__range=[searchFrom, searchTo])
    return render(request,'Academy/acd_view_player_for_trials.html',{'htmldata':data})


def acd_approve_player(request,id):
    Trial_Request.objects.filter(id=id).update(status='Approved')
    return HttpResponse(
        '''<script>alert("You has been Approved for the Trials!!");window.location='/myapp/acd_view_player_for_trials/'</script>''')

def acd_reject_player(request,id):
    Trial_Request.objects.filter(id=id).update(status='Rejected')
    return HttpResponse('''<script>alert("Sorry!! You has been  Rejected for the Trials!!");window.location='/myapp/acd_view_player_for_trials/'</script>''')

def acd_rejected_player_for_trials(request):
    data=Trial_Request.objects.filter(status='Rejected')
    return render(request,'Academy/acd_view_rejected_player_for_trials.html',{'htmldata':data})

def acd_rejected_player_for_trials_post(request):
    searchFrom=request.POST['textfield']
    searchTo=request.POST['textfield2']
    data=Trial_Request.objects.filter(status='Rejected',date__range=[searchFrom,searchTo])
    return render(request,'Academy/acd_view_rejected_player_for_trials.html',{'htmldata':data})


def acd_approved_player_for_trials(request):
    data = Trial_Request.objects.filter(status='Approved')
    return render(request,'Academy/acd_view_approved_player_for_trials.html',{"htmldata":data})

def acd_approved_player_for_trials_post(request):
    searchFrom=request.POST['textfield']
    searchTo=request.POST['textfield2']
    data=Trial_Request.objects.filter(status='Approved',date__range=[searchFrom,searchTo])
    return render(request,'Academy/acd_view_approved_player_for_trials.html',{'htmldata':data})

def acd_attend_players(request,id):
    Trial_Request.objects.filter(id=id).update(status='Attended')
    return HttpResponse('''<script>alert("You are attended!!");window.location='/myapp/acd_approved_player_for_trials/'</script>''')

def acd_view_attended_players(request):
    data = Trial_Request.objects.filter(status='Attended')
    return render(request,'Academy/acd_view_attended_players.html',{"htmldata":data})

def acd_view_attended_players_post(request):
    search=request.POST['textfield']
    data = Trial_Request.objects.filter(status='Attended',PLAYER__name__icontains=search)
    return render(request, 'Academy/acd_view_attended_players.html', {'htmldata': data})


def acd_shortlist_players(request,id):
    Trial_Request.objects.filter(id=id).update(status='Shortlisted')
    return HttpResponse('''<script>alert("You are Shortlisted!!");window.location='/myapp/acd_view_attended_players/'</script>''')

def acd_view_shortlist_players(request):
    data = Trial_Request.objects.filter(status='Shortlisted')
    return render(request, 'Academy/acd_view_shortlist_players.html', {"htmldata":data})

def acd_view_shortlist_players_post(request):
    searchFrom = request.POST['textfield']
    searchTo = request.POST['textfield2']
    data = Trial_Request.objects.filter(status='Shortlisted',date__range=[searchFrom, searchTo])
    return render(request, "Academy/acd_view_shortlist_players.html", {'htmldata': data})


def acd_view_profile(request) :
    data=Academy.objects.get(LOGIN__id=request.session['login_id'])
    return  render(request, "Academy/profile_index.html",{"htmldata":data})


def acd_view_reviews(request) :
    data=Reviews.objects.all()
    return  render(request, "Academy/acd_view_reviews.html",{'htmldata':data})

def acd_view_reviews_post(request) :
    searchFrom = request.POST['textfield']
    searchTo = request.POST['textfield2']
    data = Trials.objects.filter(date__range=[searchFrom, searchTo])
    return render(request, "Academy/acd_view_reviews.html", {'htmldata': data})


def acd_view_trials(request):
    data=Trials.objects.all()
    return render(request, "Academy/view_trials_index.html",{'htmldata':data})

def acd_view_trials_post(request):
    searchFrom=request.POST['textfield']
    searchTo=request.POST['textfield2']
    data = Trials.objects.filter(date__range=[searchFrom,searchTo])
    return render(request, "Academy/acd_view_trials.html", {'htmldata': data})


################################# chat #######################


def chat(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Player.objects.get(LOGIN_id=cid)

    return render(request, "Academy/Chat.html", {'photo': qry.photo, 'name': qry.name, 'toid': cid})


def chat_view(request):
    fromid = request.session["login_id"]
    toid = request.session["userid"]
    qry = Player.objects.get(LOGIN_id=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.msg, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    return JsonResponse({'photo': qry.photo, "data": l, 'name': qry.name, 'toid': request.session["userid"]})


def chat_send(request, msg):
    lid = request.session["login_id"]
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.msg = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})





#----------------Player----------------#





def ply_login(request):
    uname = request.POST['username']
    password = request.POST['password']

    loginobj = Login.objects.filter(username=uname, password=password)
    if loginobj.exists():
        ll = Login.objects.get(username=uname, password=password)
        lid=ll.id
        if ll.type == 'player':
            return JsonResponse({'status':'ok','lid':str(lid),'type':ll.type})
        elif ll.type == 'coach':
            return JsonResponse({'status': 'ok', 'lid': str(lid), 'type': ll.type})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status': 'no'})

def ply_signup(request):
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    height = request.POST['height']
    weight = request.POST['weight']
    photo = request.POST['photo']
    h_name = request.POST['h_name']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    country = request.POST['country']
    email = request.POST['email']
    phone = request.POST['phone']
    password = request.POST['password']
    confirm_password = request.POST['confirmpassword']


    if Login.objects.filter(username=email).exists():
        return JsonResponse({'status':'no'})

    l=Login()
    l.username=email
    l.password=password
    l.type='pending'
    l.save()

    if password==confirm_password:

        import base64
        dt=datetime.now().strftime('%Y%m%d-%H%M%S')
        a=base64.b64decode(photo)
        ftime=open("C:\\Users\\talen\\OneDrive\\Desktop\\Rumaiz Flutter\\Project Ultra\\Project Ultra\\Selection_Trails Pycharm\\media\\"+dt+".jpg","wb")
        path="/media/"+dt+".jpg"
        ftime.write(a)
        ftime.close()

        player_obj=Player()

        player_obj.name=name
        player_obj.dob=dob
        player_obj.gender=gender
        player_obj.height=height
        player_obj.weight=weight
        player_obj.photo=path
        player_obj.h_name=h_name
        player_obj.place=place
        player_obj.city=city
        player_obj.state=state
        player_obj.country=country
        player_obj.email=email
        player_obj.phone=phone
        player_obj.LOGIN=l

        player_obj.save()

        return JsonResponse({'status': 'ok'})

def ply_apply_trial(request):
    tid=request.POST['tid']
    lid=request.POST['lid']

    trialreq_obj=Trial_Request()

    trialreq_obj.TRAIL_id=tid
    trialreq_obj.PLAYER=Player.objects.get(LOGIN=lid)
    trialreq_obj.date=datetime.now().today()
    trialreq_obj.status='pending'

    trialreq_obj.save()

    return JsonResponse({'status':'ok'})

def ply_change_password(request):
    current_password = request.POST['current_pass']
    new_password = request.POST['new_pass']
    confirm_password = request.POST['confirm_pass']
    lid=request.POST['lid']

    loginobj = Login.objects.filter(id=lid, password=current_password)

    if loginobj.exists():
        if new_password==confirm_password:
            Login.objects.filter(id=lid, password=current_password).update(password=new_password)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'ok'})

def ply_view_profile(request):
    lid=request.POST['lid']

    data=Player.objects.get(LOGIN=lid)

    return JsonResponse({'status':'ok',

                         'name':data.name,
                         'dob':data.dob,
                         'gender':data.gender,
                         'height':data.height,
                         'weight':data.weight,
                         'photo':data.photo,
                         'h_name':data.hname,
                         'place':data.place,
                         'city':data.city,
                         'state':data.state,
                         'email':data.email,
                         'country':data.country,
                         'phone':data.phone,

    })

def ply_edit_profile(request):
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    height = request.POST['height']
    weight = request.POST['weight']
    photo = request.POST['photo']
    h_name = request.POST['h_name']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    country = request.POST['country']
    email = request.POST['email']
    phone = request.POST['phone']
    lid = request.POST['lid']


    ply_obj=Player.objects.get(LOGIN=lid)
    if len(photo) > 0:
        import base64
        dt = datetime.now().strftime('%Y%m%d-%H%M%S')
        a = base64.b64decode(photo)
        ftime = open(
            "D:\\Rumaiz Codes\\Rumaiz Flutter\\Project Ultra\\Project Ultra\\Selection_Trails Pycharm\\media\\" + dt + ".jpg",
            "wb")
        path = "/media/" + dt + ".jpg"
        ftime.write(a)
        ftime.close()
        ply_obj.photo = path
        ply_obj.save()


    ply_obj.name=name
    ply_obj.dob=dob
    ply_obj.gender=gender
    ply_obj.height=height
    ply_obj.weight=weight
    ply_obj.h_name=h_name
    ply_obj.place=place
    ply_obj.city=city
    ply_obj.state=state
    ply_obj.country=country
    ply_obj.phone=phone
    ply_obj.email=email

    ply_obj.save()

    return JsonResponse({'status':'ok'})


def ply_view_coach_and_follow(request):


    lid = request.POST['lid']
    cid = request.POST['cid']

    flw_obj = Follow()
    flw_obj.date = datetime.today()
    flw_obj.status = "followed"

    flw_obj.PLAYER=Player.objects.get(LOGIN=lid)
    flw_obj.COACH_id=cid

    flw_obj.save()

    return JsonResponse({"status": "ok"})

def ply_view_trial(request):
    data = Trials.objects.all()
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "name": i.name,
            "date": i.date,
            "venue": i.venue,
            "description": i.description,
            "age": i.age,
            "status": i.TRIstatus,
            "game_name": i.GAME.name,
            "academy_name": i.ACADEMY.name,
        })

    return JsonResponse({"status": "ok", 'data': l})

def ply_view_followed_coach(request):
    lid = request.POST['lid']
    data = Follow.objects.filter(PLAYER__LOGIN_id=lid)
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "name": i.COACH.name,
            "dob": i.COACH.dob,
            "gender": i.COACH.gender,
            "photo": i.COACH.photo,
            "hname": i.COACH.h_name,
            "city": i.COACH.city,
            "place": i.COACH.place,
            "state": i.COACH.state,
            "email": i.COACH.email,
            "country": i.COACH.country,
            "phone": i.COACH.phone,
            "LOGIN_id": i.COACH.LOGIN.id,
        })

    return JsonResponse({"status": "ok", 'data': l})

def ply_view_applied_trials(request):
    lid = request.POST['lid']
    data = Trial_Request.objects.filter(PLAYER__LOGIN_id=lid)
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "date": i.date,
            "status": i.status,
        })

    return JsonResponse({"status": "ok", 'data': l})

def ply_view_certificate_of_coach(request):
    cid = Coach.objects.all()
    data = Follow.objects.get(COACH__LOGIN_id=cid)
    var = Certificates.objects.get(COACH_id=data,)
    l = []
    for i in var:
        l.append({
            "id": i.id,
            "certificate_type": i.certificate_type,
            "file": i.file,
            "date": i.date,
        })

    return JsonResponse({"status": "ok", 'data': l})

def ply_view_tips(request):
    tip_obj = Tips.objects.all()
    l = []

    for i in tip_obj:
        l.append({
            "tip_title": i.tip_title,
            "tip_description": i.tip_description,
            "tip_of": i.COACH.name,
            "id": i.id,

        })

    return JsonResponse({"status": "ok", "data": l})

def ply_view_experience(request):
    exp_obj = Experience.objects.all()
    l = []

    for i in exp_obj:
        l.append({
            "academy_name": i.academy_name,
            "from_year": i.from_year,
            "to_year": i.to_year,
            "position": i.position,
            "exp_of": i.COACH.username,
            "id": i.id,

        })

    return JsonResponse({"status": "ok", "data": l})

def ply_send_review_about_academy(request):
    review = request.POST['review']
    rating = request.POST['rating']

    lid = request.POST['lid']
    a_login_id = request.POST['aid']

    rev_obj = Reviews()
    rev_obj.date = datetime.today()
    rev_obj.LOGIN_id = a_login_id
    rev_obj.PLAYER = Player.objects.get(LOGIN_id=lid)
    rev_obj.review = review
    rev_obj.rating = rating

    rev_obj.save()

    return JsonResponse({"status": "ok"})

def ply_send_review_about_coach(request):
    review = request.POST['review']
    rating = request.POST['rating']

    lid = request.POST['lid']
    a_login_id = request.POST['aid']

    rev_obj = Reviews()
    rev_obj.date = datetime.today()
    rev_obj.LOGIN_id = a_login_id
    rev_obj.PLAYER = Player.objects.get(LOGIN_id=lid)
    rev_obj.review = review
    rev_obj.rating = rating

    rev_obj.save()

    return JsonResponse({"status": "ok"})

def ply_view_achievement_of_coach(request):
    data = Achievements.objects.all()
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "coach_name": i.COACH.name,
            "achievement": i.achievement,
            "event": i.event,

        })

    return JsonResponse({"status": "ok", 'data': l})

#----------------Chat with Coach----------------#


def ply_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.msg=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def ply_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.msg, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})

def ply_view_chat_coach(request):

    data = Coach.objects.all()
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "name": i.name,
            "dob": i.dob,
            "gender": i.gender,
            "photo": i.photo,
            "hname": i.h_name,
            "city": i.city,
            "place": i.place,
            "state": i.state,
            "email": i.email,
            "country": i.country,
            "phone": i.phone,
            "LOGIN_id": i.LOGIN.id,
        })


    return JsonResponse({"status": "ok", 'data': l})

def ply_view_chat_academy(request):
    data = Academy.objects.all()
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "name": i.name,
            "since": i.since,
            "logo": i.logo,
            "proof": i.proof,
            "district": i.district,
            "place": i.place,
            "state": i.state,
            "email": i.email,
            "insta_id": i.insta_id,
            "website": i.website,
            "country": i.country,
            "phone": i.phone,
            "LOGIN_id": i.LOGIN.id,
        })

    return JsonResponse({"status": "ok", 'data': l})
#--------------------------------#



#----------------Chat with Academy----------------#


def ply_sendchat_acd(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.msg=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def ply_viewchat_acd(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.msg, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})

def ply_view_chat_acd(request):

    # data = Academy.objects.filter(Trials__Trial_Request__PLAYER=request.user.player,
    #                               Trials__Trial_Request__status='Approved').distinct()

    data = Academy.objects.filter(status="Approved")

    # data = Trial_Request.objects.get(TRAIL_id__ACADEMY_)
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "name": i.name,
            "logo": i.logo,
            "district": i.district,
            "website": i.website,
            "insta_id": i.insta_id,
            "since": i.since,
            "place": i.place,
            "state": i.state,
            "email": i.email,
            "country": i.country,
            "phone": i.phone,
            "proof": i.proof,
            "LOGIN_id": i.LOGIN.id,
        })


    return JsonResponse({"status": "ok", 'data': l})






#--------------------------------#


#----------------Coach----------------#


def coc_change_password(request):
    current_password = request.POST['current_pass']
    new_password = request.POST['new_pass']
    confirm_password = request.POST['confirm_pass']
    lid=request.POST['lid']

    loginobj = Login.objects.filter(id=lid, password=current_password)

    if loginobj.exists():
        if new_password==confirm_password:
            Login.objects.filter(id=lid, password=current_password).update(password=new_password)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'ok'})


def coc_signup(request):
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    photo = request.POST['photo']
    h_name = request.POST['h_name']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    country = request.POST['country']
    email = request.POST['email']
    phone = request.POST['phone']
    password = request.POST['password']
    confirm_password = request.POST['confirmpassword']

    l=Login()
    l.username=email
    l.password=password
    l.type='pending'
    l.save()

    if password==confirm_password:

        import base64
        dt=datetime.now().strftime('%Y%m%d-%H%M%S')
        a=base64.b64decode(photo)
        ftime=open("C:\\Users\\talen\\OneDrive\\Desktop\\Rumaiz Flutter\\Project Ultra\\Project Ultra\\Selection_Trails Pycharm\\media\\"+dt+".jpg","wb")
        path="/media/"+dt+".jpg"
        ftime.write(a)
        ftime.close()

        coc_obj=Coach()

        coc_obj.name=name
        coc_obj.dob=dob
        coc_obj.gender=gender
        coc_obj.photo=path
        coc_obj.h_name=h_name
        coc_obj.place=place
        coc_obj.city=city
        coc_obj.state=state
        coc_obj.country=country
        coc_obj.email=email
        coc_obj.phone=phone
        coc_obj.LOGIN=l

        coc_obj.save()

        return JsonResponse({'status': 'ok'})

def coc_view_profile(request):
    lid = request.POST['lid']

    data = Coach.objects.get(LOGIN=lid)

    return JsonResponse({'status': 'ok',

                         'name': data.name,
                         'dob': data.dob,
                         'gender': data.gender,
                         'photo': data.photo,
                         'h_name': data.h_name,
                         'place': data.place,
                         'city': data.city,
                         'state': data.state,
                         'email': data.email,
                         'country': data.country,
                         'phone': data.phone,

    })

def coc_edit_profile(request):
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    photo = request.POST['photo']
    h_name = request.POST['h_name']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    country = request.POST['country']
    email = request.POST['email']
    phone = request.POST['phone']
    lid = request.POST['lid']

    coc_obj = Coach.objects.get(LOGIN=lid)
    if len(photo)>0:
        import base64
        dt = datetime.now().strftime('%Y%m%d-%H%M%S')
        a = base64.b64decode(photo)
        ftime = open(
            "C:\\Users\\talen\\OneDrive\\Desktop\\Rumaiz Flutter\\Project Ultra\\Project Ultra\\Selection_Trails Pycharm\\media\\" + dt + ".jpg",
            "wb")
        path = "/media/" + dt + ".jpg"
        ftime.write(a)
        ftime.close()
        coc_obj.photo = photo
        coc_obj.save()

    coc_obj.name = name
    coc_obj.dob = dob
    coc_obj.gender = gender
    coc_obj.phone = phone
    coc_obj.email = email
    coc_obj.h_name = h_name
    coc_obj.place = place
    coc_obj.city = city
    coc_obj.state = state
    coc_obj.country = country

    coc_obj.save()

    return JsonResponse({'status':'ok'})

def coc_add_experience(request):

        name = request.POST['name']
        fromyear = request.POST['fromyear']
        toyear = request.POST['toyear']
        position = request.POST['position']
        lid = request.POST['lid']

        exp_obj = Experience()

        exp_obj.COACH_id=lid
        exp_obj.academy_name = name
        exp_obj.from_year = fromyear
        exp_obj.to_year = toyear
        exp_obj.position = position

        exp_obj.save()

        return JsonResponse({"status": "ok"})

def coc_view_experience(request):
    lid=request.POST['lid']
    coc_obj=Coach.objects.get(LOGIN=lid).LOGIN.id
    exp_obj=Experience.objects.filter(COACH_id=coc_obj)
    l=[]

    for i in exp_obj:
        l.append({
            "name":i.academy_name,
            "fromyear":i.from_year,
            "toyear":i.to_year,
            "position":i.position,
            "id":i.id,


        })

    return JsonResponse({"status":"ok","data":l})

def coc_edit_experience(request):
    name = request.POST['name']
    fromyear = request.POST['fromyear']
    toyear = request.POST['toyear']
    position = request.POST['position']
    lid = request.POST['lid']

    exp_obj = Experience.objects.get(id=lid)

    exp_obj.academy_name=name
    exp_obj.from_year=fromyear
    exp_obj.to_year=toyear
    exp_obj.position=position

    exp_obj.save()

    return JsonResponse({"status":"ok"})

def coc_edit_experience_get(request):
    lid = request.POST['lid']
    print(lid,"lllllllllllllllll")

    i = Experience.objects.get(id=lid)

    return JsonResponse({"status": "ok",
                         "name": i.academy_name,
                         "fromyear": i.from_year,
                         "toyear": i.to_year,
                         "position": i.position,
                         })

def coc_view_reply(request):
    lid = request.POST['lid']
    comp_obj = Complaint.objects.filter(LOGIN_id=lid)
    l = []

    for i in comp_obj:
        l.append({
            "date": i.date,
            "complaint": i.complaint,
            "status": i.status,
            "reply": i.reply,
            "id": i.id,

        })

    return JsonResponse({"status": "ok", "data": l})

def coc_send_complaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']

    comp_obj = Complaint()
    comp_obj.date = datetime.today()
    comp_obj.LOGIN_id = lid
    comp_obj.complaint = complaint
    comp_obj.status="pending"

    comp_obj.save()

    return JsonResponse({"status": "ok"})

def coc_add_tips(request):
    tip_title = request.POST['tip_title']
    tip_description = request.POST['tip_description']
    lid = request.POST['lid']

    tip_obj = Tips()

    tip_obj.COACH_id = lid
    tip_obj.tip_title = tip_title
    tip_obj.tip_description = tip_description

    tip_obj.save()

    return JsonResponse({"status": "ok"})


def coc_view_tips(request):
    tip_obj = Tips.objects.all()
    l = []

    for i in tip_obj:
        l.append({
            "tip_title": i.tip_title,
            "tip_description": i.tip_description,
            "id": i.id,

        })

    return JsonResponse({"status": "ok", "data": l})

def coc_edit_tips(request):
    tip_title = request.POST['tip_title']
    tip_description = request.POST['tip_description']
    lid = request.POST['lid']

    tip_obj = Tips.objects.get(id=lid)

    tip_obj.tip_title=tip_title
    tip_obj.tip_description=tip_description

    tip_obj.save()

    return JsonResponse({"status":"ok"})

def coc_edit_tips_get(request):
    lid = request.POST['lid']
    print(lid,"lllllllllllllllll")

    i = Tips.objects.get(id=lid)

    return JsonResponse({"status": "ok",
                         "tip_title": i.tip_title,
                         "tip_description": i.tip_description,
                         })


def coc_add_achievement(request):
    achievement = request.POST['achievement']
    event = request.POST['event']
    lid = request.POST['lid']

    achievement_obj=Achievements()

    achievement_obj.achievement=achievement
    achievement_obj.event=event
    achievement_obj.COACH_id=lid

    achievement_obj.save()

    return JsonResponse({'status':'ok'})

def coc_view_achievement(request):
    ach_obj = Achievements.objects.all()
    l = []

    for i in ach_obj:
        l.append({
            "achievement": i.achievement,
            "event": i.event,
            "id": i.id,

        })

    return JsonResponse({"status": "ok", "data": l})

def coc_edit_achievement(request):
    achievement = request.POST['achievement']
    event = request.POST['event']
    lid = request.POST['lid']

    ach_obj = Achievements.objects.get(id=lid)

    ach_obj.achievement=achievement
    ach_obj.event=event

    ach_obj.save()

    return JsonResponse({"status":"ok"})

def coc_edit_achievement_get(request):
    lid = request.POST['lid']
    print(lid,"lllllllllllllllll")

    i = Achievements.objects.get(id=lid)

    return JsonResponse({"status": "ok",
                         "achievement": i.achievement,
                         "event": i.event,
                         })

def coc_add_certificate(request):
    certificate_type = request.POST['certificate_type']
    file = request.POST['file']
    lid = request.POST['lid']

    from datetime import datetime
    import base64
    dt=datetime.today()
    a=base64.b64decode(file)
    fs=open("D:\\Rumaiz Codes\\Rumaiz Flutter\\Project Ultra\\Project Ultra\\Selection_Trails Pycharm\\media\\"+dt+".jpg","wb")
    path='/media/'+dt+".jpg"
    fs.write(a)
    fs.close()

    cert_type = Certificates()
    cert_type.certificate_type = certificate_type
    cert_type.date = dt
    cert_type.COACH = Coach.objects.get(LOGIN=lid)
    cert_type.file = path
    cert_type.save()

    return JsonResponse({"status": "ok"})

def coc_view_reviews(request):
    rev_obj = Reviews.objects.all()
    l = []

    for i in rev_obj:
        l.append({
            "review": i.review,
            "rating": i.rating,
            "date": i.date,
            "player": i.PLAYER.name,
            "id": i.id,

        })

    return JsonResponse({"status": "ok", "data": l})


#----------------Chat with Player----------------#


def coc_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.msg=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def coc_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.msg, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})

def coc_view_chat_player(request):

    data = Player.objects.all()
    l = []
    for i in data:
        l.append({
            "id": i.id,
            "name": i.name,
            "dob": i.dob,
            "gender": i.gender,
            "height": i.height,
            "weight": i.weight,
            "photo": i.photo,
            "hname": i.hname,
            "city": i.city,
            "place": i.place,
            "state": i.state,
            "email": i.email,
            "country": i.country,
            "phone": i.phone,
            "LOGIN_id": i.LOGIN.id,
        })


    return JsonResponse({"status": "ok", 'data': l})

#--------------------------------#