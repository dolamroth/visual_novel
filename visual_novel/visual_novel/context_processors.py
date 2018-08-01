def global_settings(request):
    return {
        'custom_admin_header_settings': _admin_custom_header_settings()
    }


def _admin_custom_header_settings():
    admin_header = dict()
    admin_header['header_title'] = 'Администрирование vn-russian'
    return admin_header
