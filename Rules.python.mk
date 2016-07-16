

#      ------------ -- 
CLN                 += $(shell find ./ -name '*.pyc')

#      ------------ -- 

URWID_EXAMPLES      := tour graph edit browse subproc palette_test pop_up \
											bigtext treesample lcd_cf635

var/urwid/examples:: 
	mkdir -vp $@
	cd $@ ; for name in $(URWID_EXAMPLES); \
	do test -e "$$name.py" || wget https://raw.githubusercontent.com/urwid/urwid/master/examples/$$name.py; \
	done

TRGT                += var/urwid/examples

#      ------------ -- 


