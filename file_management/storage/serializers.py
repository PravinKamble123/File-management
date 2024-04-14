from rest_framework import serializers


from .models import File, Folder


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            'id',
            'name',
            'owner',
            'file',
            'folder',
            'created_at',
            'updated_at',
        ]

        read_only_fields = ['owner',]


class FolderSerializer(serializers.ModelSerializer):
    parent_folder = serializers.SerializerMethodField()
    files = FileSerializer(many=True, read_only=True)
    class Meta:
        model = Folder
        fields = [
            'id',
            'name',
            'owner',
            'parent_folder',
            'files',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'owner'
        ]

    def create(self, validated_data):
        data = self.context.get('request').data
        validated_data['parent_folder'] = data.get('parent_folder')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        data = self.context.get('request').data
        instance.parent_folder = data.get('parent_folder', instance.parent_folder)
        instance.name = data.get('name', instance.name)
        instance.save()
        return instance

    def get_parent_folder(self, instance):
        if instance.parent_folder:
            serializer = self.__class__(instance.parent_folder)
            return serializer.data
        return None
