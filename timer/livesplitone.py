import eventlet
import logging
import traceback
from eventlet import websocket, wsgi
from threading import Thread

class LiveSplitOne:
  def __init__(self, host="localhost", port=8000, debug=False):
    self.debug = debug
    self.ws = None

    self.listener = eventlet.listen((host, port))
    print(f"running at ws://{host}:{port}")
    Thread(target=self._target, daemon=True).start()

  def _handler(self, env, start_response):
    @websocket.WebSocketWSGI
    def handle(ws):
      print('[connect]', ws.origin)
      self.ws = ws
      try:
        ws.wait()
      except KeyboardInterrupt:
        exit(1)
      except Exception:
        logging.error(traceback.format_exc())
      finally:
        print('[disconnect]', ws.origin)
        self.ws = None
    return handle(env, start_response)

  def _target(self):
    wsgi.server(self.listener, self._handler, log_output=False)

  def _send(self, msg, log=True):
    if log: print('[send]', msg)
    self.ws.send(msg)

  def connected(self):
    return self.ws is not None

  def start(self):
    self._send("start")

  def split(self):
    self._send("split")

  def reset(self):
    self._send("reset")

  def toggle_pause(self):
    self._send("togglepause")

  def undo(self):
    self._send("undo")

  def skip(self):
    self._send("skip")

  def init_game_time(self):
    self._send("initgametime", self.debug)

  def set_game_time(self, game_time):
    self._send(f"setgametime {game_time}", self.debug)

  def pause_game_time(self):
    self._send("pausegametime", self.debug)

  def resume_game_time(self):
    self._send("resumegametime", self.debug)
