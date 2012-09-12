package com.dotmpe.statusmonitor;

import js.Lib;
import js.Dom;
import haxe.remoting.AsyncProxy;
import haxe.remoting.AsyncConnection;
import haxe.remoting.HttpAsyncConnection;


class Client
{
	public static var server:_Session;
	public static var cnx:AsyncConnection;

	public static function connect(endpoint:String)
	{
		// make async connection
		cnx = HttpAsyncConnection.urlConnect(endpoint + ".n");
		cnx.setErrorHandler(function(e){ trace(e); });
		trace("Connected to " + endpoint);

		// access shared xu88 Session instance by proxy
		server = new _Session(cnx.xu88);

//		trace("New session for " + server.x_account());//accountid);
	}

	public static function onLoad(evt:Event):Void
	{
		trace(evt);
		if (cnx == null)
		{
			trace("Initializing StatusMonitor client..");
			var endpoint:String;
//			var args = Web.getParams();
//			if (args.exists("endpoint"))
//				endpoint = args.get("endpoint");
//			else
//				endpoint = Sandpit.URI;
//
//			connect(endpoint);
			trace("Sandpit front-end initalization done.");
		}	
	}

	public static function onData(data:Dynamic)
	{
		trace(data);
	}

	public static function main():Void
	{
		Lib.window.onload = onLoad;
	}
}

private class _Session extends AsyncProxy<com.dotmpe.statusmonitor.Monitor>
//	implements scrow.xu88.ISession
{}

