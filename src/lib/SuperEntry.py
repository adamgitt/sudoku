import gtk, pango

class SuperEntry (gtk.AspectFrame):

    main_size = 9
    
    def __init__ (self):
        gtk.AspectFrame.__init__(self,ratio=1,obey_child=False)
        self.set_shadow_type(gtk.SHADOW_IN)
        self.vb = gtk.VBox(); self.vb.show()
        self.al = gtk.Alignment(); self.al.show()
        self.al.add(self.vb)
        self.add(self.al)
        self.al.set_property('xalign',0.5); self.al.set_property('xscale',0.5)
        self.al.set_property('yalign',0.5); self.al.set_property('yscale',0.5)
        self.setup_main_entry()
        self.sub_entry = gtk.Entry()
        self.top_entry = gtk.Entry()
        self.top_entry.set_width_chars(5)
        self.sub_entry.set_width_chars(5)
        self.main_font = pango.FontDescription()
        self.sub_font = pango.FontDescription()
        self.main_font.set_size(pango.SCALE * self.main_size)
        self.main_entry.modify_font(self.main_font)
        self.sub_font.set_size(int(pango.SCALE * self.main_size*(9.0/16)))
        self.sub_entry.modify_font(self.sub_font)
        self.top_entry.modify_font(self.sub_font)        
        self.vb.pack_start(self.top_entry,expand=False,fill=False); self.top_entry.show()        
        self.vb.pack_start(self.main_entry,expand=False,fill=False); self.main_entry.show()
        self.vb.pack_start(self.sub_entry,expand=False,fill=False); self.sub_entry.show()        
        color = gtk.gdk.color_parse('white')
        for e in ['main_entry','sub_entry','top_entry']:
            e = getattr(self,e)
            e.set_has_frame(False)
        self.just_allocated = False
        self.connect('size-allocate',self.allocate_cb)
            #e.modify_bg(gtk.STATE_NORMAL,color)
            #e.modify_base(gtk.STATE_NORMAL,color)
            #e.modify_fg(gtk.STATE_NORMAL,color)

    def allocate_cb (self, widg, rect):
        return
        if self.just_allocated: return
        if rect.height > rect.width: side = rect.height
        elif rect.height < rect.width: side = rect.width
        else: return
        self.set_property('width-request',side)
        self.set_property('height-request',side)
        rect = self.main_entry.get_allocation()
        self.main_entry.set_property('height-request',rect.height)
        self.just_allocated = True
        gobject.timeout_add(500,
                            lambda *args: setattr(self,'just_allocated',False)
                            )

    def do_it_for_all (f):
        name = f.__name__
        def foo (self,*args,**kwargs):
            getattr(self.sub_entry,
                    name)(*args,**kwargs)
            getattr(self.top_entry,
                    name)(*args,**kwargs)
            return getattr(self.main_entry,
                    name)(*args,**kwargs)
        return foo
    
    @do_it_for_all
    def modify_bg (self,*args,**kwargs): pass

    @do_it_for_all
    def modify_fg (self,*args,**kwargs): pass

    @do_it_for_all
    def modify_base (self,*args,**kwargs): pass

    @do_it_for_all
    def set_editable (self,*args,**kwargs): pass

    def modify_font (self, newfont):
        if newfont.get_size():
            #print 'special modify_font'
            self.main_font = newfont
            self.sub_font = newfont.copy()
            self.sub_font.set_size(
                int(self.main_font.get_size()*(9.0/16))
                )
            self.sub_entry.modify_font(self.sub_font)
            self.top_entry.modify_font(self.sub_font)
            self.main_entry.modify_font(self.main_font)
        else:
            #print 'plain old modify_font'
            doer = self.do_it_for_all(self.modify_font)
            return doer(newfont)

    def get_note_text (self):
        return self.top_entry.get_text(),self.sub_entry.get_text()

    def set_note_text (self, top=None, bottom=None):
        if top is not None:
            self.top_entry.set_text(top)
        if bottom is not None:
            self.sub_entry.set_text(bottom)
    
    def setup_main_entry (self):
        self.main_entry = gtk.Entry()
        self.main_entry.set_width_chars(5)
        self.main_entry.set_alignment(0.5)
        self.main_entry.set_max_length(1)


    def __getattr__ (self, attname):
        # This should raise an attribute error if it fails, which will
        # automatically get us normal behavior
        try:
            return getattr(self,attname)
        except:
            return getattr(self.main_entry,attname)
        #except:
        #    raise

if __name__ == '__main__':
    w = gtk.Window()
    w.connect('delete-event',lambda *args: gtk.main_quit())
    vb = gtk.VBox()
    l = gtk.Label('Super Entry: '); l.show()
    vb.pack_start(l)
    tb = gtk.Table()
    tb.set_row_spacings(6)
    tb.set_col_spacings(6)
    def foo (*args):
        print args
    for x in range(5):
        for y in range(5):
            se = SuperEntry(); se.show()
            #al = gtk.Alignment()
            #af = gtk.AspectFrame(None,0.5,0.5,1,False)
            se.set_text('4')
            #al.add(se)
            #af.add(al)
            #af.show_all()
            #al.set_property('xscale',0.5); al.set_property('xalign',0.5)
            #al.set_property('yscale',0.5); al.set_property('yalign',0.5)
            #se.connect('changed',foo)
            tb.attach(se,x,x+1,y,y+1)
            if y/3 == 2:
                se.modify_base(gtk.STATE_NORMAL,
                               gtk.gdk.color_parse('#f00')
                               )
                se.modify_fg(gtk.STATE_NORMAL,
                               gtk.gdk.color_parse('#f00')
                               )
                se.modify_bg(gtk.STATE_NORMAL,
                               gtk.gdk.color_parse('#f00')
                               )                
    vb.pack_start(tb); tb.show()
    w.add(vb)
    vb.show()
    w.present()
    gtk.main()
