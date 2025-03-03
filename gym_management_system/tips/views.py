from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tip, TipCategory
from .serializers import TipSerializer, TipCategorySerializer
from experts.models import ExpertProfile

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsExpertUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'expert'

class TipListView(generics.ListAPIView):
    queryset = Tip.objects.filter(is_active=True)
    serializer_class = TipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Tip.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        expert = self.request.query_params.get('expert')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if expert:
            queryset = queryset.filter(expert_id=expert)
            
        return queryset

class TipDetailView(generics.RetrieveAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [permissions.IsAuthenticated]

class TipCreateView(generics.CreateAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def perform_create(self, serializer):
        if self.request.user.role == 'expert':
            try:
                expert_profile = ExpertProfile.objects.get(user=self.request.user)
                serializer.save(expert=expert_profile)
            except ExpertProfile.DoesNotExist:
                raise serializers.ValidationError("Expert profile not found")
        else:
            serializer.save()

class TipUpdateView(generics.UpdateAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'expert':
            try:
                expert_profile = ExpertProfile.objects.get(user=request.user)
                return obj.expert == expert_profile
            except ExpertProfile.DoesNotExist:
                return False
        return False

class TipDeleteView(generics.DestroyAPIView):
    queryset = Tip.objects.all()
    permission_classes = [IsAdminUser | IsExpertUser]
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'expert':
            try:
                expert_profile = ExpertProfile.objects.get(user=request.user)
                return obj.expert == expert_profile
            except ExpertProfile.DoesNotExist:
                return False
        return False

class TipCategoryListView(generics.ListAPIView):
    queryset = TipCategory.objects.all()
    serializer_class = TipCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TipCategoryDetailView(generics.RetrieveAPIView):
    queryset = TipCategory.objects.all()
    serializer_class = TipCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TipCategoryCreateView(generics.CreateAPIView):
    queryset = TipCategory.objects.all()
    serializer_class = TipCategorySerializer
    permission_classes = [IsAdminUser]

class ExpertTipListView(APIView):
    permission_classes = [IsExpertUser]
    
    def get(self, request):
        try:
            expert_profile = ExpertProfile.objects.get(user=request.user)
            tips = Tip.objects.filter(expert=expert_profile)
            serializer = TipSerializer(tips, many=True)
            return Response(serializer.data)
        except ExpertProfile.DoesNotExist:
            return Response(
                {"error": "Expert profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )