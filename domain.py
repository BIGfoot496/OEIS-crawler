from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

# Get second path segment (/maybe)
def get_second_path_segment(url):
    try:
        results = get_path(url).split('/')
        return results[2]
    except:
        return ''

# Get first path segment (/for_instance)
def get_first_path_segment(url):
    try:
        results = get_path(url).split('/')
        return results[1]
    except:
        return ''
    
# Get path (/for_instance/maybe)
def get_path(url):
    try:
        return urlparse(url).path
    except:
        return ''

# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''