#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from spcread import *

class Handler:

    def __init__(self):
        self.label1 = builder.get_object("label1")
        self.label2 = builder.get_object("label2")
        self.label3 = builder.get_object("label3")
        self.label4 = builder.get_object("label4")
        self.label5 = builder.get_object("label5")
        self.label6 = builder.get_object("label6")
        self.label7 = builder.get_object("label7")
        self.label8 = builder.get_object("label8")
        self.label9 = builder.get_object("label9")
        self.label10 = builder.get_object("label10")
        self.label11 = builder.get_object("label11")
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
        
        self.spin1 = builder.get_object("spin1") # depth
        self.spin2 = builder.get_object("spin2") # species
        self.spin3 = builder.get_object("spin3") # E-bins

        self.spin1.set_sensitive(False)
        self.spin2.set_sensitive(False)
        self.spin3.set_sensitive(False)
        
        self.button1 = builder.get_object("button1")
        self.button2 = builder.get_object("button2")
        self.button1.set_sensitive(False)
        
    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button1):
        print("Hello World!")
        self.set_labels()
        
    def main_quit(self, *args):
        print("Call Gtk.main_quit")
        Gtk.main_quit(*args)

    def on_spin1_value_changed(self,*args):
        print("spin1 vc")

    def on_spin2_value_changed(self,*args):
        print("spin2 vc")

    def on_spin3_value_changed(self,*args):
        print("spin3 vc")

    def on_menuopen_activate(self,*args):
        print("open menu")

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
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()

        spc = SPC(path)
        spc.read_spc()

        cur_depth = 0
        cur_species = 0
        cur_ebin = 0
        

        self.spin1.set_range(1,spc.ndsteps)
        self.spin2.set_range(1,spc.data[cur_depth].nparts)
        self.spin3.set_range(1,spc.data[cur_depth].species[cur_species].ne)

        self.spin1.set_sensitive(True)
        self.spin2.set_sensitive(True)
        self.spin3.set_sensitive(True)

        self.button1.set_sensitive(True)
        #print(str(spc.ndsteps))
        #print(str(spc.data[cur_depth].nparts))
        
        self.set_labels(spc)
        

    def set_labels(self,spc):
        self.label1.set_text(spc.filetype)
        self.label2.set_text(spc.fileversion)
        self.label3.set_text(spc.filedate)
        self.label4.set_text(spc.targname)
        self.label5.set_text(spc.projname)
        self.label6.set_text('{:f}'.format(spc.energy))
        self.label7.set_text('{:f}'.format(spc.peakpos))
        self.label8.set_text('{:f}'.format(spc.norm))
        self.label9.set_text('{:d}'.format(spc.ndsteps))

        
        
            
builder = Gtk.Builder()
builder.add_from_file("spcinspect.glade")
builder.connect_signals(Handler())

window1 = builder.get_object("window1")
window1.show_all()

Gtk.main()
