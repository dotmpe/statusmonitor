/* 
 */
package com.dotmpe.statusmonitor;

import haxe.Log;
import haxe.PosInfos;
import haxe.Template;
import haxe.remoting.Context;
import haxe.remoting.HttpConnection;
#if neko
import neko.Lib;
import neko.Web;
import neko.io.File;
#elseif php
import php.Lib;
import php.Web;
import php.io.File;
#else
#error
#end


typedef Data = 
{
	var title:String;
	var parent:String;
	var endpoint:String;
	var prolog:String;
	var header:String;
	var content:String;
	var footer:String;
	var epilog:String;
}

class Server extends Monitor
{
	/**
	 */
	public function new() 
	{
	}

	/** Process a server-side sandpit session */
	public function handleRequest()
	{
		var data = DATA;
//		data.log = this.log;
		data.content = StringTools.htmlEscape(Std.string(data));
	//	new Sandpit(session, false)
	//			.assemble(spec)
	//			.render();

		Web.setHeader("Content-Type", "application/xhtml+xml");
		var tpl = File.getContent("var/tpl/main.xhtml");
		Lib.print(new Template(tpl).execute(data));
	}

	/** Server-side entry-points */
	public static function main():Void
	{
#if neko		
//		if (Web.isModNeko) 
			// not completely clear on how this works..
			Web.cacheModule(run);
#end			
		run();
	}

	var log:Array<Array<Dynamic>>;

	static function handleTrace(v:Dynamic, ?info:PosInfos)
	{
		//log.append([v, info]);
	}

	public static var ctx:Context;
	public static var server:Server;

	static function run()
	{
		if (server == null)
		{
			Log.trace = handleTrace;
			server = new Server();
			ctx = new Context();
			ctx.addObject("statusmonitor", server);
			//ctx.addObject("monitor", server.session);
		}
		if (!HttpConnection.handleRequest(ctx))
			server.handleRequest();
	}


	/** Outer HTML template */

	static var DATA:Data = 
	{
		title: "Status Monitor",
		parent: "/",
		endpoint: "/monitor",
		prolog: null,
		header: null,
		content: null,
		footer: null,
		epilog: null
	};

}

