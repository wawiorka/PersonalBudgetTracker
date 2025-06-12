from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Expense, ExpenseCategory
from .serializers import ExpenseCategorySerializer, ExpenseSerializer


# Create your views here.
class ExpenseCategoryView(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # user = self.request.user
    #     return ExpenseCategory.objects.all
    #
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def get_success_url(self):
    #     messages.success(self.request, 'Outcome created successfully!')
    #     return reverse_lazy('my_finances:outcome_list')

class ExpenseView(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer