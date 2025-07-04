from rest_framework import serializers
from .models import (
    Course, Enrollment, CustomUser, Assignment, AssignmentSubmission, Announcement, 
    Message, Module, Lesson, Notification, DiscussionThread, DiscussionPost, 
    Progress, Certificate, Category, Quiz, Question, QuestionOption, QuizAttempt, 
    QuizResponse, LessonProgress, Badge, UserBadge, Payment, CourseRating, 
    Wishlist, LearningPath
)
from django.contrib.auth import authenticate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'points', 'level', 'bio', 'avatar', 'date_of_birth', 'phone', 'address']
        read_only_fields = ['id', 'points', 'level']


class CourseSerializer(serializers.ModelSerializer):
    instructor = CustomUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    video_intro = serializers.SerializerMethodField()
    enrolled_students_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'short_description', 'thumbnail', 
            'instructor', 'category', 'difficulty', 'status', 'language', 'duration', 
            'total_lessons', 'rating', 'total_ratings', 'enrolled_students', 
            'enrolled_students_count', 'average_rating', 'price', 'original_price',
            'created_at', 'updated_at', 'is_featured', 'tags', 'requirements', 
            'learning_outcomes', 'video_intro'
        ]
        read_only_fields = ['id', 'instructor', 'created_at', 'updated_at', 'enrolled_students_count', 'average_rating']
    
    def get_thumbnail(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            url = obj.thumbnail.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_video_intro(self, obj):
        request = self.context.get('request')
        if obj.video_intro:
            if obj.video_intro.startswith('http'):
                return obj.video_intro
            if request is not None:
                return request.build_absolute_uri(obj.video_intro)
            return obj.video_intro
        return None

    def get_enrolled_students_count(self, obj):
        return obj.enrollments.count()
    
    def get_average_rating(self, obj):
        if obj.total_ratings > 0:
            return round(obj.rating, 1)
        return 0.0


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    student = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['id', 'enrolled_at', 'completed_at', 'last_accessed']


class ModuleSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ['id', 'lessons_count']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    video_url = serializers.SerializerMethodField()
    file_attachment = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video_url:
            if obj.video_url.startswith('http'):
                return obj.video_url
            if request is not None:
                return request.build_absolute_uri(obj.video_url)
            return obj.video_url
        return None

    def get_file_attachment(self, obj):
        request = self.context.get('request')
        if obj.file_attachment and hasattr(obj.file_attachment, 'url'):
            url = obj.file_attachment.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = '__all__'
        read_only_fields = ['id', 'completed_at', 'last_accessed']


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['id', 'questions_count']
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = '__all__'
        read_only_fields = ['id', 'started_at', 'completed_at']


class QuizResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_options = QuestionOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizResponse
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    submissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'submissions_count']
    
    def get_submissions_count(self, obj):
        return obj.submissions.count()


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    student = CustomUserSerializer(read_only=True)
    graded_by = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
        read_only_fields = ['id', 'submitted_at', 'graded_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']


class MessageSerializer(serializers.ModelSerializer):
    instructor = CustomUserSerializer(read_only=True)
    sender = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = '__all__'
        read_only_fields = ['id', 'earned_at']


class PaymentSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'payment_date']


class DiscussionThreadSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DiscussionThread
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'posts_count']
    
    def get_posts_count(self, obj):
        return obj.posts.count()


class DiscussionPostSerializer(serializers.ModelSerializer):
    thread = DiscussionThreadSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DiscussionPost
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count']
    
    def get_likes_count(self, obj):
        return obj.likes.count()


class ProgressSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ['id', 'last_accessed']


class CertificateSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Certificate
        fields = '__all__'
        read_only_fields = ['id', 'issued_at', 'file_url', 'certificate_id']


class CourseRatingSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseRating
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WishlistSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['id', 'added_at']


class LearningPathSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = LearningPath
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'role', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


# Legacy serializers for backward compatibility
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'points', 'level', 'bio', 'avatar', 'date_of_birth', 'phone', 'address']
        read_only_fields = ['id']


