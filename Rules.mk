include                $(MK_SHARE)Core/Main.dirstack.mk
MK_$d               := $/Rules.mk
MK                  += $(MK_$d)
#
#      ------------ -- 


#ifneq ($(call get-bin,python),)
include                ./Rules.python.mk
#endif

#      ------------ -- 

ifneq ($(shell which haxe),)
BIN                 += haxe=$(shell which haxe)
endif

ifneq ($(call get-bin,haxe),)
include                ./Rules.haxe.mk
endif


#      ------------ -- 
#
include                $(MK_SHARE)Core/Main.dirstack-pop.mk
# vim:noet:
