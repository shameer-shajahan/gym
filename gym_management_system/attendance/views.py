from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Attendance
from .serializers import AttendanceSerializer
from batches.models import Batch, BatchMember
from trainers.models import TrainerProfile
from datetime import date

class IsAdminOrTrainerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trainer']

class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTrainerUser]
    
    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        # Filter by date
        attendance_date = self.request.query_params.get('date')
        if attendance_date:
            queryset = queryset.filter(date=attendance_date)
        
        # Filter by user
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by batch
        batch_id = self.request.query_params.get('batch')
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        
        # If trainer, only show attendances for their batches
        if self.request.user.role == 'trainer':
            try:
                trainer_profile = TrainerProfile.objects.get(user=self.request.user)
                batch_ids = Batch.objects.filter(trainer=trainer_profile).values_list('id', flat=True)
                queryset = queryset.filter(batch_id__in=batch_ids)
            except TrainerProfile.DoesNotExist:
                return Attendance.objects.none()
        
        return queryset

class AttendanceDetailView(generics.RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTrainerUser]
    
    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        # If trainer, only show attendances for their batches
        if self.request.user.role == 'trainer':
            try:
                trainer_profile = TrainerProfile.objects.get(user=self.request.user)
                batch_ids = Batch.objects.filter(trainer=trainer_profile).values_list('id', flat=True)
                queryset = queryset.filter(batch_id__in=batch_ids)
            except TrainerProfile.DoesNotExist:
                return Attendance.objects.none()
        
        return queryset

class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTrainerUser]
    
    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)

class AttendanceUpdateView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTrainerUser]
    
    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        # If trainer, only allow updating attendances for their batches
        if self.request.user.role == 'trainer':
            try:
                trainer_profile = TrainerProfile.objects.get(user=self.request.user)
                batch_ids = Batch.objects.filter(trainer=trainer_profile).values_list('id', flat=True)
                queryset = queryset.filter(batch_id__in=batch_ids)
            except TrainerProfile.DoesNotExist:
                return Attendance.objects.none()
        
        return queryset
    
    def perform_update(self, serializer):
        serializer.save(marked_by=self.request.user)

class UserAttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # If user is a regular user, only show their own attendance
        if user.role == 'user':
            return Attendance.objects.filter(user=user)
        
        # If admin, show all attendances
        elif user.role == 'admin':
            user_id = self.request.query_params.get('user')
            if user_id:
                return Attendance.objects.filter(user_id=user_id)
            return Attendance.objects.all()
        
        # If trainer, show attendances for their batches
        elif user.role == 'trainer':
            try:
                trainer_profile = TrainerProfile.objects.get(user=user)
                batch_ids = Batch.objects.filter(trainer=trainer_profile).values_list('id', flat=True)
                
                user_id = self.request.query_params.get('user')
                if user_id:
                    return Attendance.objects.filter(batch_id__in=batch_ids, user_id=user_id)
                return Attendance.objects.filter(batch_id__in=batch_ids)
            except TrainerProfile.DoesNotExist:
                return Attendance.objects.none()
        
        return Attendance.objects.none()

class BatchAttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTrainerUser]
    
    def get_queryset(self):
        batch_id = self.kwargs.get('batch_id')
        attendance_date = self.request.query_params.get('date', date.today())
        
        # If trainer, only show attendances for their batches
        if self.request.user.role == 'trainer':
            try:
                trainer_profile = TrainerProfile.objects.get(user=self.request.user)
                is_trainer_batch = Batch.objects.filter(id=batch_id, trainer=trainer_profile).exists()
                if not is_trainer_batch:
                    return Attendance.objects.none()
            except TrainerProfile.DoesNotExist:
                return Attendance.objects.none()
        
        return Attendance.objects.filter(batch_id=batch_id, date=attendance_date)

class MarkAttendanceView(APIView):
    permission_classes = [IsAdminOrTrainerUser]
    
    def post(self, request):
        batch_id = request.data.get('batch')
        attendance_date = request.data.get('date', date.today())
        attendance_data = request.data.get('attendance', [])
        
        if not batch_id:
            return Response(
                {"error": "Batch ID is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the batch exists and the trainer has access to it
        try:
            batch = Batch.objects.get(id=batch_id)
            
            if request.user.role == 'trainer':
                try:
                    trainer_profile = TrainerProfile.objects.get(user=request.user)
                    if batch.trainer != trainer_profile:
                        return Response(
                            {"error": "You don't have permission to mark attendance for this batch"}, 
                            status=status.HTTP_403_FORBIDDEN
                        )
                except TrainerProfile.DoesNotExist:
                    return Response(
                        {"error": "Trainer profile not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all members of the batch
        batch_members = BatchMember.objects.filter(batch_id=batch_id)
        
        # Process attendance data
        results = []
        for attendance_item in attendance_data:
            user_id = attendance_item.get('user')
            status_value = attendance_item.get('status')
            remarks = attendance_item.get('remarks', '')
            
            # Check if the user is a member of the batch
            is_member = batch_members.filter(user_id=user_id).exists()
            if not is_member:
                results.append({
                    "user": user_id,
                    "status": "error",
                    "message": "User is not a member of this batch"
                })
                continue
            
            # Create or update attendance record
            attendance, created = Attendance.objects.update_or_create(
                user_id=user_id,
                batch_id=batch_id,
                date=attendance_date,
                defaults={
                    'status': status_value,
                    'remarks': remarks,
                    'marked_by': request.user
                }
            )
            
            results.append({
                "user": user_id,
                "status": "created" if created else "updated",
                "attendance_id": attendance.id
            })
        
        return Response(results)