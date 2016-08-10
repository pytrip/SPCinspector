#!/usr/bin/env python3
import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from spcread import *

ppp = ""

class Handler:

    def __init__(self):
        global ppp

        self.window1 = builder.get_object("window1")
        self.window1.set_title("SPCinspector - No file loaded")

        self.label0 = builder.get_object("label0")
        self.label1 = builder.get_object("label1")
        self.label2 = builder.get_object("label2")
        self.label3 = builder.get_object("label3")
        self.label4 = builder.get_object("label4")
        self.label5 = builder.get_object("label5")
        self.label6 = builder.get_object("label6")
        self.label7 = builder.get_object("label7")
        self.label8 = builder.get_object("label8")
#        self.label9 = builder.get_object("label9")
#        self.label10 = builder.get_object("label10")
#        self.label11 = builder.get_object("label11")
        self.label12 = builder.get_object("label12")
        self.label13 = builder.get_object("label13")
        self.label14 = builder.get_object("label14")
        self.label15 = builder.get_object("label15")
        self.label16 = builder.get_object("label16")
        self.label17 = builder.get_object("label17")
        self.label18 = builder.get_object("label18")
        self.label19 = builder.get_object("label19")
        self.label20 = builder.get_object("label20")
        self.label21 = builder.get_object("label21")
        self.label22 = builder.get_object("label22")
        self.label23 = builder.get_object("label23")
        self.label24 = builder.get_object("label24")
        self.label25 = builder.get_object("label25")
        self.label26 = builder.get_object("label26")
        
        self.spin1 = builder.get_object("spin1") # depth
        self.spin2 = builder.get_object("spin2") # species
        self.spin3 = builder.get_object("spin3") # E-bins

        self.spin1.set_sensitive(False)
        self.spin2.set_sensitive(False)
        self.spin3.set_sensitive(False)
        
        self.button1 = builder.get_object("button1")
        self.button2 = builder.get_object("button2")
        self.button1.set_sensitive(False)
        
        self.cur_depth = 0
        self.cur_species = 0
        self.cur_ebin = 0
        
        self.spc = []
        self.path = ""
        
        print(ppp)
        if os.path.isfile(ppp):
            self.load_spc(ppp)
        
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button1):
        print("Hello World!")
        
    def main_quit(self, *args):
        print("Call Gtk.main_quit")
        Gtk.main_quit(*args)

    def on_spin1_value_changed(self,*args):
        self.cur_depth = self.spin1.get_value_as_int()-1       
        self.set_labels(self.spc)

    def on_spin2_value_changed(self,*args):
        self.cur_species = self.spin2.get_value_as_int()-1
        self.set_labels(self.spc)
        
    def on_spin3_value_changed(self,*args):
        self.cur_ebin = self.spin3.get_value_as_int()-1
        self.set_labels(self.spc)

    def on_menuopen_activate(self,*args):
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        #self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            path = dialog.get_filename()
            dialog.destroy()
            self.load_spc(path)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()
        
    def load_spc(self,path):
        spc = SPC(path)
        spc.read_spc()

        self.filename = os.path.split(path)[1]
        self.window1.set_title("SPCinspector - "+ self.filename)
        
        self.spin1.set_range(1,spc.ndsteps)
        self.spin2.set_range(1,spc.data[self.cur_depth].nparts)
        self.spin3.set_range(1,spc.data[self.cur_depth].species[self.cur_species].ne)

        self.spin1.set_sensitive(True)
        self.spin2.set_sensitive(True)
        self.spin3.set_sensitive(True)

        self.button1.set_sensitive(True)
        self.set_labels(spc)
        self.spc = spc

    def set_labels(self,spc):
        self.label0.set_text(self.filename)
        self.label1.set_text(spc.filetype)
        self.label2.set_text(spc.fileversion)
        self.label3.set_text(spc.filedate)
        self.label4.set_text(spc.targname)
        self.label5.set_text(spc.projname)
        self.label6.set_text('{:f}'.format(spc.energy))
        self.label7.set_text('{:f}'.format(spc.peakpos))
        self.label8.set_text('{:f}'.format(spc.norm))
        # - depth
        self.label12.set_text('{:d}'.format(spc.ndsteps))

        d = spc.data[self.cur_depth]
        self.label13.set_text('{:f}'.format(d.depth))
        self.label14.set_text('{:f}'.format(d.dsnorm))

        # - species 
        self.label15.set_text('{:d}'.format(d.nparts))
        ds = d.species[self.cur_species]
        self.label16.set_text('{:f} {:f}'.format(ds.z,ds.a))
        self.label17.set_text('{:d} {:d}'.format(ds.lz,ds.la))
        self.label18.set_text('{:f}'.format(ds.dscum)) # running cum.sum over species
        self.label19.set_text('{:d}'.format(ds.nc))
        
        # - energy
        self.label20.set_text('{:d}'.format(ds.ne))
        dse = ds.ebindata[self.cur_ebin]
        if self.cur_ebin == 0:
            dsel = dse
        else:
            dsel = ds.ebindata[self.cur_ebin-1]            
        dsh = ds.histdata[self.cur_ebin]
        dsc = ds.rcumdata[self.cur_ebin]
        self.label21.set_text('{:.4f} {:.4f} {:.4f}'.format(dsel,(dsel+dse)*0.5,dse))
        self.label22.set_text('{:f}'.format(dse - dsel))
        self.label23.set_text('{:f}'.format(dsh))
        self.label24.set_text('{:f}'.format(dsh*(dse-dsel)))
        self.label25.set_text('{:f}'.format(dsc)) #cummulative sum
        self.label26.set_text('{:.2f} {:.2f}'.format(ds.ebindata.min(),ds.ebindata.max())) 

        

if sys.argv[1] != None:
    ppp = sys.argv[1]
builder = Gtk.Builder()
builder.add_from_file("spcinspect.glade")
builder.connect_signals(Handler())

window1 = builder.get_object("window1")
window1.show_all()


Gtk.main()
