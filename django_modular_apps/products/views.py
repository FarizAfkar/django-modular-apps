import base64
import mimetypes
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from accounts.models import Product, Module
from products.forms import ProductForm
from django.conf import settings

# Create your views here.
def validate_uploaded_file(uploaded_file):
    """
    Validate the uploaded file for size and type.

    - Checks if the file size is within the allowed limit.
    - Ensures the file type is allowed.

    Raises ValidationError if invalid.
    """
    # Error Flag
    error_size = False
    error_type = False

    # Check file size
    if uploaded_file.size > settings.MAX_FILE_SIZE:
        error_size = True

    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    if not mime_type:
        mime_type = 'application/octet-stream'  # Default for unknown files

    # Validate file type (allow only certain types)
    allowed_types = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_FILE_TYPES
    if mime_type not in allowed_types:
        error_type = True

    context = {
        'error_size': error_size,
        'error_type': error_type,
        'mime_type': mime_type,
    }

    return context

def file_to_base64(uploaded_file):
    """
    Convert an uploaded file (image or any file) to Base64 with MIME type.
    """
    # Detect MIME type (e.g., image/png, application/pdf)
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    if not mime_type:
        mime_type = 'application/octet-stream'  # Default for unknown files

    # Read the file's binary content
    file_content = uploaded_file.read()

    # Encode the content to Base64
    base64_encoded = base64.urlsafe_b64encode(file_content).decode('utf-8').rstrip('=')

    # Format Base64 data as a Data URL (for embedding in HTML if needed)
    data_url = f'data:{mime_type};base64,{base64_encoded}'

    return {
        'filename': uploaded_file.name,
        'mime_type': mime_type,
        'base64': base64_encoded,
        'data_url': data_url,  # Useful for embedding in HTML
    }

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
    error_file = False
    if listproduct.count() == 0:
        product_none = 'Sorry, At this moment you don\'t have any Data Product'

    # Set Module Form
    form = ProductForm(request.POST)
    extra_fields = module.extra_fields

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
        file_request = request.FILES

        # Validate Add Prod
        if form.is_valid() and data_request['btn_action'] == 'add_product':

            # Check File
            for key, value in file_request.items():
                validate_file = validate_uploaded_file(request, value)
                if validate_file['error_size']:
                    error_file = True
                    messages.error(request, f'File size exceeds {settings.MAX_FILE_SIZE / 1024 / 1024:.2f}MB limit.')
                if validate_file['error_type']:
                    error_file = True
                    messages.error(request, f"Invalid file type: ({validate_file['mime_type']})")

            # Check Product
            if validate_prod(module.id_module, data_request['name'], data_request['barcode']) and not error_file:
                # Add Product Basic
                product = Product.objects.create(
                            module_id_id = module.id_module,
                            name = form.cleaned_data['name'],
                            barcode = form.cleaned_data['barcode'],
                            price = form.cleaned_data['price'],
                            stock = form.cleaned_data['stock'],
                            created_by = request.user.email
                        )

                # Add Product Extra Data
                for key, value in data_request.items():
                    if 'extra_' in key:

                        # Set part
                        parts = key.split('_')
                        field_number = parts[1]
                        field_type = parts[2]
                        field_name = parts[3]

                        result = {
                            'name' : field_name,
                            'type' : field_type,
                            'value' : value
                        }

                        # Save to DB
                        product.extra_fields[field_number] = result
                        product.save()

                # Add Product Extra File
                for key, value in file_request.items():
                    if 'extra_' in key:

                        # Set part
                        parts = key.split('_')
                        field_number = parts[1]
                        field_type = parts[2]
                        field_name = parts[3]
                        base64_data = file_to_base64(value)

                        # Formated Json
                        result = {
                            'name' : field_name,
                            'type' : field_type,
                            'value' : base64_data
                        }

                        # Save to DB
                        product.extra_fields[field_number] = result
                        product.save()

                messages.info(request, f'New Product has been added.')
                return redirect('products:home', name=name)

            else:
                if not error_file:
                    error_message = 'Product Barcode and Name must be Unique'

    # Render Context to HTML
    context = {
        'module' : name,
        'formproduct' : ProductForm,
        'extra_fields' : extra_fields,
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
        'extra_field': populated_data.extra_fields,
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
    info_message = ''
    error_file = False

    # Request Post
    if request.method == 'POST':

        # Get Data Request
        data_request = request.POST
        file_request = request.FILES
        form = ProductForm(request.POST)

        # Validate Update Prod
        if form.is_valid() and data_request['btn_action'] == 'update_product':

            # Check File
            for key, value in file_request.items():
                validate_file = validate_uploaded_file(request, value)
                if validate_file['error_size']:
                    error_file = True
                    messages.error(request, f'File size exceeds {settings.MAX_FILE_SIZE / 1024 / 1024:.2f}MB limit.')
                if validate_file['error_type']:
                    error_file = True
                    messages.error(request, f"Invalid file type: ({validate_file['mime_type']})")

            # Extra Data
            if not error_file:
                # Add Product Extra Data
                for key, value in data_request.items():
                    if 'extra_' in key:

                        # Set part
                        parts = key.split('_')
                        field_number = parts[1]
                        field_type = parts[2]
                        field_name = parts[3]

                        result = {
                            'name' : field_name,
                            'type' : field_type,
                            'value' : value
                        }

                        # Save to DB
                        if field_type != 'file':
                            populated_data.extra_fields[field_number] = result
                            populated_data.save()

                # Add Product Extra File
                for key, value in file_request.items():
                    if 'extra_' in key:

                        # Set part
                        parts = key.split('_')
                        field_number = parts[1]
                        field_type = parts[2]
                        field_name = parts[3]
                        base64_data = file_to_base64(value)

                        # Formated Json
                        result = {
                            'name' : field_name,
                            'type' : field_type,
                            'value' : base64_data
                        }

                        # Save to DB
                        populated_data.extra_fields[field_number] = result
                        populated_data.save()

                info_message = 'Your minor changes have been saved'
                messages.info(request, info_message)

            # Validate Major Data
            change_name = populated_data.name != form.cleaned_data['name']
            change_barcode = populated_data.barcode != form.cleaned_data['barcode']
            change_price = int(populated_data.price) != int(form.cleaned_data['price'])
            change_stock = populated_data.stock != form.cleaned_data['stock']

            # Check Major Update
            if not (change_name or change_barcode or change_price or change_stock):
                info_message = 'No Major data was changed'
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
                info_message = 'Your major changes have been saved'
                messages.info(request, info_message)
                return redirect('products:update', name=name, barcode=form.cleaned_data['barcode'])

    # Render Context to HTML
    context = {
        'module' : name,
        'details' : details,
        'extra_field': populated_data.extra_fields,
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
