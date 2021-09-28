from django.shortcuts import render, redirect, reverse
from .models import Lead, Agent
from .forms import *
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorandLoginRequiredMixin


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse('login')


class HomeView(generic.TemplateView):
    template_name = "home.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)

            context.update({
                'unassigned_leads' : queryset,
            })
        return context



def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    return render(request, "lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead' : lead
    }
    return render(request, "lead_detail.html", context)
# Create your views here.


class LeadCreateView(OrganisorandLoginRequiredMixin, generic.CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("lead_list")

    def form_valid(self, form):
        send_mail(
            subject="A new Lead",
            message="The new lead is created please check the portal!",
            from_email='pandeyaman2485@gmail.com',
            recipient_list=['agent@gmail.com ']

        )
        return super(LeadCreateView, self).form_valid((form))


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    context = {
        'form':form
    }
    return render(request, "lead_create.html",context)


class LeadUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("lead_list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    context = {
        'form':form
    }
    return render(request, "lead_update.html",context)


class LeadDeleteView(OrganisorandLoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"

    def get_success_url(self):
        return reverse("lead_list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('lead_list')


class AssignAgentView(OrganisorandLoginRequiredMixin, generic.FormView):
    template_name = "agents/assign_agent.html"
    form_class = AssignAgentForm

    def get_success_url(self):
        return reverse("lead_list")

    def get_form_kwargs(self, **kwargs):
        kwargs=super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(
            id=self.kwargs['pk']
        )
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
        

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.userprofile)

        context['unassigned_lead_count']  = queryset.filter(category__isnull=True).count()

        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.userprofile)

        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     qs =self.get_object().leads.all()
    #
    #     context['leads'] = qs
    #
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.userprofile)

        return queryset


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "category_update.html"
    form_class = CategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse("category_detail", kwargs={'pk':self.get_object().id})


# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             lead.first_name = form.cleaned_data['first_name']
#             lead.last_name = form.cleaned_data['last_name']
#             lead.age = form.cleaned_data['age']
#             lead.agent = Agent.objects.first()
#             lead.save()
#             return redirect('lead_list')
#     context = {
#         'form': form,
#         'lead':lead
#     }
#     return render(request, "lead_update.html", context)
