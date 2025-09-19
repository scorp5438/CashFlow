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
    class Meta(CreateCashFlowForm.Meta):
        fields = 'creation_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment'


class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class UpdateStatusForm(CreateStatusForm):
    class Meta(CreateStatusForm.Meta):
        pass


class CreateTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'


class UpdateTypeForm(CreateTypeForm):
    class Meta(CreateTypeForm.Meta):
        fields = 'type_name',


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class UpdateCategoryForm(CreateCategoryForm):
    class Meta(CreateCategoryForm.Meta):
        fields = 'category_name',


class CreateSubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'


class UpdateSubcategoryForm(CreateSubcategoryForm):
    class Meta(CreateSubcategoryForm.Meta):
        fields = 'subcategory_name',
