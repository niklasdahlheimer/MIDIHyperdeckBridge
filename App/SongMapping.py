import mido

class MappingInfo:
    def __init__(self, name, msg, func):
        self.name = name
        self.msg = msg
        self.func = func

midi_channel = 9  # midi channels are 0-15
song_select_base_msg = mido.Message('song_select')
play_base_msg = mido.Message('control_change', channel=midi_channel)

# https://mido.readthedocs.io/en/latest/message_types.html?highlight=song_select#supported-messages
# https://mido.readthedocs.io/en/latest/message_types.html?highlight=song_select#parameter-types
def assign_songs_to_list(cmd_list, select_clip, play):
    cmd_list.append(
        MappingInfo('Play Command',
                    play_base_msg.copy(value=10),
                    lambda: play()))
    cmd_list.append(
        MappingInfo('Glanz und Gloria',
                    song_select_base_msg.copy(song=0),
                    lambda: select_clip(0)))
    cmd_list.append(
        MappingInfo('1000kg Konfetti',
                    song_select_base_msg.copy(song=1),
                    lambda: select_clip(1)))
    cmd_list.append(
        MappingInfo('Medley',
                    song_select_base_msg.copy(song=2),
                    lambda: select_clip(2)))
    cmd_list.append(
        MappingInfo('100.000 Stimmen',
                    song_select_base_msg.copy(song=3),
                    lambda: select_clip(3)))
    cmd_list.append(
        MappingInfo('Tanzen',
                    song_select_base_msg.copy(song=10),
                    lambda: select_clip(10)))
