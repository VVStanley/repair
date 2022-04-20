from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, FormView

from repairs.forms.customer import CustomerForm
from repairs.forms.master import MasterForm
from repairs.forms.tehnician import TechnicianForm
from repairs.forms.worker import WorkerForm
from repairs.models import Repair
from repairs.models.repair import Status
from users.models import Role


class ListRepairs(ListView):
    """Список заявок"""
    template_name = 'repairs.html'
    model = Repair
    paginate_by = 20

    def get_queryset(self):
        queyset = []
        # Клиент видит все свои заявки
        if self.request.user.role == Role.CUSTOMER:
            queyset = Repair.objects.filter(users=self.request.user)
        # Техник видит все заявки
        if self.request.user.role == Role.TECHNICIAN:
            queyset = Repair.objects.filter(status__in=[
                Status.RAW, Status.VERIFICATION
            ])
        # Мастер
        if self.request.user.role == Role.MASTER:
            queyset = Repair.objects.filter(status__in=[
                Status.CONFIRMED, Status.VERIFICATION, Status.TESTS
            ])
        # Слесарь
        if self.request.user.role == Role.WORKER:
            queyset = Repair.objects.filter(status__in=[
                Status.PROGRESS, Status.RE_REPAIR, Status.READY_TO_WORK
            ])
        return queyset


class CreateRepair(FormView):
    """Создание формы клиентом"""
    template_name = 'create_repair.html'
    form_class = CustomerForm
    success_url = '/repairs/'

    def form_valid(self, form):
        repair = form.save()
        repair.status = Status.RAW
        repair.save()
        repair.users.add(self.request.user)
        return super().form_valid(form)


class DetailRepair(View):
    template_customer = 'repair_detail/customer.html'
    template_technician = 'repair_detail/technician.html'
    template_master = 'repair_detail/master.html'
    template_worker = 'repair_detail/worker.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == Role.CUSTOMER:
            if request.method == "GET":
                return self.get_customer(request, *args, **kwargs)
            return self.method_not_allowed(request, *args, **kwargs)

        if request.user.role == Role.TECHNICIAN:
            if request.method == "GET":
                return self.get_technician(request, *args, **kwargs)
            else:
                return self.post_technician(request, *args, **kwargs)

        if request.user.role == Role.MASTER:
            if request.method == "GET":
                return self.get_master(request, *args, **kwargs)
            else:
                return self.post_master(request, *args, **kwargs)

        if self.request.user.role == Role.WORKER:
            if request.method == "GET":
                return self.get_worker(request, *args, **kwargs)
            else:
                return self.post_worker(request, *args, **kwargs)

        return self.method_not_allowed(request, *args, **kwargs)

    def method_not_allowed(self, request, *args, **kwargs):
        handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_customer(self, request, repair_id):
        """Клиент GET"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = CustomerForm(instance=repair)
        return render(request, self.template_customer, {
            'form': form,
            'repair': repair
        })

    def get_worker(self, request, repair_id):
        """Слесарь GET"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = WorkerForm(instance=repair)
        return render(request, self.template_worker, {
            'repair': repair,
            'form': form,
        })

    def post_worker(self, request, repair_id):
        """Слесарь POST"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = WorkerForm(request.POST, instance=repair)
        if form.is_valid():
            repair = form.save()
            repair.save()
            return redirect('repairs:list')
        context = {'form': form, 'repair': repair}
        return render(request, self.template_technician, context)

    def get_master(self, request, repair_id):
        """Мастер GET"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = MasterForm(instance=repair, initial={
            'users': repair.users.filter(role=Role.WORKER).first()
        })
        return render(request, self.template_master, {
            'form': form,
            'repair': repair
        })

    def post_master(self, request, repair_id):
        """Мастер POST"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = MasterForm(request.POST, instance=repair)
        if form.is_valid():
            users = form.cleaned_data.get('users')
            del form.cleaned_data['users']
            repair = form.save()
            repair.save()
            repair.users.add(users, request.user)
            return redirect('repairs:list')
        context = {'form': form, 'repair': repair}
        return render(request, self.template_master, context)

    def get_technician(self, request, repair_id):
        """Техник GET"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = TechnicianForm(instance=repair)
        return render(request, self.template_technician, {
            'form': form,
            'repair': repair
        })

    def post_technician(self, request, repair_id):
        """Техник POST"""
        repair = get_object_or_404(Repair, pk=repair_id)
        form = TechnicianForm(request.POST, instance=repair)
        if form.is_valid():
            repair = form.save()
            repair.save()
            repair.users.add(self.request.user)
            return redirect('repairs:list')
        context = {'form': form, 'repair': repair}
        return render(request, self.template_technician, context)
