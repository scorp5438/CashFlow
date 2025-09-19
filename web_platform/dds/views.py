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
    """
    Представление для отображения главной страницы системы учета ДДС.

    Обеспечивает:
    - Отображение списка денежных операций с пагинацией
    - Фильтрацию операций по различным параметрам
    - Передачу в контекст справочников для фильтров

    Атрибуты:
        template_name (str): Путь к шаблону страницы
        paginate_by (int): Количество операций на странице

    Методы:
        get_queryset(): Возвращает отфильтрованный queryset операций
        get_context_data(): Добавляет в контекст данные для фильтров и формы

    Фильтрация поддерживается по:
        - Диапазону дат (date_from, date_to)
        - Статусу операции (status)
        - Типу операции (type_obj)
        - Категории (category)
        - Подкатегории (subcategory)

    Пример использования в URL:
        /?date_from=2024-01-01&date_to=2024-12-31&status=1&type_obj=2

    Возвращает:
        QuerySet: Отсортированный по дате (новые сначала) список операций
        с предзагруженными связанными объектами для оптимизации запросов.
    """
    template_name = 'dds/index.html'
    paginate_by = 5

    def get_queryset(self):
        """
        Формирует и возвращает отфильтрованный queryset денежных операций.

        Обрабатывает GET-параметры фильтрации:
            - date_from: начальная дата (включительно)
            - date_to: конечная дата (включительно)
            - status: ID статуса операции
            - type_obj: ID типа операции
            - category: ID категории
            - subcategory: ID подкатегории

        Returns:
            QuerySet: Отфильтрованный и отсортированный queryset операций CashFlow
                     с предзагрузкой связанных объектов для избежания N+1 проблемы.

        Note:
            Использует select_related для оптимизации запросов к связанным моделям.
            Фильтрация по ID выполняется только для цифровых значений.
        """
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
        """
        Расширяет контекст шаблона дополнительными данными.

        Добавляет в контекст:
            - Все справочники для заполнения фильтров
            - Текущие значения фильтров для сохранения состояния формы

        Args:
            object_list: Список объектов для отображения
            **kwargs: Дополнительные аргументы контекста

        Returns:
            dict: Контекст с данными для шаблона, включая:
                - object_list: Список операций
                - statuses: Все статусы операций
                - types: Все типы операций
                - categories: Все категории
                - subcategories: Все подкатегории
                - current_*: Текущие значения фильтров
        """
        context = super().get_context_data(**kwargs)

        # Справочники для фильтров
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        # Текущие значения фильтров для сохранения состояния формы
        context['current_date_from'] = self.request.GET.get('date_from', '')
        context['current_date_to'] = self.request.GET.get('date_to', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_type'] = self.request.GET.get('type_obj', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_subcategory'] = self.request.GET.get('subcategory', '')
        return context


class CreateDdsView(CreateView):
    """
    Представление для создания новой денежной операции.

    Обеспечивает отображение формы создания и обработку данных операции.
    После успешного создания перенаправляет на главную страницу.
    """
    model = CashFlow
    template_name = 'dds/create_dds.html'
    form_class = CreateCashFlowForm
    success_url = reverse_lazy('dds:index')


class UpdateDdsView(UpdateView):
    """
    Представление для редактирования существующей денежной операции.

    Обеспечивает отображение формы редактирования и обновление данных операции.
    После успешного обновления перенаправляет на главную страницу.
    """
    model = CashFlow
    template_name = 'dds/update_dds.html'
    form_class = UpdateCashFlowForm
    success_url = reverse_lazy('dds:index')


class DeleteDdsView(DeleteView):
    """
    Представление для удаления денежной операции.

    Обеспечивает подтверждение удаления и удаление операции из системы.
    После успешного удаления перенаправляет на главную страницу.
    """
    model = CashFlow
    template_name = 'dds/delete_dds.html'
    success_url = reverse_lazy('dds:index')


class BaseCreateView(CreateView):
    """
    Базовое представление для создания записей справочников.

    Наследуется от Django CreateView и предоставляет общую конфигурацию
    для всех форм создания справочных данных (статусов, типов, категорий и т.д.).

    Атрибуты:
        template_name: Общий шаблон для всех форм создания
        submit_button: Текст кнопки отправки формы
        back_url: URL для кнопки "Назад"
        title: Заголовок страницы

    Методы:
        get_context_data: Добавляет в контекст дополнительные данные для шаблона
    """
    template_name = 'dds/base_form.html'
    submit_button = 'Добавить'
    back_url = None
    title = None

    def get_context_data(self, **kwargs):
        """
        Расширяет контекст шаблона дополнительными данными.

        Добавляет:
            - title: Заголовок страницы
            - submit_button: Текст кнопки отправки
            - back_url: URL для кнопки "Назад"

        Returns:
            dict: Расширенный контекст для рендеринга шаблона
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['submit_button'] = self.submit_button
        context['back_url'] = self.back_url
        return context


class BaseUpdateView(UpdateView):
    """
    Базовое представление для редактирования записей справочников.

    Наследуется от Django UpdateView и предоставляет общую конфигурацию
    для всех форм редактирования справочных данных.

    Атрибуты:
        template_name: Общий шаблон для всех форм редактирования
        submit_button: Текст кнопки сохранения изменений
        back_url: URL для кнопки "Назад"
        title: Заголовок страницы

    Методы:
        get_context_data: Добавляет в контекст дополнительные данные для шаблона
    """
    template_name = 'dds/base_form.html'
    submit_button = 'Сохранить'
    back_url = None
    title = None

    def get_context_data(self, **kwargs):
        """
        Расширяет контекст шаблона дополнительными данными.

        Добавляет:
            - title: Заголовок страницы
            - submit_button: Текст кнопки сохранения
            - back_url: URL для кнопки "Назад"

        Returns:
            dict: Расширенный контекст для рендеринга шаблона
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['submit_button'] = self.submit_button
        context['back_url'] = self.back_url
        return context


class StatusesView(ListView):
    """
    Представление для отображения списка всех статусов операций.
    """
    template_name = 'dds/statuses.html'
    queryset = Status.objects.all()


class CreateStatusView(BaseCreateView):
    """
    Представление для создания нового статуса операции.
    Наследует базовую конфигурацию формы создания.
    """
    model = Status
    form_class = CreateStatusForm
    success_url = reverse_lazy('dds:statuses')
    title = 'Добавление статуса'
    back_url = reverse_lazy('dds:statuses')


class UpdateStatusView(BaseUpdateView):
    """
    Представление для редактирования существующего статуса операции.
    Наследует базовую конфигурацию формы редактирования.
    """
    model = Status
    form_class = UpdateStatusForm
    success_url = reverse_lazy('dds:statuses')
    title = 'Обновление статуса'
    back_url = reverse_lazy('dds:statuses')


class DeleteStatusView(DeleteView):
    """
    Представление для удаления статуса операции.
    Включает предзагрузку связанных операций для отображения предупреждения.
    """
    model = Status
    template_name = 'dds/delete_status.html'
    success_url = reverse_lazy('dds:statuses')
    queryset = Status.objects.prefetch_related('status_cash_flows')


class TypesView(ListView):
    """
    Представление для отображения списка всех типов операций.
    """
    template_name = 'dds/types.html'
    queryset = Type.objects.all()


class CreateTypeView(BaseCreateView):
    """
    Представление для создания нового типа операции.
    Наследует базовую конфигурацию формы создания.
    """
    model = Type
    form_class = CreateTypeForm
    success_url = reverse_lazy('dds:types')
    title = 'Добавление типа'
    back_url = reverse_lazy('dds:types')


class UpdateTypeView(BaseUpdateView):
    """
    Представление для редактирования существующего типа операции.
    Наследует базовую конфигурацию формы редактирования.
    """
    model = Type
    form_class = UpdateTypeForm
    success_url = reverse_lazy('dds:types')
    title = 'Обновление статуса'
    back_url = reverse_lazy('dds:types')


class DeleteTypeView(DeleteView):
    """
    Представление для удаления типа операции.
    Включает предзагрузку связанных категорий, подкатегорий и операций
    для отображения предупреждения о связанных данных.
    """
    model = Type
    template_name = 'dds/delete_type.html'
    success_url = reverse_lazy('dds:types')
    queryset = Type.objects.prefetch_related('categories__subcategories', 'type_cash_flows').all()

    def get_context_data(self, **kwargs):
        """
        Расширяет контекст списком всех подкатегорий, связанных с типом.
        """
        context = super().get_context_data(**kwargs)

        all_subcategories = []
        for category in self.object.categories.all():
            all_subcategories.extend(category.subcategories.all())
        context['all_subcategories'] = all_subcategories
        return context

class CategoriesView(ListView):
    """
    Представление для отображения списка всех категорий операций.
    Включает предзагрузку связанных типов для оптимизации запросов.
    """
    template_name = 'dds/categories.html'
    queryset = Category.objects.select_related('type').all()


class CreateCategoryView(BaseCreateView):
    """
    Представление для создания новой категории операции.
    Наследует базовую конфигурацию формы создания.
    """
    model = Category
    form_class = CreateCategoryForm
    success_url = reverse_lazy('dds:categories')
    title = 'Добавление категории'
    back_url = reverse_lazy('dds:categories')


class UpdateCategoryView(BaseUpdateView):
    """
    Представление для редактирования существующей категории операции.
    Наследует базовую конфигурацию формы редактирования.
    """
    model = Category
    form_class = UpdateCategoryForm
    success_url = reverse_lazy('dds:categories')
    title = 'Обновление категории'
    back_url = reverse_lazy('dds:categories')


class DeleteCategoryView(DeleteView):
    """
    Представление для удаления категории операции.
    Включает предзагрузку связанных операций и подкатегорий
    для отображения предупреждения о связанных данных.
    """
    model = Category
    template_name = 'dds/delete_category.html'
    success_url = reverse_lazy('dds:categories')
    queryset = Category.objects.prefetch_related('category_cash_flows', 'subcategories').all()

class SubcategoriesView(ListView):
    """
    Представление для отображения списка всех подкатегорий операций.
    Включает предзагрузку связанных категорий и их типов для оптимизации запросов.
    """
    template_name = 'dds/subcategories.html'
    queryset = Subcategory.objects.select_related('category__type').all()


class CreateSubcategoryView(BaseCreateView):
    """
    Представление для создания новой подкатегории операции.
    Наследует базовую конфигурацию формы создания.
    """
    model = Subcategory
    form_class = CreateSubcategoryForm
    success_url = reverse_lazy('dds:subcategories')
    title = 'Добавление подкатегории'
    back_url = reverse_lazy('dds:subcategories')


class UpdateSubcategoryView(BaseUpdateView):
    """
    Представление для редактирования существующей подкатегории операции.
    Наследует базовую конфигурацию формы редактирования.
    """
    model = Subcategory
    form_class = UpdateSubcategoryForm
    success_url = reverse_lazy('dds:subcategories')
    title = 'Обновление подкатегории'
    back_url = reverse_lazy('dds:subcategories')


class DeleteSubcategoryView(DeleteView):
    """
    Представление для удаления подкатегории операции.
    Включает предзагрузку связанных операций для отображения предупреждения.
    """
    model = Subcategory
    template_name = 'dds/delete_subcategory.html'
    success_url = reverse_lazy('dds:subcategories')
    queryset = Subcategory.objects.prefetch_related('subcategory_cash_flows')
