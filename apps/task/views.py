#from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,GenericAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
# Create your views here.
from .serializers import TaskAPI,TaskSerializer
from .models import Task

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 12

    def get_paginated_response(self,data):
        print(dir(self.page.paginator.page))
        return Response({"total_pages":self.page.paginator.num_pages,
            "count":self.page.paginator.count,
            "links":{
                "previus":self.get_previous_link(),
                "next":self.get_next_link(),
            },
            "result":data
            })
        
#pagición standar         
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self,data):
        print(dir(self.page.paginator.page))
        return Response({"total_pages":self.page.paginator.num_pages,
            "count":self.page.paginator.count,
            "links":{
                "previus":self.get_previous_link(),
                "next":self.get_next_link(),
            },
            "result":data
            })


class TaskVIEW(ListCreateAPIView):
        queryset=Task.objects.all()
        serializer_class=TaskAPI
        #permission_classes=(IsAuthenticated,)
        #authentication_classes=(TokenAuthentication,)

#VIEW QUE RETORNA LAS TAREAS DE ACUERDO A EL ID DE EL USUARIO
class TaskA(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskAPI
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    pagination_class = StandardResultsSetPagination
    def get_queryset(self,request):
        return Task.objects.filter(created_by=request.user.id).order_by('date').reverse()

    def list(self, request):
        #print(request.query_params)
        #print(dir(request))
        #id=request.query_params.get('id')
        #token=Token.objects.get(user=request.user).key
        #self.headers.setdefault("Authorization",{"Token":token})
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.filter_queryset(self.get_queryset(request))
        paginate=self.paginate_queryset(queryset)
        serializer = TaskAPI(paginate, many=True)
        result=self.get_paginated_response(serializer.data)
        #print(paginate)
        #queryset=Task.objects.all()
        #print(dir(queryset))

        #print(self.paginator.num_pages)

        #print(dir(self.paginator.page))
        #print(dir(result.data))

        return Response(result.data)

#CREA LA TAREA 
class CreateTaskView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request):
        serializer=TaskAPI(data=request.data)
        serializer.is_valid(raise_exception=True)
        #print(request.data.get('title'))
        #data=serializer.validate
        #print(serializer.validate)

        #task=Task.objects.create(**data)
        serializer.save()

        return Response(serializer.data,status.HTTP_201_CREATED)

#VISTAS DONDE VAMOS A RECIBIR, LA ACTUALIZACIÓN Y UPDATE DE LAS TAREAS
class TaskView(viewsets.ModelViewSet):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

class TaskUncomplete(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    pagination_class = StandardResultsSetPagination

    def list(self,request):
        queryset=tasks=Task.objects.filter(created_by=self.request.user.id,completed=False)
        print(dir(self))
        paginate=self.paginate_queryset(queryset)
        serializer = TaskAPI(paginate, many=True)
        result=self.get_paginated_response(serializer.data)
        return Response(result.data)

class TaskComplete(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    pagination_class = StandardResultsSetPagination
    def list(self,request):
        queryset=tasks=Task.objects.filter(created_by=self.request.user.id,completed=True).order_by('-date')
        #print(dir(queryset))
        paginate=self.paginate_queryset(queryset)
        serializer = TaskAPI(paginate, many=True)
        result=self.get_paginated_response(serializer.data)
        return Response(result.data)

class TaskFavorite(ListAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    pagination_class = StandardResultsSetPagination
    def list(self,request):
        queryset=tasks=Task.objects.filter(created_by=self.request.user.id,favorite=True).order_by('-date')

        paginate=self.paginate_queryset(queryset)
        serializer = TaskAPI(paginate, many=True)
        result=self.get_paginated_response(serializer.data)
        return Response(result.data)