# Copyright 2018 Janos Klieber, Roberts Kolosovs, Peter Spieler
# This file is part of Phoenixserver.
#
# Phoenixserver is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Phoenixserver is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Phoenixserver.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings

default_headers = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'user-agent',
    'accept-encoding',
)

CORS_ALLOW_HEADERS = getattr(settings, 'CORS_ALLOW_HEADERS', default_headers)

default_methods = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
)
CORS_ALLOW_METHODS = getattr(settings, 'CORS_ALLOW_METHODS', default_methods)

CORS_ALLOW_CREDENTIALS = getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)

CORS_PREFLIGHT_MAX_AGE = getattr(settings, 'CORS_PREFLIGHT_MAX_AGE', 86400)

CORS_ORIGIN_ALLOW_ALL = getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', True)

CORS_ORIGIN_WHITELIST = getattr(settings, 'CORS_ORIGIN_WHITELIST', ())

CORS_ORIGIN_REGEX_WHITELIST = getattr(
    settings,
    'CORS_ORIGIN_REGEX_WHITELIST',
    ())

CORS_EXPOSE_HEADERS = getattr(settings, 'CORS_EXPOSE_HEADERS', ())

CORS_URLS_REGEX = getattr(settings, 'CORS_URLS_REGEX', '^.*$')

CORS_MODEL = getattr(settings, 'CORS_MODEL', None)

CORS_REPLACE_HTTPS_REFERER = getattr(
    settings,
    'CORS_REPLACE_HTTPS_REFERER',
    False)
CORS_URLS_ALLOW_ALL_REGEX = getattr(settings, 'CORS_URLS_ALLOW_ALL_REGEX', ())
