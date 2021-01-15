import blinker

status_message = blinker.Signal()
action_command = blinker.Signal()
action_singlecommand = blinker.Signal()
delayed_signal = blinker.Signal()
focus = blinker.Signal()
execute = blinker.Signal()
