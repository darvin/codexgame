# -*- coding: utf-8 -*-

from settings import MIDDLEWARE_CLASSES, INSTALLED_APPS

DEBUG = True

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'codewars'
DATABASE_USER = 'codewars'
DATABASE_PASSWORD = 'insecticid'

MEDIA_ROOT = 'C:/BigApache/proj/codewars/media'
#LOG_PATH = 'C:/BigApache/proj/codewars/logs'

TEMPLATE_DIRS = (
	'C:/BigApache/proj/codewars/templates',
)

if DEBUG:
	MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
	INSTALLED_APPS += ('debug_toolbar',)

	DEBUG_TOOLBAR_PANELS = (
		#'debug_toolbar.panels.version.VersionDebugPanel',
		'debug_toolbar.panels.timer.TimerDebugPanel',
		'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
		'debug_toolbar.panels.headers.HeaderDebugPanel',
		'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
		'debug_toolbar.panels.template.TemplateDebugPanel',
		'debug_toolbar.panels.sql.SQLDebugPanel',
		'debug_toolbar.panels.cache.CacheDebugPanel',
		'debug_toolbar.panels.logger.LoggingPanel',
	)
	
	DEBUG_TOOLBAR_CONFIG = {
		'EXCLUDE_URLS': ('/admin',),
		'INTERCEPT_REDIRECTS': False,
	}






