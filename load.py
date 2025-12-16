import tkinter as tk
from EDMCLogging import get_plugin_logger
from l10n import translations as tr
import functools
import os

from typing import Optional, Tuple, Dict, Any

plugin_name = "FuelStatus"
logger = get_plugin_logger(f'{plugin_name}')

_ = functools.partial(tr.tl, context=os.path.dirname(__file__))

label: Optional[tk.Label]
status: Optional[tk.Label]

main_tank: Optional[float] = None
reservoir: Optional[float] = None

def plugin_start3(plugin_dir: str) -> str:
  logger.debug('fuelstatus plugin loaded')
  return plugin_name

def plugin_stop() -> None:
  pass

def prefs_changed(cmdr: str, is_beta: bool) -> None:
  update_status()

def plugin_app(parent) -> Tuple[tk.Label,tk.Label]:
  global label, status
  label = tk.Label(parent, text="")
  status = tk.Label(parent, text="")
  update_status()
  return label, status

def dashboard_entry(cmdr: str, is_beta: bool, entry: Dict[str, Any]) -> None:
  global main_tank, reservoir
  main_tank = None
  reservoir = None
  if "Fuel" in entry:
    if "FuelMain" in entry["Fuel"]:
      main_tank = entry["Fuel"]["FuelMain"]
    if "FuelReservoir" in entry["Fuel"]:
      reservoir = entry["Fuel"]["FuelReservoir"]
  update_status()

def update_status() -> None:
  global label, status
  label["text"] = f'{_("Fuel levels")}:'
  if main_tank is None or reservoir is None:
    if main_tank is None and reservoir is None:
      status["text"] = _("waiting for data …")
    else:
      # maybe add error handling for this weird edge case, should it ever exist …
      status["text"] = _("ERROR")
      logger.error("One of main tank and reservoir fuel levels is None, the other isn’t … WTF?")
  else:
    status["text"] = f'{round(main_tank,3)} t ({_("main")}), {round(reservoir,3)} t ({_("reservoir")})'
