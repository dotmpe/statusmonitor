include                $(MK_SHARE)Core/Main.dirstack.mk
MK_$d               := $/Rules.mk
MK                  += $(MK_$d)
#
#      ------------ -- 

CLN += $(shell find ./ -name '*.pyc')

#      ------------ -- 
#

STRGT +=  init-tmp-db
TRGT  +=  init-tmp-db

init-tmp-db:
	@python src/python/datastore.py
	@$(call log,Done,$@)

#      ------------ -- 

monitor_$d          := $(BUILD_$/)monitor/index.php\
                       $(BUILD_$/)monitor.js\
                       $(BUILD_$/)monitor.n
monitor: $(monitor_$d)

TRGT                += $(monitor_$d)
CLN                 += $(monitor_$d)

#      ------------ --

HX                  := 
HX_$d               := $(shell find $/src/haxe/ -iname '*.hx')
HX_CP               := $/src/haxe $/test/hx

$(BUILD_$/)monitor.js: $(HX_$d)
	@$(ll) file_target "$@"
	@$(mk-target)
	@haxe $(HX) $(HX_CP:%=-cp %) -main com.dotmpe.statusmonitor.Client -js $@
	@$(ll) file_ok "$@"

$(BUILD_$/)monitor/index.php: $(HX_$d)
	@$(ll) file_target "$@"
	@$(mk-target)
	@haxe $(HX) $(HX_CP:%=-cp %) -main com.dotmpe.statusmonitor.Server -php $(@D)
	@$(ll) file_ok "$@"

$(BUILD_$/)monitor.n: $(HX_$d)
	@$(ll) file_target "$@"
	@$(mk-target)
	@haxe $(HX) $(HX_CP:%=-cp %) -main com.dotmpe.statusmonitor.Server -neko $@
	@$(ll) file_ok "$@"

#      ------------ -- 
#
include                $(MK_SHARE)Core/Main.dirstack-pop.mk
# vim:noet:
