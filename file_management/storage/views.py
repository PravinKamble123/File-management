from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes

from storage.models import Folder

from .models import File
from .serializers import (
    FileSerializer,
    FolderSerializer,
)


"""
============================================ File ===========================================================
"""

@api_view(['POST'])
def upload_file(request):
    try:
        file = request.FILES['file']
        request.data['file'] = file

        if request.data.get('folder_id'):
            request.data['folder'] = Folder.objects.get(pk=request.data.get('folder_id'), owner=request.user).pk
        else:
            folder_id = request.user.folders.get(name='Root').id
            request.data['folder'] = folder_id

        serializer = FileSerializer(data=request.data ,context={'files': request.FILES})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data, status=201)
    except Folder.DoesNotExist:
        return Response({'message': "Folder not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_file(request, pk):
    try:
        _file = File.objects.get(pk=pk)
        if request.FILES:
            request.data['file'] = request.FILES['file']
        
        if request.data.get('folder_id'):
            request.data['folder'] = Folder.objects.get(pk=request.data.get('folder_id'), owner=request.user).pk
        else:
            request.data['folder'] = _file.folder.pk
        
        serializer = FileSerializer(_file, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Updated Successfully", 'data': serializer.data}, status=200)
    except File.DoesNotExist:
        return Response({'message': "File not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def my_files(request):
    try:
        files = File.objects.filter(owner=request.user)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def file_detail(request, pk):
    try:
        _file = File.objects.get(pk=pk, owner=request.user)
        return Response(FileSerializer(_file).data, status=200)
    except File.DoesNotExist:
        return Response({'message': "File not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_file(request, pk):
    try:
        _file = File.objects.get(pk=pk, owner=request.user)
        _file.delete()
        return Response({'message': "File deleted successfully"}, status=200)
    except File.DoesNotExist:
        return Response({'message': "File not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
========================================= Folders =========================================================
"""

@api_view(['POST'])
def create_folder(request):
    try:
        if request.data.get('parent_folder_id'):
            request.data['parent_folder'] = Folder.objects.get(pk=request.data.get('parent_folder_id'), owner=request.user)
        else:
            request.data['parent_folder'] = request.user.folders.get(name='Root')
        serializer = FolderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data, status=201)
    except Folder.DoesNotExist:
        return Response({'message': "Folder not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def edit_folder(request, pk):
    try:
        folder = Folder.objects.get(pk=pk)
        
        if request.data.get('parent_folder_id'):
            request.data['parent_folder'] = Folder.objects.get(pk=request.data.get('parent_folder_id'), owner=request.user)
        else:
            request.data['parent_folder'] = folder.parent_folder
        
        request.data['name'] = request.data.get('name', folder.name)
        
        serializer = FolderSerializer(folder, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Updated Successfully", 'data': serializer.data}, status=200)
    except Folder.DoesNotExist:
        return Response({'message': "File not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def my_folders(request):
    try:
        folders = Folder.objects.filter(owner=request.user)
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def folder_detail(request, pk):
    try:
        folder = Folder.objects.get(pk=pk, owner=request.user)
        return Response(FolderSerializer(folder).data, status=200)
    except Folder.DoesNotExist:
        return Response({'message': "Folder not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_folder(request, pk):
    try:
        folder = Folder.objects.get(pk=pk, owner=request.user)
        folder.delete()
        return Response({'message': "Folder deleted successfully"}, status=200)
    except Folder.DoesNotExist:
        return Response({'message': "Folder not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)