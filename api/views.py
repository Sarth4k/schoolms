from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from subjects.models import Subject
from accounts.models import User, StudentProfile
from .serializers import SubjectSerializer, StudentProfileSerializer


# ── Subjects ──────────────────────────────────────
@api_view(['GET'])
def subjects_list(request):
    subjects = Subject.objects.prefetch_related('teachers__user').all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def subjects_detail(request, pk):
    subject = Subject.objects.get(id=pk)
    serializer = SubjectSerializer(subject)
    return Response(serializer.data)


@api_view(['DELETE'])
def subjects_delete(request, pk):
    subject = Subject.objects.get(id=pk)
    subject.delete()
    return Response({"message": "Subject deleted"}, status=status.HTTP_200_OK)


# ── Auth ──────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role,
        })
    return Response({'error': 'Wrong username or password'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)
    User.objects.create_user(username=username, password=password, role='student')
    return Response({"message": "User created successfully"}, status=201)


# ── Student Profile ───────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=404)
    serializer = StudentProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def student_profile_update(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=404)
    serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_admission_status(request):
    try:
        admission = request.user.studentprofile.admissionrequest
        return Response({
            'status': admission.status,
            'applied_at': admission.applied_at,
            'reason': admission.reason if admission.status == 'rejected' else None
        })
    except:
        return Response({'status': 'No admission request found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_enrolled_subjects(request):
    try:
        subjects = request.user.studentprofile.enrolled_subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    except:
        return Response({'error': 'Profile not found'}, status=404)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(
            {
                "error":"Username and password required"
            },
            status=400
        )
    if User.objects.filter(
        username=username
    ).exists():
        return Response(
            {
                "error":"Username already taken"
            },
            status=400
        )
    User.objects.create_user(
        username=username,
        password=password
    )
    return Response(
        {
            "message":"User created successfully"
        },
        status=201
    )




#login api
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(
        username=username,
        password=password
    )
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    return Response(
        {
            'error':'Wrong username or password'
        },
        status=status.HTTP_400_BAD_REQUEST
    )
   