from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, BadRequest, ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from api.serializers import EmployeeSerializer, InventorySerializer
from api.models import Customer, Employee, Inventory, Role, Permission, Property, PropertyAssignment

def startup():
    # create web users using employee information
    def create_users():
        for eo in Employee.objects.all():
            User.objects.get_or_create(username=eo.name, password=eo.name, first_name=eo.name)

    # assign tokens to users for api token authentication
    def assign_tokens():
        for uo in User.objects.all():
            Token.objects.get_or_create(user=uo)

    create_users()
    assign_tokens()

startup()


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username, password=password)

            # login creates a sessionid to keep track of the current user's session
            login(request, user)
            token = Token.objects.get(user=user)

            response = Response({
                'message': 'Sign in successful',
                'user': user.first_name,
            }, status=status.HTTP_200_OK)

            # authentication token in cookie for backup
            response.set_cookie('auth-token', token)
            return response
        except PermissionDenied:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

  
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request) # clear session cookie
            response = Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
            response.delete_cookie('auth-token')
            response.delete_cookie('csrftoken')
            return response
        except BadRequest:
            return Response({'error': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class InventoryView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        def check_authorization():
            try:
                emp = Employee.objects.get(name=request.user)
                perms = emp.permission.all().values_list('permission', flat=True)
            except ObjectDoesNotExist:
                return Response({'error': 'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            if 'View' not in perms:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
        check_authorization()
        
        inv = Inventory.objects.all()
        serializer = InventorySerializer(inv, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        def check_authorization():
            try:
                emp = Employee.objects.get(name=request.user)
                perms = emp.permission.all().values_list('permission', flat=True)
            except ObjectDoesNotExist:
                return Response({'error': 'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
            if 'Update' not in perms:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)    
        
        check_authorization()        

        quantity = request.data.get('quantity')
        if quantity < 0:
            return Response({'error': 'Quantity Cannot Be Negative'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        def assign_paint_status():
            # paint status cutoff values.
            # Anything quantity higher than the cutoffs is assigned the status on right
            quantity_status = [
                (50, Inventory.StatusType.AVAILABLE),
                (0, Inventory.StatusType.LOW),
            ]
            # order matters so we will sort 
            quantity_status.sort(key=lambda x: x[0], reverse=True)

            # update paint status based on the quantity added by a manager
            stock = Inventory.StatusType.EMPTY
            for q, s in quantity_status:
                if quantity > q:
                    stock = s
                    break
            return stock
        
        paint_status = assign_paint_status()
        paint = Inventory.objects.filter(pk=pk) # must use .filter so we can use .update
        paint.update(quantity=quantity, status=paint_status)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)
    

class UserView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        self.check_authorization(request.user)
        
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=2):
        self.check_authorization(request.user)

        # format accepted by the serializer
        # request.data['role'] = [1, 2, 3]
        # request.data['permission'] = [1, 2, 3]

        total_permissions = Permission.objects.all()
        total_roles = Role.objects.all()
        if len(request.data['role']) > total_roles or \
           len(request.data['permission']) > total_permissions:
            return Response({'error': 'Too many roles or pemissions'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            employee = Employee.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # update using serializer so we can avoid naming all the fields
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'error': 'Employee failed to update'}, status=status.HTTP_501_NOT_IMPLEMENTED)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)

    def check_authorization(self, user):
        try:
            emp = Employee.objects.get(name=user)
            perms = emp.permission.all().values_list('permission', flat=True)
        except ObjectDoesNotExist:
            return Response({'error': 'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)            
        if 'Admin' not in perms:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)