#from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User 
from rest_framework import status
from django.http import Http404
from crud.serializer import ProductSerializer
from .models import Product

class ProductDetail(APIView):
    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        req_data = request.data
        serializer = ProductSerializer(data = req_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":" product added successfully"}, status= status.HTTP_200_OK)
        return Response ({"msg":" product data invalid"},status= status.HTTP_400_BAD_REQUEST)
    


class ProductInfo(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

    def put(self, request, id, format=None):
        req_data = request.data
        try:
            product = self.get_object(id)
        except Product.DoesNotExist:
            return Response({"msg":"product not found"} , status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(product, data=req_data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_200_OK)
        return Response({"msg":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, id, format=None):
        req_data = request.data
        try:
            product = self.get_object(id)
        except Product.DoesNotExist:
            return Response({"msg":"user not found"} , status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(product, data=req_data,partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_200_OK)
        return Response({"msg":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id,format=None):
        try:
            product = self.get_object(id)
        except Product.DoesNotExist:
            return Response({"msg":"user not found"} , status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response({"msg":"product deleted"} , status=status.HTTP_200_OK)
    





""" ////////////////////////////////////////////////////////////////////////////////// """
    

""" function based view """


""" ////////////////////////////////////////////////////////////////////////////////// """

""" 

@api_view(['GET', 'POST'])
def user_list(request):
    
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        User.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 """