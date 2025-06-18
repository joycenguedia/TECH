from rest_framework import serializers
from .models import Club, Project, Submission

class ClubSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'code', 'created_by', 'created_by_name', 'is_creator', 'created_at']
        extra_kwargs = {'created_by': {'read_only': True}}

    def get_is_creator(self, obj):
        request = self.context.get('request')
        return request.user == obj.created_by

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by', 'club']

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'project', 'student', 'student_name', 'file', 'submitted_at', 'feedback']
        read_only_fields = ['student', 'submitted_at']
    
        def validate_file(self, value):
            # Example: Limit file size to 5MB
            max_size = 5 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError('File size must be less than 5MB')
            # Add more validations as needed (file type, etc.)
            return value