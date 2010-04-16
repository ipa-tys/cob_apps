#!/usr/bin/python
import roslib; roslib.load_manifest('cob_tactiletools')
import rospy
from cob_msgs.msg import TactileMatrix
import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo
import threading
import time

#Initializing the gtk's thread engine
gtk.gdk.threads_init()

class Screen(gtk.DrawingArea):

	# Draw in response to an expose-event
	__gsignals__ = { "expose-event": "override" }
	sizex = 3
	sizey = 5

	# Handle the expose-event by drawing
	def do_expose_event(self, event):
		# Create the cairo context
		cr = self.window.cairo_create()
		#print "Width: ", self.allocation.width
		#print "Height: ", self.allocation.height
		# Restrict Cairo to the exposed area; avoid extra work
		cr.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
		cr.clip()
		self.draw(cr, self.allocation.width,self.allocation.height )

	def draw(self, cr, width, height):
		# Fill the background with gray
		color = 0.5
		xw = width/(self.sizex)
		yw = height/(self.sizey)
		for i in range(0,self.sizex):
			for j in range(0,self.sizey):
				if(color==0.0):
					color=1.0
				else:
					color=0.0
				cr.set_source_rgb(color, 1-color, 0.5)
				cr.rectangle((i)*xw, (j)*yw, xw, yw)
				cr.fill()

	def setMatrixSize(self, matrixx, matrixy):
		self.sizex = matrixx
		self.sizey = matrixy

	def updateTactileMatrix(self, string):
		print "Got something: ", string
		self.queue_draw()


			
def roscb(data):
	global sc1
	global testv
	gtk.threads_enter()
	if (testv == 0):
		sc1.setMatrixSize(5,13)
		testv = 1
	else:
		sc1.setMatrixSize(7,11)
		testv = 0
	sc1.updateTactileMatrix("test")
	gtk.threads_leave()


# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def main_quit(obh, obb):
	#Stopping the thread and the gtk's main loop
	gtk.main_quit()

try:
	window = gtk.Window()
	winwidth = 400
	winheight = 400
	window.set_size_request(winwidth,winheight)
	window.set_title("TactileSensorData")
	testv = 0
	sc1 = Screen()
	sc1.set_size_request((winwidth/3)-10, (winheight/2)-5)
	sc2 = Screen()
	sc2.set_size_request((winwidth/3)-10, (winheight/2)-5)
	sc3 = Screen()
	sc3.set_size_request((winwidth/3)-10, (winheight/2)-5)
	sc4 = Screen()
	sc4.set_size_request((winwidth/3)-10, (winheight/2)-5)
	sc5 = Screen()
	sc5.set_size_request((winwidth/3)-10, (winheight/2)-5)
	sc6 = Screen()
	sc6.set_size_request((winwidth/3)-10, (winheight/2)-5)
	hbox1=gtk.HBox(False ,10 )
	hbox1.pack_start(sc1,False, True, 0)
	hbox1.pack_start(sc2,False, True, 0)
	hbox1.pack_start(sc3,False, True, 0)
	hbox2=gtk.HBox(False,10)
	hbox2.pack_start(sc4,False, True, 0)
	hbox2.pack_start(sc5,False, True, 0)
	hbox2.pack_start(sc6,False, True, 0)
	vbox=gtk.VBox(True,0)
	vbox.pack_start(hbox1,False, False, 0)
	vbox.pack_start(hbox2,False, False, 0)
	window.add(vbox)
	window.show_all()
	window.connect("delete-event", main_quit)
	window.present()
	rospy.init_node('TactileSensorView', anonymous=True)
	rospy.Subscriber("cob_sdh/tactile_data", TactileMatrix, roscb)
	gtk.main()
except KeyboardInterrupt:
    main_quit("tut", "tut")
