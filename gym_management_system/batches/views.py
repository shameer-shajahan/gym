from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Batch, BatchMember
from .serializers import BatchSerializer, BatchMemberSerializer
from trainers.models import TrainerProfile

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsTrainerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trainer'

class BatchListView(generics.ListAPIView):
    queryset = Batch.objects.filter(is_active=True)
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

class BatchDetailView(generics.RetrieveAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

class BatchCreateView(generics.CreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [IsAdminUser]

class BatchUpdateView(generics.UpdateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [IsAdminUser]

class BatchDeleteView(generics.DestroyAPIView):
    queryset = Batch.objects.all()
    permission_classes = [IsAdminUser]

class BatchMemberListView(generics.ListAPIView):
    queryset = BatchMember.objects.all()
    serializer_class = BatchMemberSerializer
    permission_classes = [IsAdminUser | IsTrainerUser]
    
    def get_queryset(self):
        queryset = BatchMember.objects.all()
        batch_id = self.request.query_params.get('batch_id')
        
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
            
        if self.request.user.role == 'trainer':
            try:
                trainer_profile = TrainerProfile.objects.get(user=self.request.user)
                queryset = queryset.filter(batch__trainer=trainer_profile)
            except TrainerProfile.DoesNotExist:
                return BatchMember.objects.none()
                
        return queryset

class BatchMemberCreateView(generics.CreateAPIView):
    queryset = BatchMember.objects.all()
    serializer_class = BatchMemberSerializer
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        batch_id = request.data.get('batch')
        user_id = request.data.get('user')
        
        try:
            batch = Batch.objects.get(id=batch_id)
            if batch.is_full:
                return Response(
                    {"error": "This batch is already full"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        return super().create(request, *args, **kwargs)

class BatchMemberDeleteView(generics.DestroyAPIView):
    queryset = BatchMember.objects.all()
    permission_classes = [IsAdminUser]

class TrainerBatchListView(APIView):
    permission_classes = [IsTrainerUser]
    
    def get(self, request):
        try:
            trainer_profile = TrainerProfile.objects.get(user=request.user)
            batches = Batch.objects.filter(trainer=trainer_profile, is_active=True)
            serializer = BatchSerializer(batches, many=True)
            return Response(serializer.data)
        except TrainerProfile.DoesNotExist:
            return Response(
                {"error": "Trainer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UserBatchListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'user':
            return Response(
                {"error": "Only regular users can access their batches"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        batch_memberships = BatchMember.objects.filter(user=request.user)
        batches = [membership.batch for membership in batch_memberships]
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data)