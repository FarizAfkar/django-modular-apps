from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from accounts.models import Product, Module
from products.forms import ProductForm

# Create your views here.
def validate_prod(module, name, barcode):
    data_prod = Product.objects.filter(module_id=module)
    if data_prod.count()==0:
        return True
    if not data_prod.filter(Q(name=name) | Q(barcode=barcode)).exists():
        return True
    return False

@login_required
@permission_required('accounts.view_product', raise_exception=True)
def home(request, name):
    # Get Module
    try:
        module = Module.objects.get(name=name)
        # Validate
        if module.installed == False:
            raise PermissionDenied()

    except Module.DoesNotExist:
        raise PermissionDenied()

    # Get Product Module
    listproduct = Product.objects.filter(module_id_id=module.id_module).order_by('created_at')

    # Set Module & error Message
    error_message = ''
    product_none = ''
    if listproduct.count() == 0:
        product_none = 'Sorry, At this moment you don\'t have any Data Product'

    # Set Module Form
    form = ProductForm(request.POST)

    # Get Search Param
    search_param= request.GET.get('search_param')
    if search_param:
        listproduct = listproduct.filter(Q(name__icontains=search_param)|
                                         Q(barcode__icontains=search_param))
        if listproduct.count() == 0:
            product_none = 'Sorry, please try another keyword'

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(listproduct, 10)

    try:
        listproduct = paginator.page(page)
    except PageNotAnInteger :
        listproduct = paginator.page(1)
    except EmptyPage:
        listproduct = paginator.page(paginator.num_pages)

    # Request Post
    if request.method == 'POST' and request.user.has_perm('accounts.add_product'):

        # Get Data Request
        data_request = request.POST

        # Validate Add Prod
        if form.is_valid() and data_request['btn_action'] == 'add_product':

            # Check Product
            if validate_prod(module.id_module, data_request['name'], data_request['barcode']):
                # Add Product
                Product.objects.create(
                    module_id_id = module.id_module,
                    name = form.cleaned_data['name'],
                    barcode = form.cleaned_data['barcode'],
                    price = form.cleaned_data['price'],
                    stock = form.cleaned_data['stock'],
                    created_by = request.user.email
                )
                messages.info(request, f'New Product has been added.')
                return redirect('products:home', name=name)

            else:
                error_message = 'Product Barcode and Name must be Unique'

    # Render Context to HTML
    context = {
        'module' : name,
        'formproduct' : ProductForm,
        'listproduct' : listproduct,
        'product_none' : product_none,
        'error_message' : error_message
    }

    return render(request, 'products/index.html', context)

@login_required
@permission_required('accounts.view_product', raise_exception=True)
def detail(request, name, barcode):
    # Get Detail Product
    try:
        module = Module.objects.get(name=name)
        populated_data = Product.objects.get(barcode=barcode, module_id=module.id_module)
        details = ProductForm(instance=populated_data)
    except Exception as e:
        print('Error : ', e)
        raise PermissionDenied

    # Render Context to HTML
    context = {
        'module' : name,
        'details' : details,
        'barcode' : populated_data.barcode
    }
    return render (request, 'products/detail.html', context)

@login_required
@permission_required('accounts.change_product', raise_exception=True)
def update(request, name, barcode):
    # Get Detail Product
    try:
        module = Module.objects.get(name=name)
        populated_data = Product.objects.get(barcode=barcode, module_id=module.id_module)
        details = ProductForm(instance=populated_data)
    except Exception as e:
        print('Error : ', e)
        raise PermissionDenied

    # Set Message
    error_message = ''
    info_message =''

    # Request Post
    if request.method == 'POST':

        # Get Data Request
        data_request = request.POST
        form = ProductForm(request.POST)

        # Validate Update Prod
        if form.is_valid() and data_request['btn_action'] == 'update_product':

            # Validate Data
            change_name = populated_data.name != form.cleaned_data['name']
            change_barcode = populated_data.barcode != form.cleaned_data['barcode']
            change_price = int(populated_data.price) != int(form.cleaned_data['price'])
            change_stock = populated_data.stock != form.cleaned_data['stock']

            # Check Update
            if not (change_name or change_barcode or change_price or change_stock):
                info_message = 'No data was changed'
                messages.info(request, info_message)
                return redirect('products:update', name=name, barcode=barcode)

            else:
                # Save To DB
                if change_name:
                    if not Product.objects.filter(name=form.cleaned_data['name'],
                                                  module_id=module.id_module).\
                        exclude(id_product=populated_data.id_product).exists():
                        populated_data.name = form.cleaned_data['name']
                    else:
                        error_message = 'Product Name must be Unique'
                        messages.error(request, error_message)
                        return redirect('products:update', name=name, barcode=barcode)

                if change_barcode:
                    if not Product.objects.filter(barcode=form.cleaned_data['barcode'],
                                                  module_id=module.id_module).\
                        exclude(id_product=populated_data.id_product):
                        populated_data.barcode = form.cleaned_data['barcode']
                    else:
                        error_message = 'Product Barcode must be Unique'
                        messages.error(request, error_message)
                        return redirect('products:update', name=name, barcode=barcode)

                if change_price:
                    populated_data.price = form.cleaned_data['price']
                if change_stock:
                    populated_data.stock = form.cleaned_data['stock']

                populated_data.updated_by = request.user.username
                populated_data.save()
                info_message = 'Your changes have been saved'
                messages.info(request, info_message)
                return redirect('products:update', name=name, barcode=form.cleaned_data['barcode'])

    # Render Context to HTML
    context = {
        'module' : name,
        'details' : details,
        'barcode' : populated_data.barcode,
        'error_message': error_message,
        'info_message' : info_message
    }
    return render (request, 'products/update.html', context)

@login_required
@permission_required('accounts.delete_product', raise_exception=True)
def delete(request, name, barcode):
    # Get Product
    try:
        module = Module.objects.get(name=name)
        Product.objects.get(barcode=barcode, module_id=module.id_module).delete()
    except Exception as e:
        print('Error : ', e)
        raise PermissionDenied

    return redirect('products:home', name=module.name)
