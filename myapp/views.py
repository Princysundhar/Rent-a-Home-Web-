import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def log(request):
    return render(request,"login_index.html")

def log_post(request):
    username = request.POST['textfield']
    password = request.POST['textfield2']
    data = login.objects.filter(username=username,password=password)
    if data.exists():
        data = data[0]
        request.session['lid'] = data.id
        request.session['lg'] = "lin"
        if data.usertype == 'admin':
            return HttpResponse("<script>alert('Login Success');window.location='/admin_home'</script>")
        elif data.usertype == 'user':
            return HttpResponse("<script>alert('Welcome to userhome');window.location='/user_home'</script>")
        else:
            return HttpResponse("<script>alert('User is Blocked,wait for to unclock!!');window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('Invalid');window.location='/'</script>")


def admin_home(request):
    return render(request,"admin/admin_index.html")

def user_home(request):
    return render(request,"user/user_index.html")

def logout(request):
    request.session['lg'] = ""
    return HttpResponse("<script>alert('Logout succesfully');window.location='/'</script>")

def forgot_password(request):
    return render(request,"forgot_password.html")

def forgot_password_post(request):
    email = request.POST['textfield2']
    data = login.objects.filter(username=email)
    if data.exists():
        pwd = data[0].password
        import smtplib

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("demo@gmail.com", "tcap lzzh lmrz afio")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "demo@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Rent a home Website"
        body = "Your Password is:- - " + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return HttpResponse("<script>alert('password sended');window.location='/'</script>")


    return HttpResponse("mail incorrect")


# ================================ ADMIN MODULE =================================

def change_password(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "CHANGE PASSWORD"
    return render(request,"admin/change_password.html")

def change_password_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    res = login.objects.filter(password=old,id=request.session['lid'])
    if res.exists():
        if new == confirm:
            login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse("<script>alert('Password updated');window.location='/change_password'</script>")
        else:
            return HttpResponse("<script>alert('Password mismatch');window.location='/change_password'</script>")
    else:
        return HttpResponse("<script>alert('Doesnt Exists!! ');window.location='/change_password'</script>")


def view_user(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW USER"
    data  = user.objects.all()
    return render(request,"admin/view_user.html",{"data":data})

def block_user(request,id):
    login.objects.filter(id=id).update(usertype='blocked')
    return HttpResponse("<script>alert('user blocked');window.location='/view_user#aa'</script>")

def unblock_user(request,id):
    login.objects.filter(id=id).update(usertype='user')
    return HttpResponse("<script>alert('user unblocked');window.location='/view_user#aa'</script>")


def view_complaint(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW COMPLAINT"
    data = complaint.objects.all()
    return render(request,"admin/view_complaint.html",{"data":data})

def send_reply(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "SEND REPLY"
    return render(request,"admin/send_reply.html",{"id":id})

def send_reply_post(request,id):
    reply = request.POST['textarea']
    complaint.objects.filter(id=id).update(reply = reply,reply_date = datetime.datetime.now().date())
    return HttpResponse("<script>alert('Success');window.location='/view_complaint#aa'</script>")

def view_home_and_verify(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW HOME"
    data = home.objects.filter(status='pending')
    return render(request,"admin/view_verify_home.html",{"data":data})

def accept_home(request,id):
    home.objects.filter(id=id).update(status='home',booking_status='free')
    return HttpResponse("<script>alert('Accepted');window.location='/view_home_and_verify#aa'</script>")


def reject_home(request,id):
    home.objects.filter(id=id).update(status='reject')
    return HttpResponse("<script>alert('Rejected');window.location='/view_home_and_verify#aa'</script>")


# ========================= USER ===============================================

def user_register(request):
    return render(request, "user/register_index.html")

def user_register_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    contact = request.POST['textfield3']
    gender = request.POST['RadioGroup1']
    age = request.POST['textfield4']
    place = request.POST['textfield5']
    post = request.POST['textfield6']
    pin = request.POST['textfield7']
    password = request.POST['textfield8']
    data = login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('User already exists!!');window.location='/user_register'</script>")
    else:
        obj1 = login()
        obj1.username = email
        obj1.password = password
        obj1.usertype = 'user'
        obj1.save()

        obj = user()
        obj.name = name
        obj.email = email
        obj.contact = contact
        obj.gender = gender
        obj.age = age
        obj.place = place
        obj.post = post
        obj.pin = pin
        obj.LOGIN = obj1
        obj.save()
        return HttpResponse("<script>alert('Registration Success');window.location='/'</script>")

def user_change_password(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "CHANGE PASSWORD"
    return render(request, "user/change_password.html")

def user_change_password_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    res = login.objects.filter(password=old, id=request.session['lid'])
    if res.exists():
        if new == confirm:
            login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse("<script>alert('Password updated');window.location='/user_change_password'</script>")
        else:
            return HttpResponse("<script>alert('Password not updated');window.location='/user_change_password'</script>")
    else:
        return HttpResponse("<script>alert('Password mismatch');window.location='/user_change_password'</script>")


# ========== HOME MANAGEMENT ==================

def add_home(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "ADD HOME"
    return render(request, "user/add_home.html")

def add_home_post(request):
    house_name = request.POST['textfield']
    house_no = request.POST['textfield2']
    amount = request.POST['textfield3']
    image = request.FILES['fileField']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\PycharmProjects\Rent_A_Home\myapp\static\home_image\\" + dt + '.jpg',image)
    path = '/static/home_image/'+dt+'.jpg'
    square_feet = request.POST['textfield4']
    rooms = request.POST['textfield5']
    latitude = request.POST['textfield8']
    longitude = request.POST['textfield9']
    data = home.objects.filter(house_no=house_no)
    if data.exists():
        return HttpResponse("<script>alert('Home already exists!!');window.location='/add_home'</script>")
    else:
        obj = home()
        obj.house_name = house_name
        obj.house_no = house_no
        obj.amount = amount
        obj.image = path
        obj.square_feet = square_feet
        obj.no_of_rooms = rooms
        obj.latitude = latitude
        obj.longitude = longitude
        obj.status = 'pending'
        obj.USER = user.objects.get(LOGIN=request.session['lid'])
        obj.booking_status = 'free'
        obj.save()
        return HttpResponse("<script>alert('Success');window.location='/add_home'</script>")

def view_home(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW HOME"
    data = home.objects.filter(USER__LOGIN=request.session['lid'])
    return render(request, "user/view_home.html", {"data":data})

def edit_home(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "EDIT HOME"
    data = home.objects.get(id=id)
    return render(request, "user/edit_home.html", {"data":data, "id":id})

def edit_home_post(request,id):
    try:
        house_name = request.POST['textfield']
        house_no = request.POST['textfield2']
        image = request.FILES['fileField']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\DELL\PycharmProjects\Rent_A_Home\myapp\static\home_image\\" + dt + '.jpg', image)
        path = '/static/home_image/' + dt + '.jpg'
        square_feet = request.POST['textfield4']
        rooms = request.POST['textfield5']
        latitude = request.POST['textfield8']
        longitude = request.POST['textfield9']
        home.objects.filter(id=id).update(house_name = house_name,house_no = house_no,image = path,square_feet = square_feet,
                                          no_of_rooms = rooms,latitude = latitude,longitude = longitude)
        return HttpResponse("<script>alert('Updated');window.location='/view_home#aa'</script>")
    except Exception as e:
        house_name = request.POST['textfield']
        house_no = request.POST['textfield2']
        square_feet = request.POST['textfield4']
        rooms = request.POST['textfield5']
        latitude = request.POST['textfield8']
        longitude = request.POST['textfield9']
        home.objects.filter(id=id).update(house_name=house_name, house_no=house_no,square_feet=square_feet,
                                          no_of_rooms=rooms, latitude=latitude, longitude=longitude)
        return HttpResponse("<script>alert('Updated');window.location='/view_home#aa'</script>")


def delete_home(request,id):
    home.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted');window.location='/view_home#aa'</script>")

def view_home_and_send_request(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired! Please Login Again');window.location='/'</script>")

    data = home.objects.filter(~Q(USER__LOGIN=request.session['lid']),status='home',booking_status='free')
    print("dataaaaaaaaaa",data)


    for i in data:
        if requests.objects.filter(HOME=i.id,USER__LOGIN=request.session['lid']).exists():
            i.request_status = "1"
        else:
            i.request_status = "0"

    return render(request, "user/view_home_and_send_request.html",{"data":data})




def send_request(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "SEND REQUEST"
    obj = requests()
    obj.status = 'pending'
    obj.pay_date = 'pending'
    obj.pay_status = 'pending'
    obj.USER = user.objects.get(LOGIN=request.session['lid'])
    obj.HOME_id = id
    obj.date = datetime.datetime.now().date()
    obj.save()
    return HttpResponse("<script>alert('Requested');window.location='/view_home_and_send_request'</script>")


def view_request_and_verify(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VERIFY REQUEST"
    data = requests.objects.filter(~Q(USER__LOGIN=request.session['lid']),status='pending')
    return render(request,"user/view_request_and_verify.html",{"data":data})

def accept_request(request,id):
    requests.objects.filter(id=id).update(status='accept')
    home.objects.filter(id=id).update(booking_status='booked')
    return HttpResponse("<script>alert('Request Accepted');window.location='/view_request_and_verify'</script>")

def reject_request(request,id):
    requests.objects.filter(id=id).update(status='reject')
    return HttpResponse("<script>alert('Request Rejected');window.location='/view_request_and_verify'</script>")

def view_approved_request_owner(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW INQUIRY REQUEST"

    data = requests.objects.filter(HOME__USER__LOGIN=request.session['lid'])

    return render(request,"user/view_request_approved_owner.html",{"data":data})

def view_approved_request_user(request):

    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired! Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW OUTGOING REQUEST"

    data = requests.objects.filter(USER__LOGIN=request.session['lid'],pay_status='pending')

    return render(request, "user/view_approved_request_user.html", {"data": data})


def upload_document(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "UPLOAD DOCUMENT"
    return render(request,"user/upload_document.html",{"id":id})

def upload_document_post(request,id):
    doc = request.FILES['fileField']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\PycharmProjects\Rent_A_Home\myapp\static\document\\" + dt + '.pdf', doc)
    path = '/static/document/' + dt + '.pdf'
    data = document.objects.filter(documents=doc)
    if data.exists():
        return HttpResponse("<script>alert('Already Uploaded!!');window.location='/view_approved_request_owner'</script>")
    else:
        obj = document()
        obj.documents = path
        obj.date = datetime.datetime.now().date()
        obj.REQUESTS_id = id
        obj.save()
        return HttpResponse("<script>alert('Uploaded');window.location='/view_approved_request_owner'</script>")



def view_document(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW DOCUMENT"
    data = document.objects.filter(REQUESTS_id=id)
    return render(request,"user/view_document.html",{"data":data})

def send_complaint(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "SEND COMPLAINT"
    return render(request,"user/send_complaint.html")

def send_complaint_post(request):
    complaints = request.POST['textfield']
    obj = complaint()
    obj.complaint = complaints
    obj.date = datetime.datetime.now().date()
    obj.reply = 'pending'
    obj.reply_date = 'pending'
    obj.USER = user.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Success');window.location='/send_complaint'</script>")

def user_view_reply(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW REPLY"
    data = complaint.objects.filter(USER__LOGIN=request.session['lid'])
    return render(request,"user/view_reply.html",{"data":data})


# ================== MAKE PAYMENT ============================

def make_payment(request,id,amount):
    import razorpay


    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))
    # amount = 100
    amount = float(amount) * 100
    # amount = 100
    # amount = float(amount)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    # context = {
    #     'razorpay_api_key': razorpay_api_key,
    #     'amount': order_data['amount'],
    #     'currency': order_data['currency'],
    #     'order_id': order['id'],
    #     'rid': rid
    # }

    return render(request, 'User/UserPayProceed.html', {'razorpay_api_key': razorpay_api_key,
                                                        'amount': order_data['amount'],
                                                        'currency': order_data['currency'],
                                                        'order_id': order['id'],
                                                        'rid': id
                                                        })
    # return redirect('/view_approved_request_user')

def on_payment_success(request,id):
    dt = datetime.datetime.now().date()
    requests.objects.filter(id=id).update(pay_status='online',pay_date=dt)
    return HttpResponse("<script>alert('Success!');window.location='/view_approved_request_user'</script>")

# ========== Payment Report ====================

def view_payment(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW PAYMENT"
    return render(request,"user/view_payment.html")

def view_payment_post(request):
    month = request.POST['select']
    year = request.POST['select2']

    # Map month names to numbers
    month_mapping = {
        "January": "01", "Februvary": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "september": "09", "october": "10", "november": "11", "december": "12"
    }

    # Get the numerical value of the month
    month_number = month_mapping.get(month, "00")

    # Format the date for filtering
    formatted_date = f"{year}-{month_number}"
    # print(f"Formatted Date for Filtering: {formatted_date}")

    # Perform the aggregation
    res = requests.objects.filter(pay_date__startswith=formatted_date).aggregate(total_amount=Sum('HOME__amount'))
    # print(f"Aggregation Result: {res}")

    # Prepare the response data
    data = [{
        "total_amount": res.get('total_amount') or 0
    }]

    return render(request, "user/view_payment.html", {"data": data})