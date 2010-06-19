# -*- coding:utf-8 -*-

from django.core.management.base import AppCommand

from codewars.web.models import *

import time, Queue
from thread import start_new_thread

# =======================================================

def battleStart(bt, vs):
	try:
		virts = []
		
		bt.stage = 2
		bt.save()
	
		p = __import__('codewars.engine.%s.custom' % bt.engine.slug)
		bots = []
		for x in bt.bots.select_related('lang').all():
			v = vs.get()
			virts.append(v)
			bots.append(p.Bot(
							x.id,
							x.exe(),
							v.IP,
							v.username
							))
		
		bt.stage = 3
		bt.save()
		
		g = p.Engine(bots)
		g.start()
		
		bt.stage = 4
		bt.save()
	
	except:
		bt.stage = 5
		bt.save()

	finally:
		try:
			for x in virts:
				vs.put(x)
		except:
			pass

# =======================================================

class Command(AppCommand):

	def main(self):
		
		while 1:
			
			battles = Battle.objects.filter(stage=1).exclude(bots__compiled=0
						).select_related('engine', 'map').order_by('type', 'time')
			
			if not battles.count():
				time.sleep(10)
				continue
			
			for bt in battles:
				start_new_thread(battleStart, (bt, self.vs))


	def handle(self, *args, **options):

		virts = Virtual.filter(compiler=0)
		
		self.vs = Queue.Queue(256)
		for n in range(6):
			for v in virts:
				self.vs.put(v)
		
		self.main()
		

