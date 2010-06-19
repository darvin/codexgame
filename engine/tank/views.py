# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

import random, math, re

# ==========================================================

class mapMaker:
	
	def makeMainLayer(self):
		
		TAIL_RANDOM = {
			'DDDD': (1, 6),
			'GGGG': (8, 13),
			'SSSS': (15, 20),
			
			# ----------------
			
			'DDDG': 22,
			'DDGD': 23,
			'DGDD': 29,
			'GDDD': 30,

			'GGGD': 24,
			'GGDG': 25,
			'GDGG': 31,
			'DGGG': 32,
			
			'DGGD': 26,
			'GDDG': 33,

			'DGDG': 27,
			'GDGD': 34,

			'DDGG': 28,
			'GGDD': 35,

			# ----------------
			
			'DDDS': 36,
			'DDSD': 37,
			'DSDD': 43,
			'SDDD': 44,
			
			'SSSD': 38,
			'SSDS': 39,
			'SDSS': 45,
			'DSSS': 46,
			
			'DSSD': 40,
			'SDDS': 47,

			'DSDS': 41,
			'SDSD': 48,

			'DDSS': 42,
			'SSDD': 49,
			}
		
		def makeTile(*p):
			try:
				x = TAIL_RANDOM[''.join(p)]
				if type(x) == tuple:
					return random.randint(*x)
				return x
			except KeyError:
				return 'X'
		
		def XY2N(y, x):
			return y*self.width+x
		
		def arcFill(count, height, char):
			for i in range(random.randint(*count)):
				h = random.randint(*height)
				w = random.randint(max(h-2, 2), h+2)
				t = random.randint(-self.height-1, self.height-1)
				l = random.randint(-self.width-1, self.width-1)
				for hx in range(h):
					s = int( math.cos(float(hx)/h*2-1)*w )
					for ss in range(s):
						xx = t+hx
						yy = l+(w-s)/2+ss
						for x in (
								XY2N(xx-1, yy-1), XY2N(xx, yy-1), XY2N(xx+1, yy-1),
								XY2N(xx-1, yy), XY2N(xx, yy), XY2N(xx+1, yy),
								XY2N(xx-1, yy+1), XY2N(xx, yy+1), XY2N(xx+1, yy+1)
								):
									try:
										if v[x] not in ('D', char):
											v[x] = 'D'
									except IndexError:
										pass			
						try:
							v[XY2N(xx, yy)] = char
						except IndexError:
							pass			
		
		v = ['D']*((self.height+1)*(self.width+1))
		
		arcFill((1, self.scale/30), (self.height/3, self.height), 'S')
		arcFill((1, self.scale/20), (self.height/5, self.height/2), 'G')
		
		vv = []
		for y in range(self.height):
			for x in range(self.width):
				vv.append(makeTile(
								v[XY2N(y, x)],
								v[XY2N(y, x+1)],
								v[XY2N(y+1, x)],
								v[XY2N(y+1, x+1)]
								))
		
		'''
		for i in range(random.randint(0, self.scale/30)):
			h = random.randint(1, self.scale/28)
			w = random.randint(1, max(1, self.scale/28-h))
			t = random.randint(0, self.height-h)
			l = random.randint(0, self.width-w)
			for hx in range(h):
				for wx in range(w):
					try:
						vv[XY2N(t+hx, l+wx)] = 7
					except IndexError:
						pass
		'''
		
		return vv
	
	def makeBarriers(self):
		v = ['_']*(self.width*self.height)

		def XY2N(y, x):
			return y*self.width+x
				
		for i in range(max(3, self.scale/10)):
			h = random.randint(3, self.height-1)
			if random.randint(1, 2) == 1:	# вертикальная
				t = random.randint(1, self.height-h)
				l = random.randint(0, self.width-1)
				for x in range(t, t+h):
					n = XY2N(x, l)
					if v[n] == 'D':
							v[n] = 'M'
					else:	v[n] = 'D'

			
			else:							# горизонтальная
				h = min(h, self.width)
				t = random.randint(1, self.height-1)
				l = random.randint(0, self.width-h)
				for x in range(l, l+h):
					n = XY2N(t, x)
					if v[n] == 'D':
							v[n] = 'M'
					else:	v[n] = 'D'			
		
		vv1 = []
		vv2 = []
		for y in range(len(v)/self.width):
			w1 = v[y*self.width:(y+1)*self.width]
			w2 = w1[:]
			w2.reverse()
			w = w1+w2
			vv1 = vv1 + w
			vv2 = w + vv2
		return vv1 + vv2
	
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.scale = width*height
		self.lDirt = self.makeMainLayer()
		self.lBlock = list(self.makeBarriers())

	def pxHeight(self):
		return self.height*64

	def pxWidth(self):
		return self.width*64
	
	def randPerc(self):
		return random.randint(0, 100)

# ==========================================================

def testMakeMap(request):
	
	m = mapMaker(12, 8)
	
	return render_to_response('tank/map.html',
			{
			'map': m,
			})






