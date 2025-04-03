import base64
import os
from django import template
from django.conf import settings

register = template.Library()

def add_base64_padding(data):
    """
    Ensures the Base64 string has the correct padding (`=` characters).
    """
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

@register.filter(name='decode_base64_file')
def decode_base64_file(data, filename):
    """
    Decodes a URL-safe Base64-encoded file and saves it to the media directory.

    :param data: Base64-encoded string (without the data URL prefix)
    :param filename: The desired filename to save
    :return: The file URL of the saved file
    """
    try:
        # Remove metadata prefix (e.g., "data:image/png;base64,")
        if "," in data:
            data = data.split(",")[1]

        # Ensure proper padding
        data = add_base64_padding(data)

        # Decode URL-safe Base64
        file_data = base64.urlsafe_b64decode(data)

        # Ensure the media directory exists
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the file
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Return the file URL for use in templates
        return os.path.join(settings.MEDIA_URL, filename)

    except Exception as e:
        return f"Error: {str(e)}"