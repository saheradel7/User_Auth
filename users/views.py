from rest_framework.views import APIView
from . serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt , datetime
from crud.models import Product, Order
from crud.serializer import OrderSerializer

class RegisterView(APIView ):
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 





class loginView (APIView):
    def post(self , request):
        email = request.data['email']
        password = request.data['password']

        user =User.objects.filter(email = email).first()
        if user is None:
            raise AuthenticationFailed('user not found !!')
        if not user.check_password(password):
               raise AuthenticationFailed('incorect password !!')
        
        
        
        payload={
             'id'  : user.id,
             'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes =60),
             'iat' : datetime.datetime.utcnow()
        }
        

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        responce = Response()
        responce.set_cookie(key='jwt', value= token , httponly=True)


        responce.data ={
             "jwt":token
        }
        return responce

class UserView(APIView):
    def get(self, request):
        token =request.COOKIES.get('jwt')
          
        if not token:
            raise AuthenticationFailed('UNauthorised')

        try:
            payload= jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UNauthorised')
            
        order = Order.objects.filter(user = payload['id']).all()
        serializer = OrderSerializer(order, many = True)
        return Response(serializer.data)
    
    def post(self , request):
        token =request.COOKIES.get('jwt')
          
        if not token:
            raise AuthenticationFailed('UNauthorised')

        try:
            payload= jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UNauthorised')
        
        req_data = request.data
        serializer = OrderSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            "message":"you loged out"
        }
        return response