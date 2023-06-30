from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
from django.core.mail import send_mail
# Create your views here.

def home(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        context = {
            'uid': uid,
        }
        return render(request, "vehicleapp/index.html", context)
    else:
        return redirect("login")

def logout(request):
    if "email" in request.session:
        del request.session['email']
        return redirect("home")
    else:
        return redirect("home")

def login(request):
    if "email" in request.session:
        return redirect("home")
    else:
        if request.POST:
            p_email = request.POST['email']
            p_password = request.POST['password']
            try:
                uid = User.objects.get(email=p_email)
                if uid.password == p_password:

                    print("------>Sign in button pressed---->", uid)
                    print(uid.password)
                    request.session['email'] = uid.email  # session store
                    # request.session.set_expiry(10)
                    return redirect("home")
                else:
                    context = {
                        'e_msg': "Invalid Password !!"
                    }
                    print("-------------------Something went wrong")
                    return render(request, "vehicleapp/login.html", context)
            except:
                context = {
                    'e_msg': "Invalid Email Address !!"
                }
                print("-------------------Something went wrong")
                return render(request, "vehicleapp/login.html", context)
        else:
            print("------>Login page refresh")
            return render(request, "vehicleapp/login.html")
        
def signup(request):
    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        contact = request.POST['contact']

        uid = User.objects.create(
            email=email, password=password, firstname=firstname, lastname=lastname, contact=contact)
        msg = "Successfully Account Created !!"
        context = {
            'msg': msg,
            'uid': uid,
        }
        return render(request, "vehicleapp/login.html", context)
    else:
        return render(request, "vehicleapp/signup.html")

def profile(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])

        context = {
            'uid': uid,
        }
        return render(request, "vehicleapp/profile.html", context)
    else:
        return render(request, "vehicleapp/login.html")
    
def change_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.POST:
            if "picture" in request.FILES:
                uid.pic = request.FILES['picture']

            uid.firstname = request.POST['firstname']
            uid.lastname = request.POST['lastname']
            uid.contact = request.POST['contact']

            uid.save()
            context = {
                'uid': uid,
            }
            return render(request, "vehicleapp/profile.html", context)
        else:
            context = {
                'uid': uid,
            }
            return render(request, "vehicleapp/account.html", context)
    else:
        return render(request, "vehicleapp/login.html")
    
def help(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.POST:
            hid = Help.objects.create(
                user_id=uid,
                message=request.POST['message'],
            )
            reid = HelpReply.objects.create(
                help_id=hid,
                user_id=uid
            )
            msg = "Successfully Added !!"
            context = {
                'uid': uid,
                'hid': hid,
                'msg': msg,
                'reid': reid
            }
            return render(request, "vehicleapp/help.html", context)
        else:
            context = {
                'uid': uid,
            }
            return render(request, "vehicleapp/help.html", context)
    else:
        return redirect("login")

def helpreply(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])

        rid = HelpReply.objects.filter(user_id=uid)

        print("========>rid :", rid)

        for i in rid:
            print(i.reply)

        context = {
            'uid': uid,
            # 'hid': hid,
            'rid': rid,
        }
        return render(request, "vehicleapp/helpreply.html", context)
    
def ride(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.POST:
            rid = Ride.objects.create(
                r_email=uid.email,
                sloc=request.POST['sloc'],
                dloc=request.POST['dloc'],
                date=request.POST['date'],
                time=request.POST['time']
            )
            did=Drive.objects.all()
            context = {
                'uid': uid,
                'rid': rid,
                'did':did
            }
            return render(request, "vehicleapp/showdrivers.html", context)
        else:
            context = {
                'uid': uid,
            }
            return render(request, "vehicleapp/ride.html", context)
    else:
        return redirect("login")
    
def drive(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.POST:
            
            did = Drive.objects.create(
                d_email=uid.email,
                vehicle_num=request.POST['vehicle_num'],
                license_num=request.POST['license_num'],
                sloc=request.POST['sloc'],
                dloc=request.POST['dloc'],
                date=request.POST['date'],
                time=request.POST['time']
            )
            context = {
                'uid': uid,
                'did': did,
            }
            return render(request, "vehicleapp/drive.html", context)
        else:
            context = {
                'uid': uid,
            }
            return render(request, "vehicleapp/drive.html", context)
    else:
        return redirect("login")

def book(request,did):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        did=Drive.objects.get(id=did)
        rid=Ride.objects.get(r_email=uid)
        book=RideBook.objects.create(
            r_email=uid.email,
            d_email=did.d_email,
            sloc=rid.sloc,
            dloc=rid.dloc,
            date=rid.date,
            time=rid.time
        )
        context = {
                'uid': uid, 
                'book':book,
                'rid':rid,
            }

        return render(request, "vehicleapp/book.html",context)

def request(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        dinfo=RideBook.objects.filter(d_email=uid,status='PENDING')
        context = {
                'uid': uid, 
                'dinfo':dinfo,
            }
        return render(request, "vehicleapp/request.html",context)
        
def d_activity(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        dinfo=RideBook.objects.filter(d_email=uid)
        context = {
                'uid': uid, 
                'dinfo':dinfo
            }
        return render(request, "vehicleapp/d_activity.html",context)
    
def r_activity(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        rinfo=RideBook.objects.filter(r_email=uid)  
        context = {
                'uid': uid, 
                'rinfo':rinfo
            }
        return render(request, "vehicleapp/r_activity.html",context)
    
def accept(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        ainfo=RideBook.objects.get(d_email=uid)
        if  request.POST:
            ainfo.status="Accepted"
            ainfo.save()
   
        context = {
                'uid': uid, 
                'ainfo':ainfo
            }
        return render(request, "vehicleapp/request.html",context)
    
def reject(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        ainfo=RideBook.objects.get(d_email=uid)
        if  request.POST:
            ainfo.status="Rejected"
            ainfo.save()
   
        context = {
                'uid': uid, 
                'ainfo':ainfo
            }
        return render(request, "vehicleapp/requset.html",context)