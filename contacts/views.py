from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,  RetrieveDestroyAPIView
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import permissions

# Create your views here.
#creating and listing
class ContactList(ListCreateAPIView):
    serializer_class =ContactSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
    

#deleting, updating
class ContactDetailView(RetrieveDestroyAPIView):
    serializer_class =ContactSerializer
    permission_classes=(permissions.IsAuthenticated,)

    look_field = 'id'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
   

   
