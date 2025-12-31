from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View

from BottleBucksApp.serializer import *
from BottleBucksApp.forms import *
from BottleBucksApp.models import *

# Create your views here.


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self,request):
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        try:
            obj = LoginTable.objects.get(Username=username,Password=password)
            request.session['user_id']=obj.id
            if obj.UserType=='admin':
                return HttpResponse('''<script>alert("Login successful");window.location='HomePage'</script>''')
            else:
                return HttpResponse('''<script>alert("Login successful");window.location='home'</script>''')
        except LoginTable.DoesNotExist:
                return HttpResponse('''<script>alert("Login successful");window.location='home'</script>''')


    
class RegisterPage(View):
    def get(self, request):
       c = UserTable.object.all() 
       return render(request, 'register.html',{'c':c})
     


class RewardsPage(View):
    def get(self, request):
       c = RewardTable.object.all() 
       return render(request, 'rewards.html',{})

class UsergiftPage(View):
     def get(self, request):
        return render(request, 'user gift.html')

class UserPage(View):
     def get(self, request):
        u=UserTable.objects.all()
        return render(request, 'approve.html', {'obj': u})
     
class ApproveUser(View):
    def get(self,request,login_id):
        obj=LoginTable.objects.get(id=login_id)
        print(obj,'?????????')
        obj.UserType="user"
        obj.save()
        return HttpResponse('''<script>alert("Successfully Approved");window.location="/UserPage";</script>''')
        
class RejectUser(View):
    def get(self,request,login_id):
        obj=LoginTable.objects.get(id=login_id)
        print(obj,'?????????')
        obj.UserType="rejected"
        obj.save()
        return HttpResponse('''<script>alert("Successfully Rejected");window.location="/UserPage";</script>''')

class ApprovedUsersPage(View):
     def get(self, request):
        c=UserTable.objects.filter(LOGINID__UserType='user')
        return render(request, 'approved users.html', {'c':c})

class HomePage(View):
     def get(self, request):
        return render(request, 'home.html')
     
class NotificationPage(View):
     def get(self, request):
        return render(request, 'notification.html')

class ViewgiftPage(View):
    def get(self,request):
       gift= GiftTable.objects.all
       return render(request,'view gift.html',{'hh':gift})
    
class AddgiftPage(View):
    def get(self,request):
        return render(request,'add gift.html')
    def post(self,request):
        c =Giftform (request.POST,request.FILES)
        if c.is_valid():
            g = c.save()
            d = NotificationTable.objects.create(Description=f"New Product Added {g.ProductName}")
            return redirect('/ViewgiftPage')
        
class DeleteProduct(View):
    def get(self,request, id):
        c=GiftTable.objects.get(id=id)
        c.delete()
        return redirect('/ViewgiftPage')
    
class EditGift(View):
    def get(self,request,id):
        c=GiftTable.objects.get(id=id)
        return render(request,'editgift.html',{'c':c})
    def post(self,request,id):
        c=GiftTable.objects.get(id=id)
        d =Giftform (request.POST,request.FILES, instance=c)
        if d.is_valid():
            d.save()
            return redirect('/ViewgiftPage')
    
######################################################3API############################


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

import qrcode
import json
from io import BytesIO
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserReg_api(APIView):
    def post(self, request):
        print("#####################", request.data)

        user_serial = UserSerializer(data=request.data)
        login_serial = LoginSerializer(data=request.data)

        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            # Save login
            login_profile = login_serial.save(UserType='pending')

            user = user_serial.save(LOGINID=login_profile)

            qr_data = {
                "id":user.id,
                "Name": user.Name,
                "Email": user.Email,
                "Phone": user.Phno,
                "Address": user.Address,
                "District": user.District,
                "Pin": user.Pin,
                "Points": user.point,
            }

            qr_json = json.dumps(qr_data, ensure_ascii=False)

            qr_img = qrcode.make(qr_json)

            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")

            file_name = f"user_{user.id}_qr.png"

            user.qr.save(file_name, File(buffer), save=True)

            return Response(user_serial.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                'login_error': login_serial.errors if not login_valid else None,
                'user_error': user_serial.errors if not data_valid else None
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    
class LoginPageAPI(APIView):
        def post(self,request):
            print("###################", request.data)
            response_dict={}

            username=request.data.get("Username")
            password=request.data.get("Password")
            print("$$$$$$$$$$$$$$$",username)

            if not username or not password:
                response_dict["message"]="failed"
                return Response(response_dict,status=HTTP_400_BAD_REQUEST)
            
            user=LoginTable.objects.filter(Username=username, Password=password).first()
            print("%%%%%%%%%%%%",user)

            if not user:
                response_dict["message"]="failed"
                return Response(response_dict,status=HTTP_401_UNAUTHORIZED)
            else:
                response_dict["message"]="success"
                response_dict["login_id"]=user.id
                response_dict["usertype"]=user.UserType
                # print(response_dict['login_id'])
                # print(response_dict['usertype'])


                return Response(response_dict,status=HTTP_200_OK)
            

class ProductAPI(APIView):
    def get(self,request):
        c=GiftTable.objects.all()
        ser=GiftSerializer(c, many=True)
        return Response(ser.data, status=HTTP_200_OK)
    
class Kyc(APIView):
    def get(self, request, id):
        accounts = AccountTable.objects.filter(USERID__LOGINID=id)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
 


    def delete(self, request, id):
       
            account = AccountTable.objects.get(id=id)
            account.delete()
            return Response(
                {"message": "Account deleted successfully"},
                status=HTTP_200_OK
            )
      
                    
    def post(self, request, id):
        print("++++++==========", request.data)

        # ✅ get UserTable OBJECT (not id)
        user = UserTable.objects.get(LOGINID__id=id)

        count = AccountTable.objects.filter(USERID=user).count()
        if count >= 3:
            return Response(
                {'message': "Three KYC already Exist"},
                status=HTTP_401_UNAUTHORIZED
            )

        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(USERID=user)   # ✅ pass object
            return Response(serializer.data, status=HTTP_200_OK)

        print(serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



class RedeemGift(APIView):
    def post(self, request, id, gift_id):
        try:
            print("Redeem request: user =", id, "gift =", gift_id)
            print('===========================', request.data)
            address = request.data.get('address')

            user = UserTable.objects.get(LOGINID__id=id)
            gift = GiftTable.objects.get(id=gift_id)

            # Validate points
            if user.point is None or gift.PointsEligible is None:
                return Response({"message": "Invalid points data"}, status=400)

            if user.point < gift.PointsEligible:
                return Response(
                    {"message": "Not enough points to redeem this gift."},
                    status=400
                )

            # Validate quantity
            if gift.Quantity is None:
                return Response(
                    {"message": "Gift has no quantity set."},
                    status=400
                )

            if gift.Quantity <= 0:
                return Response(
                    {"message": "Gift out of stock."},
                    status=400
                )

            # Deduct user points
            user.point -= gift.PointsEligible
            user.save()

            # Deduct gift quantity
            gift.Quantity -= 1
            gift.save()

            # Create claim record
            ClaimProduct.objects.create(
                USERID=user,
                PRODUCTID=gift,
                totalRewardSpend=gift.PointsEligible,
                Address=address
            )

            NotificationTable.objects.create(
                Description= f"{gift.ProductName} redeemed Successfully",
                USER_ID=user
            )

            return Response({
                "message": "Gift redeemed successfully!",
                "gift": gift.ProductName,
                "points_spent": gift.PointsEligible,
                "remaining_points": user.point
            }, status=200)

        except UserTable.DoesNotExist:
            return Response({"message": "User not found."}, status=404)

        except GiftTable.DoesNotExist:
            return Response({"message": "Gift not found."}, status=404)

        except Exception as e:
            print("ERROR:", str(e))
            return Response(
                {"message": f"An error occurred: {str(e)}"},
                status=500
            )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreditPointsAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        account_id = request.data.get("account_id")
        points = request.data.get("points")

        print("REQUEST:", request.data)

        # Basic presence check
        if not all([user_id, account_id, points]):
            return Response({"error": "Missing fields: user_id, account_id and points are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Allowed redemption amounts (exact)
        allowed_points = {10, 100, 1000}

        try:
            points = int(points)
        except (ValueError, TypeError):
            return Response({"error": "Invalid points value"}, status=status.HTTP_400_BAD_REQUEST)

        if points not in allowed_points:
            return Response({"error": "Invalid redemption amount. Allowed: 10, 100, 1000 points."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserTable.objects.get(LOGINID__id=user_id)
        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            account = AccountTable.objects.get(id=account_id, USERID=user)
        except AccountTable.DoesNotExist:
            return Response({"error": "Account not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure user points numeric
        user_point_value = user.point if (user.point is not None) else 0

        if user_point_value < points:
            return Response({"error": "Insufficient points"}, status=status.HTTP_400_BAD_REQUEST)

        # Compute money (10 points => 1 rupee)
        redeemmoney = points // 10  # 10->1, 100->10, 1000->100

        try:
            # Create claim record
            ClaimPointAccount.objects.create(
                USERID=user,
                AccountId=account,
                points=points,
                redeemmoney=redeemmoney
            )

            # Deduct points from user
            user.point = user_point_value - points
            user.save()

            return Response({
                "message": "Points redeemed successfully",
                "points_redeemed": points,
                "redeem_amount": redeemmoney,
                "remaining_points": user.point
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 

class ProfileView(APIView):
    def get(self, request, id):
        c= AccountTable.objects.filter(USERID__LOGINID__id = id)
        print(c)
        ser = ProfileAccountSer(c, many=True)
        print(ser.data)
        return Response(ser.data, status=HTTP_200_OK)
    

class RedeemHistoryAPI(APIView):
    def get(self,request,id):
        c= ClaimProduct.objects.filter(USERID__LOGINID__id = id)
        ser=ClaimProductser(c,many=True)
        return Response(ser.data,status=HTTP_200_OK)
    
class BucksHistoryAPI(APIView):
    def get(self,request,id):
        c=ClaimPointAccount.objects.filter(USERID__LOGINID__id = id)
        ser=ClaimPointAccountser(c,many=True)
        return Response(ser.data,status=HTTP_200_OK)
    

class ProfileViewAPI(APIView):
    def get(self,request,id):
        c=UserTable.objects.filter(LOGINID__id=id)
        serializers=ProfileSerializer(c,many=True)
        print(serializers.data)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def put(self,request,id):
        print("-----------data--------",request.data)
        try:
            User=UserTable.objects.get(LOGINID__id=id)
        except UserTable.DoesNotExist:
            return Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        serializers=UserSerializer(User,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'Profile update successfully','data':serializers.data},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
class NotificationApi(APIView):
    def get(self, request):
        c=NotificationTable.objects.all()
        serializer=NotificationSerializer(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class UserNotificationApi(APIView):
    def get(self, request, id):
        c=NotificationTable.objects.filter(USER_ID__LOGINID__id = id)
        serializer=NotificationSerializer(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class TransactionHistoryAPI(APIView):
    def get(self,request,id):
        c=ClaimPointAccount.objects.filter(USERID__LOGINID__id = id)
        ser=ClaimPointAccountser(c,many=True)
        return Response(ser.data,status=HTTP_200_OK)
    

import cv2
import json
import requests
from pyzbar.pyzbar import decode
from django.http import JsonResponse
from .models import UserTable

ESP_URL = "http://192.168.137.75/open"
DEFAULT_POINTS = 100


def scan_qr_and_open_bin(request):
    cap = cv2.VideoCapture(0)
    qr_raw_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for qr in decode(frame):
            qr_raw_data = qr.data.decode("utf-8")
            break

        cv2.imshow("Scan QR Code", frame)

        if qr_raw_data:
            break

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

    if not qr_raw_data:
        return JsonResponse({"status": "failed", "message": "QR not detected"})

    try:
        # ---- PARSE JSON FROM QR ----
        qr_data = json.loads(qr_raw_data)

        user_id = qr_data.get("id")
        if not user_id:
            return JsonResponse({"status": "failed", "message": "Invalid QR data"})

        # ---- FETCH USER ----
        user = UserTable.objects.get(id=user_id)

        # ---- ADD POINTS ----
        user.point = (user.point or 0) + DEFAULT_POINTS
        user.save()

        # ---- OPEN BIN ----
        requests.get(ESP_URL, timeout=3)

        return JsonResponse({
            "status": "success",
            "user": user.Name,
            "points_added": DEFAULT_POINTS,
            "total_points": user.point
        })

    except UserTable.DoesNotExist:
        return JsonResponse({"status": "failed", "message": "User not found"})

    except json.JSONDecodeError:
        return JsonResponse({"status": "failed", "message": "QR is not valid JSON"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
