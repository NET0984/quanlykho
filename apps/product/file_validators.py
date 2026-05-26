from django.core.exceptions import ValidationError


def validate_file_image(file):
    if not file:
        return
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("Anh vuot qua 5MB")

    valid_types = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
    if file.content_type not in valid_types:
        raise ValidationError("Chi chap nhan JPG, JPEG, PNG, WEBP")
