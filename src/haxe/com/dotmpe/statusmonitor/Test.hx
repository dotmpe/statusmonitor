package com.dotmpe.statusmonitor;

class Test {
	public static function main():Void {
		trace("Test.main");
		data.content = StringTools.htmlEscape(Std.string("Bladie"));
		Web.setHeader("Content-Type", "application/xhtml+xml");
		tpl = File.read("var/tpl/main.xhtml");
		Lib.print(new Template(tpl).execute(data));
	}
}
