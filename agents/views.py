from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import *
from django.shortcuts import reverse
from .forms import *
from django.core.mail import send_mail
from .mixins import OrganisorandLoginRequiredMixin
import random


class AgentListView(OrganisorandLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganisorandLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentCreateForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_organisor = False
        user.is_agent = True
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject="Invitation",
            message="The invitation to join the CRM of the company!!",
            from_email="admin@mail.com",
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('agent_list')


class AgentDetailView(generic.DetailView, OrganisorandLoginRequiredMixin):
    template_name = "agents/agent_detail.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentCreateForm

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse('agent_list')


class AgentDeleteView(OrganisorandLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse('agent_list')
