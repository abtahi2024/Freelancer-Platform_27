from django.core.exceptions import ValidationError

def validate_file_size(file):
    """This validator validates if file size is less than 50 MB"""
    max_size = 50  # MB
    max_size_in_bytes = max_size * 1024 * 1024

    if file.size > max_size_in_bytes:
        raise ValidationError(f"File cannot be larger than {max_size} MB!")
