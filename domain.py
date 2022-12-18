from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

# Get path (/for_instance/maybe)
def get_path(url):
    try:
        return urlparse(url).path
    except:
        return ''

# Get nth path segment (/for_instance)
def get_nth_path_segment(url, n):
    try:
        results = get_path(url).split('/')
        return results[n]
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
