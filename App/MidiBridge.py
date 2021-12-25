import logging

import mido

midi_channel = 9  # midi channels are 0-15
base_msg = mido.Message('control_change', channel=midi_channel)


class mapping_info:
    def __init__(self, name, msg, func):
        self.name = name
        self.msg = msg
        self.func = func


# creating list


# We can also access instances attributes
# as list[0].name, list[0].roll and so on.

class MidiBridge:
    logger = logging.getLogger(__name__)
    cmd_list = []
    callback = None

    def __init__(self, hyperdeck):
        self._hyperdeck = hyperdeck
        self.assignSongs()

    def assignSongs(self):
        select_clip = self._hyperdeck.select_clip_by_index
        play = self._hyperdeck.play

        self.cmd_list.append(
            mapping_info('Play Command',
                         base_msg.copy(value=10),
                         lambda: play()))
        self.cmd_list.append(
            mapping_info('Glanz und Gloria Select',
                         base_msg.copy(value=10),
                         lambda: select_clip(1)))
        self.cmd_list.append(
            mapping_info('Glanz und Gloria Play',
                         base_msg.copy(value=10),
                         lambda: select_clip(1)))
        self.cmd_list.append(
            mapping_info('1000kg Konfetti',
                         base_msg.copy(value=20),
                         lambda: select_clip(1)))
        self.cmd_list.append(
            mapping_info('Medley',
                         base_msg.copy(value=30),
                         lambda: select_clip(1)))
        self.cmd_list.append(
            mapping_info('100.000 Stimmen',
                         base_msg.copy(value=40),
                         lambda: select_clip(1)))
        self.cmd_list.append(
            mapping_info('Tanzen',
                         base_msg.copy(value=50),
                         lambda: select_clip(1)))

    def set_callback(self, callback):
        self.callback = callback

    def get_inputs(self):
        return mido.get_input_names()

    def connect(self, name):
        self.logger.info("try to get input messages from " + name)
        mido.open_input(name, virtual=False, callback=self.on_midi_message_receive)

    def on_midi_message_receive(self, msg):
        self.logger.info("received msg!")
        print(msg)
        executed = False
        for cmd in self.cmd_list:
            if cmd.msg == msg:
                executed = True
                cmd.func()
                self.callback.on_midi_msg_received(cmd.name)

        if not executed:
            print("no command found for", msg)
            self.callback("msg_received", params={'text': "no command found for" + msg})
