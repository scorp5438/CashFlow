from django.urls import (
    reverse_lazy
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import (
    CreateCashFlowForm,
    UpdateCashFlowForm,
    CreateStatusForm,
    UpdateStatusForm,
    CreateTypeForm,
    CreateCategoryForm,
    CreateSubcategoryForm,
    UpdateTypeForm,
    UpdateCategoryForm,
    UpdateSubcategoryForm)
from .models import (
    CashFlow,
    Status,
    Type,
    Category,
    Subcategory,
)


class IndexView(ListView):
    template_name = 'dds/index.html'
    paginate_by = 5

    def get_queryset(self):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        type_obj = self.request.GET.get('type_obj')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')

        queryset = CashFlow.objects.select_related(
            'status',
            'type',
            'category',
            'subcategory',
        ).all()

        if date_from:
            queryset =queryset.filter(creation_date__gte=date_from)

        if date_to:
            queryset =queryset.filter(creation_date__lte=date_to)

        if status and status.isdigit():
            queryset = queryset.filter(status=int(status))

        if type_obj and type_obj.isdigit():
            queryset = queryset.filter(type=int(type_obj))

        if category and category.isdigit():
            queryset = queryset.filter(category=int(category))

        if subcategory and subcategory.isdigit():
            queryset = queryset.filter(subcategory=int(subcategory))

        return queryset.order_by('-creation_date')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        context['current_date_from'] = self.request.GET.get('date_from', '')
        context['current_date_to'] = self.request.GET.get('date_to', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_type'] = self.request.GET.get('type_obj', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_subcategory'] = self.request.GET.get('subcategory', '')
        return context


class CreateDdsView(CreateView):
    model = CashFlow
    template_name = 'dds/create_dds.html'
    form_class = CreateCashFlowForm
    success_url = reverse_lazy('dds:index')


class UpdateDdsView(UpdateView):
    model = CashFlow
    template_name = 'dds/update_dds.html'
    form_class = UpdateCashFlowForm
    success_url = reverse_lazy('dds:index')


class DeleteDdsView(DeleteView):
    model = CashFlow
    template_name = 'dds/delete_dds.html'
    success_url = reverse_lazy('dds:index')


class BaseCreateView(CreateView):
    template_name = 'dds/base_form.html'
    submit_button = 'Добавить'
    back_url = None
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['submit_button'] = self.submit_button
        context['back_url'] = self.back_url
        return context


class BaseUpdateView(UpdateView):
    template_name = 'dds/base_form.html'
    submit_button = 'Сохранить'
    back_url = None
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['submit_button'] = self.submit_button
        context['back_url'] = self.back_url
        return context


class StatusesView(ListView):
    template_name = 'dds/statuses.html'
    queryset = Status.objects.all()


class CreateStatusView(BaseCreateView):
    model = Status
    form_class = CreateStatusForm
    success_url = reverse_lazy('dds:statuses')
    title = 'Добавление статуса'
    back_url = reverse_lazy('dds:statuses')


class UpdateStatusView(BaseUpdateView):
    model = Status
    form_class = UpdateStatusForm
    success_url = reverse_lazy('dds:statuses')
    title = 'Обновление статуса'
    back_url = reverse_lazy('dds:statuses')


class DeleteStatusView(DeleteView):
    model = Status
    template_name = 'dds/delete_status.html'
    success_url = reverse_lazy('dds:statuses')
    queryset = Status.objects.prefetch_related('status_cash_flows')


class TypesView(ListView):
    template_name = 'dds/types.html'
    queryset = Type.objects.all()


class CreateTypeView(BaseCreateView):
    model = Type
    form_class = CreateTypeForm
    success_url = reverse_lazy('dds:types')
    title = 'Добавление типа'
    back_url = reverse_lazy('dds:types')


class UpdateTypeView(BaseUpdateView):
    model = Type
    form_class = UpdateTypeForm
    success_url = reverse_lazy('dds:types')
    title = 'Обновление статуса'
    back_url = reverse_lazy('dds:types')


class DeleteTypeView(DeleteView):
    model = Type
    template_name = 'dds/delete_type.html'
    success_url = reverse_lazy('dds:types')
    queryset = Type.objects.prefetch_related('categories__subcategories', 'type_cash_flows').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_subcategories = []
        for category in self.object.categories.all():
            all_subcategories.extend(category.subcategories.all())
        context['all_subcategories'] = all_subcategories
        return context

class CategoriesView(ListView):
    template_name = 'dds/categories.html'
    queryset = Category.objects.select_related('type').all()


class CreateCategoryView(BaseCreateView):
    model = Category
    form_class = CreateCategoryForm
    success_url = reverse_lazy('dds:categories')
    title = 'Добавление категории'
    back_url = reverse_lazy('dds:categories')


class UpdateCategoryView(BaseUpdateView):
    model = Category
    form_class = UpdateCategoryForm
    success_url = reverse_lazy('dds:categories')
    title = 'Обновление категории'
    back_url = reverse_lazy('dds:categories')


class DeleteCategoryView(DeleteView):
    model = Category
    template_name = 'dds/delete_category.html'
    success_url = reverse_lazy('dds:categories')
    queryset = Category.objects.prefetch_related('category_cash_flows', 'subcategories').all()

class SubcategoriesView(ListView):
    template_name = 'dds/subcategories.html'
    queryset = Subcategory.objects.select_related('category__type').all()
    back_url = reverse_lazy('dds:index')
    title = 'Список подкатегорий'


class CreateSubcategoryView(BaseCreateView):
    model = Subcategory
    form_class = CreateSubcategoryForm
    success_url = reverse_lazy('dds:subcategories')
    title = 'Добавление подкатегории'
    back_url = reverse_lazy('dds:subcategories')


class UpdateSubcategoryView(BaseUpdateView):
    model = Subcategory
    form_class = UpdateSubcategoryForm
    success_url = reverse_lazy('dds:subcategories')
    title = 'Обновление подкатегории'
    back_url = reverse_lazy('dds:subcategories')


class DeleteSubcategoryView(DeleteView):
    model = Subcategory
    template_name = 'dds/delete_subcategory.html'
    success_url = reverse_lazy('dds:subcategories')
    queryset = Subcategory.objects.prefetch_related('subcategory_cash_flows')
