
def fix_legacy_database_uri(uri):
    """ Fixes legacy Database uris, like postgres:// which is provided by Heroku but no longer supported by SqlAlchemy """
    if uri.startswith('postgres://'):
      uri = uri.replace('postgres://', 'postgresql://', 1)
    return uri
