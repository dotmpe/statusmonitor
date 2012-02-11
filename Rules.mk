include                $(MK_SHARE)Core/Main.dirstack.mk
MK_$d               := $/Rules.mk
MK                  += $(MK_$d)
#
#      ------------ -- 

CLN += $(shell find ./ -name '*.pyc')

#      ------------ -- 
#
STRGT_$d = \
	init-tmp-db
STRGT += $(STRGT_$d)

TRGT_$d = \
	init-tmp-db
STRGT += $(STRGT_$d)
TRGT += $(TRGT_$d) \
		com.dotmpe.statusmonitor.Test.n

$/com.dotmpe.statusmonitor.Test.n: src/haxe
	haxe -x com.dotmpe.statusmonitor.Test -cp src/haxe

init-tmp-db:
	@python src/python/datastore.py
	@$(call log,Done,$@)

#      ------------ -- 
#
include                $(MK_SHARE)Core/Main.dirstack-pop.mk
# vim:noet:
