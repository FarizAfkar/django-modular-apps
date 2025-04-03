
# Django Modular App

A modular Django-based web application where modules can be installed, upgraded, and uninstalled dynamically.

## Table of content


- [Features](##Features)

- [Tech Stack](##TechStack)

- [Environment Variables](#EnvironmentVariables)

- [Installation](#Installation)

- [Usage/Examples](#Usage/Examples)

- [Screenshots](#Screenshots)

- [License](#License)


## Features

✅ Modular App Engine for handling modules dynamically

✅ Module Management Page to list, install, upgrade, and uninstall modules

✅ Product Management Page to list, install, update, and uninstall product

✅ Role-Based Access Control (RBAC)

✅ Field Modification Handling during upgrades


## Tech Stack

**Backend:** Django

**Database:** PostgreSQL

**Frontend:** HTML, CSS, Bootstrap


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```
SECRET_KEY='django-insecure-4oj=-3+uwc@+$hcvf41!0lrx0y%g9@dgd2a899j&e8t8pi%fm2'
DEBUG='True'
DB_NAME = modular
DB_USER = postgres
DB_PASSWORD = postgres
DB_HOST = localhost
DB_PORT = 5432
SUPER_USER = adminhash
SUPER_EMAIL = admin@hashmicro.com
SUPER_PASS = password2025
MANAGER_USER = manager
MANAGER_FRIST = manager
MANAGER_LAST = user
MANAGER_EMAIL = manager@hashmicro.com
MANAGER_PASS = password2025
USER_USER = user
USER_FRIST = user
USER_LAST = user
USER_EMAIL = user@hashmicro.com
USER_PASS = password2025
PUBLIC_USER = public
PUBLIC_FRIST = public
PUBLIC_LAST = user
PUBLIC_EMAIL = public@hashmicro.com
PUBLIC_PASS = password2025
```

## Installation

🔹 Prerequisites
Ensure you have the following installed:

Python (≥3.9)

PostgreSQL 17

Git


🔹 Clone the Repository
```bash
git clone https://github.com/FarizAfkar/django-modular-apps.git
cd django-modular-apps
```

🔹 Create a Virtual Environment
```bash
python -m venv env
Windows: venv\Scripts\activate
```

🔹 Install Dependencies
```bash
pip install -r requirements.txt
```

🔹 Apply Migrations
```bash
cd django_modular_apps
python manage.py migrate #Intial create user
python manage.py makemigrations #Update Models
python manage.py migrate #Apply Role-Based Access Control
```

🔹 Start the Development Server
```bash
python manage.py runserver
```

Now, open http://127.0.0.1:8000/ in your browser.


## Usage/Examples

🔹 Role-Based Access Control (RBAC)

    Login As:
    
    Manager → CRUD access

    User → CRU access

    Public → Read-only access

🔹 Install Module

    1. Go to http://127.0.0.1:8000/module/

    2. Click Install Module

    3. Fill Module name and Click Install

🔹 View Module

    1. Click View

    2. The landing page will now be available at http://127.0.0.1:8000/module/product/,<module_name>


🔹 Upgrade Module

    1. Click Upgrade

    2. The landing page will now be available at http://127.0.0.1:8000/module/upgrade/<module_name>

    3. Fill name and choose type field, you can Add and Remove the field up to 3 field then click Upgrade

    4. The system will automatically apply changes

🔹 Uninstall Module

    1. Click Uninstall

    2. The module selected will popout validation 'Are you sure to Uninstall this Module?' then click Yes

    3. The module and its landing page will be removed

🔹 Add Product
    
    1. Can be access from View Module

    2. click Add Product

    3. Fill the field and click Add

🔹 View Product

    1. Click View

    2. The landing page will now be available at http://127.0.0.1:8000/module/product/<module_name>/detail/<barcode>

🔹 Update Product

    1. Click Update

    2. The landing page will now be available at http://127.0.0.1:8000/module/product/<module_name>/update/<barcode>

    3. Fill the field click Update

    4. The system will automatically apply changes

🔹 Delete Product

    1. Click Delete

    2. The Product selected will popout validation 'Are you sure to Delete this Record?' then click Yes

    3. The Product and its landing page will be removed
## Screenshots
![App Screenshot 1](https://github.com/user-attachments/assets/9c1eb3c1-ed48-4f0a-b0d6-98295311b8dc)

![App Screenshot 2](https://github.com/user-attachments/assets/9f8e66d7-30c1-40f9-98ad-945c05f5794e)

![App Screenshot 3](https://github.com/user-attachments/assets/40d685e9-95d5-4699-b108-f15c82a52392)

![App Screenshot 4](https://github.com/user-attachments/assets/ca3e5388-1c32-48d8-89e4-1b28d53f034d)

![App Screenshot 5](https://github.com/user-attachments/assets/70467495-bc6d-4a35-b3f3-26ed88a2eb3c)

![App Screenshot 6](https://github.com/user-attachments/assets/c9ec3100-5cb7-4044-990a-e45fafa3c0a1)

![App Screenshot 7](https://github.com/user-attachments/assets/cae79d76-3e56-4783-8d42-a9411d8fec13)

![App Screenshot 8](https://github.com/user-attachments/assets/e2b64c1c-6ca8-4e89-a2aa-4092728dda4f)

## License

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)]((https://choosealicense.com/licenses/mit/))

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)  

![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)  

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)

## Contact

[![LinkedIn](https://img.shields.io/badge/LinkedIn-FarizAfkar-blue?logo=linkedin)](https://www.linkedin.com/in/farizafkar/)  
[![Email](https://img.shields.io/badge/Email-Contact%20Me-red?logo=gmail)](mailto:high.oc7ane@gmail.com)
