from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from accounts.models import Module, Product
from modules.forms import ModuleForm
from collections import defaultdict

# Create your views here.
def update_version(version):
    parts = version.split('.')
    x, y = int(parts[0]), int(parts[1]) + 1
    if y > 10:
        x += 1
        y = 0
    return f"{x}.{y}"

def check_fields(fields):
    filtered_values = [value for key, value in fields.items() if 'field-name-add-' in key]
    if '' in filtered_values:
        return True
    return False

@login_required
@permission_required('accounts.view_module', raise_exception=True)
def home(request):
    # Get Object Module
    listmodules = Module.objects.all().order_by('created_at')

    # Set Module & error Message
    error_message = ''
    module_none = ''
    if listmodules.count() == 0:
        module_none = 'Sorry, At this moment you don\'t have any Module Installed'

    # Set Module Form
    form = ModuleForm(request.POST)

    # Get Search Param
    search_param= request.GET.get('search_param')
    if search_param:
        listmodules = listmodules.filter(Q(name__icontains=search_param))
        if listmodules.count() == 0:
            module_none = 'Sorry, please try another keyword'

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(listmodules, 10)

    try:
        listmodules = paginator.page(page)
    except PageNotAnInteger :
        listmodules = paginator.page(1)
    except EmptyPage:
        listmodules = paginator.page(paginator.num_pages)

    # Request Post
    if request.method == 'POST' and request.user.has_perm('accounts.add_module'):

        # Get Data Request
        data_request = request.POST

        # Validate New Module
        if form.is_valid() and data_request['btn_action'] == 'install_module':

            # Check Module Name
            if not Module.objects.filter(name=data_request['module_name']).exists():
                # Create New Module
                Module.objects.create(
                    auth_user_id_id = request.user.id,
                    name = form.cleaned_data['module_name'],
                    installed = True,
                    version = '1.0',
                    created_by = request.user.username
                )
                messages.info(request, f'New module has been added.')
                return redirect('modules:home')

            else:
                error_message = 'Module Name must be Unique'

    # Render Context to HTML
    context = {
        'formsmodule' : ModuleForm,
        'listmodules' : listmodules,
        'module_none' : module_none,
        'error_message' : error_message
    }

    return render(request, 'modules/index.html', context)

@login_required
@permission_required('accounts.change_module', raise_exception=True)
def upgrade(request, name):
    # Get Object Module
    try:
        module = Module.objects.get(name=name)
    except Module.DoesNotExist:
        raise PermissionDenied()

    # Set Message
    error_message = ''
    info_message =''

    # Get Product Attribut
    details_product = Product._meta.get_fields()

    # Processing data into structured JSON format
    formatted_data = defaultdict(dict)

    # Request Post
    if request.method == 'POST':
        # Get Dictionary Post
        fields = request.POST

        # Validate Update Prod
        if not check_fields(fields) and fields['btn_action'] == 'upgrade_module':

            for key, value in fields.items():
                if 'field' in key:

                    parts = key.split('-')  # Splitting by '-'
                    field_number = parts[3]  # Extracting field number
                    field_attr = parts[1]  # Extracting attribute type (name/type)

                    formatted_data[f'field-{field_number}'][field_attr] = value

                    # Converting to standard dictionary
                    dict_extra_fields = dict(formatted_data)

            # Save To DB
            module.version = update_version(module.version)
            module.extra_fields = dict_extra_fields
            module.save()
            info_message = 'Upgrade Module Succees'
        else:
            info_message = 'No data was changed'

    context = {
        'name' : name,
        'details_module' : module.extra_fields,
        'details_product' : details_product,
        'error_message': error_message,
        'info_message' : info_message
    }

    return render(request, 'modules/upgrade.html', context)

@login_required
@permission_required('accounts.delete_module', raise_exception=True)
def uninstall(request, name):
    # Get Object Module
    try:
        module = Module.objects.get(name=name)
        # Validate
        if not module.installed == False:
            module.installed = False
            module.updated_by = request.user.username
            module.save()
            messages.info(request, f'Module has been uninstall.')
        else:
            raise PermissionDenied()
    except Module.DoesNotExist:
        raise PermissionDenied()

    return redirect('modules:home')
