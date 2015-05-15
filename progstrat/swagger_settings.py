from _version import __version__

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': __version__,
    'api_path': '',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'info': {
        'contact': 'mcdevitt.ryan@gmail.com',
        'description': 'This is the API Documentation for Turn Based Multiplayer Progressional Game',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'Turn Based Progressional Game',
    },
    'doc_expansion': 'none',
}