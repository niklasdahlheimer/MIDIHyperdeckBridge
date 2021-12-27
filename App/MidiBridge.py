import asyncio
import logging
import mido
import SongMapping

# https://stackoverflow.com/questions/56277440/how-can-i-integrate-python-mido-and-asyncio
def make_stream():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    def callback(message):
        loop.call_soon_threadsafe(queue.put_nowait, message)

    async def stream():
        while True:
            yield await queue.get()

    return callback, stream()


class MidiBridge:
    logger = logging.getLogger(__name__)
    cmd_list = []
    callback = None

    def __init__(self, hyperdeck):
        self._hyperdeck = hyperdeck
        self.assign_songs()

    def assign_songs(self):
        select_clip_func = self._hyperdeck.select_clip_by_index
        play_func = self._hyperdeck.play
        SongMapping.assign_songs_to_list(self.cmd_list,select_clip_func,play_func)

    def set_callback(self, callback):
        self.callback = callback

    @staticmethod
    def get_inputs():
        return mido.get_input_names()

    async def connect(self, name):
        self.logger.info("try to get input messages from " + name)
        # create a callback/stream pair and pass callback to mido
        cb, stream = make_stream()
        mido.open_input(name, virtual=False, callback=cb)

        # print messages as they come just by reading from stream
        async for message in stream:
            await self.on_midi_message_receive(message)

    async def on_midi_message_receive(self, msg):
        executed = False
        for cmd in self.cmd_list:
            if cmd.msg == msg:
                executed = True
                await cmd.func()
                asyncio.create_task(self.callback("msg_received",params={'cmd':cmd.name, 'message': str(msg)}))

        if not executed:
            asyncio.create_task(self.callback("msg_received", params={'cmd': "no command found",'message':str(msg)}))
