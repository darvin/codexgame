# -*- coding:utf-8 -*-

from django.core.management.base import AppCommand

from codewars.web.models import *

import os, time

# =======================================================

class Command(AppCommand):

	def handle(self):
		
		SSH_EXEC_PATH = "/usr/bin/ssh"
		SCP_EXEC_PATH = "/usr/bin/scp"
		TMP_SOURCE = "/tmp/source"
		TMP_COMPILED = "/tmp/compiled"

		while 1:
			
			virt = Virtual.filter(compiler=1)[0]
			
			bots = Bot.objects.filter(compiled=False, lang__compilation=True, battles__stage=1
									).select_related('lang').order_by('battles__type', 'time')
			
			if not bots.count():
				time.sleep(10)
				continue
			
			for b in bots:
				os.system("%s %s %s@%s:%s" %\
					( SCP_EXEC_PATH, b.source(), virt.username, virt.IP, TMP_SOURCE ))
				os.system("%s %s@%s %s %s %s %s" %\
					( SSH_EXEC_PATH, virt.username, virt.IP, b.lang.compiler, TMP_SOURCE, b.lang.option, TMP_COMPILED ))
				os.system("%s %s@%s:%s %s" %\
					( SCP_EXEC_PATH, virt.username, virt.IP, TMP_SOURCE, player.exe() ))

				b.compiled = True
				b.save()



# =======================================================
# =======================================================
# =======================================================
# =======================================================
