from django.core.exceptions import ValidationError
from .mixins import VkProfileValidator
from .errors import WrongVkProfile
from .models import Profile


def validate_vk_profile(vk_link):
    try:
        VkProfileValidator().check_vk_profile(vk_link=vk_link)
    except WrongVkProfile:
        raise ValidationError('Такого профиля не существует', code='invalid')
    try:
        _ = Profile.objects.get(vk_link__icontains=vk_link)
        raise ValidationError('Данный профиль уже используется', code='invalid')
    except Profile.DoesNotExist:
        pass
    return vk_link
