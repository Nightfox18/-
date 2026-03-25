from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Transaction, Status, Type, Category, Subcategory
from .forms import TransactionForm

def transaction_list(request):
    transactions = Transaction.objects.select_related('status', 'type', 'category', 'subcategory').all()
    
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if status_id:
        transactions = transactions.filter(status_id=status_id)
    if type_id:
        transactions = transactions.filter(type_id=type_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if subcategory_id:
        transactions = transactions.filter(subcategory_id=subcategory_id)
    
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    context = {
        'transactions': page_obj,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'status': status_id,
            'type': type_id,
            'category': category_id,
            'subcategory': subcategory_id,
        }
    }
    return render(request, 'transactions/transaction_list.html', context)

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана.')
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form, 'title': 'Создание записи'})

def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/transaction_form.html', {'form': form, 'title': 'Редактирование записи'})

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Запись удалена.')
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})

def directory_list(request, model_name):
    models = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory,
    }
    model = models.get(model_name)
    if not model:
        return redirect('transaction_list')
    items = model.objects.all()
    context = {
        'items': items,
        'model_name': model_name,
        'verbose_name': model._meta.verbose_name,
        'verbose_name_plural': model._meta.verbose_name_plural,
    }
    return render(request, 'transactions/directory_list.html', context)

def directory_create(request, model_name):
    models = {
        'status': (Status, ['name']),
        'type': (Type, ['name']),
        'category': (Category, ['name', 'type']),
        'subcategory': (Subcategory, ['name', 'category']),
    }
    if model_name not in models:
        return redirect('transaction_list')
    model, fields = models[model_name]
    if request.method == 'POST':
        data = {}
        for field in fields:
            data[field] = request.POST.get(field)
        try:
            obj = model.objects.create(**data)
            messages.success(request, f'{model._meta.verbose_name} успешно создан.')
            return redirect('directory_list', model_name=model_name)
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
    context = {
        'model_name': model_name,
        'verbose_name': model._meta.verbose_name,
        'fields': fields,
        'types': Type.objects.all() if model_name == 'category' else None,
        'categories': Category.objects.all() if model_name == 'subcategory' else None,
    }
    return render(request, 'transactions/directory_form.html', context)

def directory_edit(request, model_name, pk):
    models = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory,
    }
    if model_name not in models:
        return redirect('transaction_list')
    model = models[model_name]
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        for field in obj._meta.fields:
            if field.name in ['id', 'created_at', 'updated_at']:
                continue
            setattr(obj, field.name, request.POST.get(field.name))
        try:
            obj.save()
            messages.success(request, f'{model._meta.verbose_name} успешно обновлен.')
            return redirect('directory_list', model_name=model_name)
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
    context = {
        'model_name': model_name,
        'verbose_name': model._meta.verbose_name,
        'obj': obj,
        'types': Type.objects.all() if model_name == 'category' else None,
        'categories': Category.objects.all() if model_name == 'subcategory' else None,
    }
    return render(request, 'transactions/directory_form.html', context)

def directory_delete(request, model_name, pk):
    models = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory,
    }
    if model_name not in models:
        return redirect('transaction_list')
    model = models[model_name]
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, f'{model._meta.verbose_name} удален.')
        except Exception as e:
            messages.error(request, f'Не удалось удалить: {str(e)}')
        return redirect('directory_list', model_name=model_name)
    return render(request, 'transactions/directory_confirm_delete.html', {'obj': obj, 'model_name': model_name})

def api_categories(request):
    type_id = request.GET.get('type')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    else:
        categories = []
    return JsonResponse(list(categories), safe=False)

def api_subcategories(request):
    category_id = request.GET.get('category')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    else:
        subcategories = []
    return JsonResponse(list(subcategories), safe=False)