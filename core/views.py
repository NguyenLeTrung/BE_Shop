from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializer import *
from .models import *
import datetime, jwt

# Create your views here.

def index(request):
    return HttpResponse("<h1> Hello World </h1>")

# ============================ USER API ======================================
class UserView():

    # Đăng ký thông tin tài khoản
    @api_view(['POST'])
    def register(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    

    # Đăng nhập thông tin tài khoản
    @api_view(['POST'])
    def login(request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        cursor = User.objects.raw("SELECT * FROM core_user u WHERE u.username = %s", [request.data["username"]])

        user = UserSerializer(cursor, many=True).data

        response.data = {
            'jwt': token,
            'user': user
        }

        return response

    # Đăng xuất thông tin tài khoản
    @api_view(['POST'])
    def logout(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
    
    # Tìm kiếm thông tin người dùng
    @api_view(['GET'])
    def search_user(self, request):
        params = request.GET 
        keyword = params.get('keyword', '')
        user_list = User.objects.filter(QuerySet(username__icontains=keyword) | QuerySet(email__icontains=keyword) | QuerySet(phone__icontains=keyword))
        serializer = UserSerializer(user_list, many=True)

        return Response(serializer.data)

    # Liệt kê danh sách người dùng
    @api_view(['GET'])
    def list_user(request):
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return Response({"Message": "List of User", "User List": serializer.data})
    

    # Liệt kê danh sách quản lý
    @api_view(['GET'])
    def list_user_manage(request):
        list_manage = User.objects.raw("SELECT u.* FROM core_user u JOIN core_user_role ur ON u.id = ur.user_id" +
                                        " JOIN core_role r ON ur.role_id = r.id WHERE r.role_name = 'ADMIN'")
        
        serializer = UserSerializer(list_manage, many=True)
        return Response(serializer.data)
    
    # Liệt kê danh sách khách hàng
    @api_view(['GET'])
    def list_user_customer(request):
        list_customer = User.objects.raw("SELECT u.* FROM core_user u JOIN core_user_role ur ON u.id = ur.user_id" +
                                        " JOIN core_role r ON ur.role_id = r.id WHERE r.role_name = 'CUSTOMER'")

        serializer = UserSerializer(list_customer, many=True)
        return Response(serializer.data)

    # Cập nhật thông tin người dùng
    @api_view(['PUT'])
    def update_user(request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "sucess", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})
    
    # Xóa thông tin người dùng
    @api_view(['DELETE'])
    def delete_user(request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.status = 0

            user.save()
            return Response({"Message": "Success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
    
# ===============================================================================



# ======================== SUPPLIER API =========================================
class SupplierView():
    # Tạo mới nhà cung cấp
    @api_view(['POST'])
    def create_supplier(request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
        
    
    # Lấy danh sách các nhà cung cấp
    @api_view(['GET'])
    def list_supplier(request):
        supplier_list = Supplier.objects.all()
        serializer = SupplierSerializer(supplier_list, many=True)
        return Response(serializer.data)

    # Tìm kiếm nhà cung cấp
    @api_view(['GET'])
    def search_supplier(request):
        params = request.GET
        keyword = params.get('keyword', '')
        supplier = Supplier.objects.filter(QuerySet(supplier_name__icontains=keyword) | QuerySet(phone__icontains=keyword))
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)

    # Cập nhật thông tin nhà cung cấp
    @api_view(['PUT'])
    def update_supplier(request, pk):
        supplier = Supplier.objects.get(pk=pk)
        serializer = SupplierSerializer(supplier, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        else: 
            return Response({"Message": "error", "Error": serializer.errors})
    
    # Xóa thông tin nhà cung cấp
    @api_view(['DELETE'])
    def delete_supplier(request, pk):
        try:
            supplier = Supplier.objects.get(pk=pk)
            supplier.delete()

            return Response({"Message": "sucesss"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================

# ================================ CATEGORY API =================================
class CategoryView():
    # Tạo mới danh mục 
    @api_view(['POST'])
    def create_category(request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
    
    # Hiển thị danh sách các danh mục 
    @api_view(['GET'])
    def list_category(request):
        list_category = Category.objects.all()
        serializer = CategorySerializer(list_category, many=True)

        return Response(serializer.data)
    
    # Tìm kiếm danh mục
    @api_view(['GET'])
    def search_category(request):
        params = request.GET
        keyword = params.get('keyword', '')
        category = Category.objects.filter(QuerySet(category_name__icontains=keyword))
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    # Lấy danh sách danh mục theo id
    @api_view(['GET'])
    def get_category_by_id(request, pk):
        list_category = Category.objects.raw("SELECT * FROM core_category WHERE id = %s", [pk])
        serializer = CategorySerializer(list_category, many=True)

        return Response(serializer.data)
    
    # Cập nhật thông tin danh mục 
    @api_view(['PUT'])
    def update_category(request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Data": serializer.errors})
    
    # Xóa thông tin danh mục
    @api_view(['DELETE'])
    def delete_category(request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({"Message": "success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================


# ================================== API BRANCH =================================
class BranchView():
    # Tạo mới thương hiệu
    @api_view(['POST'])
    def create_branch(request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=404)
    
    # Hiển thị danh sách các nhãn hiệu
    @api_view(['GET'])
    def list_branch(request):
        branch_list = Branch.objects.all()
        serializer = BranchSerializer(branch_list, many=True)

        return Response(serializer.data)
    
    # Cập nhật thông tin nhãn hàng
    @api_view(['PUT'])
    def update_branch(request, pk):
        branch = Branch.objects.get(pk=pk)
        serializer = BranchSerializer(branch, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})
    

    # Xóa danh sách các nhãn hàng
    @api_view(['DELETE'])
    def delete_branch(request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
            branch.delete()

            return Response({"Message": "sucess"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================