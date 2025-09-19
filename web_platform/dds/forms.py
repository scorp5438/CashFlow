from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Status,
    Type,
    Category,
    Subcategory,
    CashFlow
)


class CreateCashFlowForm(forms.ModelForm):
    """
    Форма для создания новой денежной операции в системе ДДС.

    Обеспечивает валидацию связей между связанными объектами и проверку
    бизнес-правил перед сохранением операции.

    Включает кастомную валидацию для:
    - Проверки существования связанных объектов (статус, тип, категория, подкатегория)
    - Проверки соответствия категории выбранному типу операции
    - Проверки соответствия подкатегории выбранной категории
    - Проверки положительности суммы операции
    """
    class Meta:
        model = CashFlow
        fields = 'status', 'type', 'category', 'subcategory', 'amount', 'comment'
        widgets = {
            'creation_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
        }

    def clean(self):
        """
        Выполняет комплексную валидацию данных формы.

        Проверяет:
        1. Существование всех выбранных связанных объектов в базе данных
        2. Логическую корректность связей:
           - Категория должна принадлежать выбранному типу
           - Подкатегория должна принадлежать выбранной категории
        3. Бизнес-правила: сумма операции должна быть положительной

        Returns:
            dict: Валидированные данные формы

        Raises:
            ValidationError: При нарушении любого из правил валидации
        """
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        type_obj = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        amount = cleaned_data.get('amount')

        if status and not Status.objects.filter(id=status.id).exists():
            raise ValidationError({'status': 'Выберите существующий статус'})

        if type_obj and not Type.objects.filter(id=type_obj.id).exists():
            raise ValidationError({'type': 'Выбранный тип не существует'})

        if category and not Category.objects.filter(id=category.id).exists():
            raise ValidationError({'category': 'Выбранная категория не существует'})

        if subcategory and not Subcategory.objects.filter(id=subcategory.id).exists():
            raise ValidationError({'subcategory': 'Выбранная подкатегория не существует'})

        if type_obj and category and category.type != type_obj:
            raise ValidationError({
                'category': f'Категория "{category}" не принадлежит типу "{type_obj}"'
            })

        if category and subcategory and subcategory.category != category:
            raise ValidationError({
                'subcategory': f'Подкатегория "{subcategory}" не принадлежит категории "{category}"'
            })

        if amount and amount < 0:
            raise ValidationError({
                'amount': f'Сумма должна быть положительной: {amount}'
            })

        return cleaned_data

class UpdateCashFlowForm(CreateCashFlowForm):
    """
    Форма для редактирования существующей денежной операции в системе ДДС.

    Наследует всю валидацию и функциональность от CreateCashFlowForm.
    Добавляет поле даты создания (creation_date) для возможности редактирования
    даты операции при обновлении.

    Используется в представлениях редактирования операций для обеспечения
    консистентности валидации между созданием и обновлением операций.
    """
    class Meta(CreateCashFlowForm.Meta):
        fields = 'creation_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment'


class CreateStatusForm(forms.ModelForm):
    """
    Форма для создания нового статуса операции в системе ДДС.

    Предоставляет поле для ввода названия статуса операции.
    Используется при добавлении новых статусов через пользовательский интерфейс.
    """
    class Meta:
        model = Status
        fields = '__all__'


class UpdateStatusForm(CreateStatusForm):
    """
    Форма для редактирования существующего статуса операции.

    Наследует всю функциональность от CreateStatusForm.
    Обеспечивает консистентность между формами создания и редактирования.
    Используется при изменении названия существующего статуса.
    """
    class Meta(CreateStatusForm.Meta):
        pass


class CreateTypeForm(forms.ModelForm):
    """
    Форма для создания нового типа операции в системе ДДС.

    Предоставляет поле для ввода названия типа операции.
    Используется при добавлении новых типов через пользовательский интерфейс.
    Включает все поля модели для максимальной гибкости при создании.
    """
    class Meta:
        model = Type
        fields = '__all__'


class UpdateTypeForm(CreateTypeForm):
    """
    Форма для редактирования существующего типа операции.

    Наследует базовую функциональность от CreateTypeForm, но ограничивает
    доступные поля только названием типа (type_name). Это предотвращает
    случайное изменение других атрибутов типа операции при редактировании.

    Обеспечивает безопасное обновление только разрешенных полей.
    """
    class Meta(CreateTypeForm.Meta):
        fields = 'type_name',


class CreateCategoryForm(forms.ModelForm):
    """
    Форма для создания новой категории операции в системе ДДС.

    Предоставляет поля для выбора типа операции и ввода названия категории.
    Используется при добавлении новых категорий через пользовательский интерфейс.
    Включает все поля модели для обеспечения полноты данных при создании.
    """
    class Meta:
        model = Category
        fields = '__all__'


class UpdateCategoryForm(CreateCategoryForm):
    """
    Форма для редактирования существующей категории операции.

    Наследует базовую функциональность от CreateCategoryForm, но ограничивает
    доступные поля только названием категории (category_name). Это предотвращает
    случайное изменение типа операции при редактировании категории.

    Обеспечивает безопасное обновление только разрешенных полей, сохраняя
    целостность связей между типами и категориями.
    """
    class Meta(CreateCategoryForm.Meta):
        fields = 'category_name',


class CreateSubcategoryForm(forms.ModelForm):
    """
    Форма для создания новой подкатегории операции в системе ДДС.

    Предоставляет поля для выбора категории и ввода названия подкатегории.
    Используется при добавлении новых подкатегорий через пользовательский интерфейс.
    Включает все поля модели для обеспечения корректных связей при создании.
    """
    class Meta:
        model = Subcategory
        fields = '__all__'


class UpdateSubcategoryForm(CreateSubcategoryForm):
    """
    Форма для редактирования существующей подкатегории операции.

    Наследует базовую функциональность от CreateSubcategoryForm, но ограничивает
    доступные поля только названием подкатегории (subcategory_name). Это предотвращает
    случайное изменение родительской категории при редактировании подкатегории.

    Обеспечивает безопасное обновление только разрешенных полей, сохраняя
    целостность иерархии категорий и подкатегорий.
    """
    class Meta(CreateSubcategoryForm.Meta):
        fields = 'subcategory_name',
