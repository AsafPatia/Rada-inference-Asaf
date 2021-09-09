import logging
import threading
import typing
import asyncio
import pickle

logger = logging.getLogger(__name__)


class BMAsyncSocket(threading.Thread):
    server: asyncio.AbstractServer
    handle_message_received_callback: typing.Callable
    host: str
    port: int

    def __init__(self, host: str, port: int, callback: typing.Callable):
        super(BMAsyncSocket, self).__init__()
        self.daemon = True
        self.cancelled = False
        self.handle_message_received_callback = callback
        self.host = host
        self.port = port

    def run(self):
        while not self.cancelled:
            self.listen(self.host, self.port)

    def cancel(self):
        self.cancelled = True
        self.server.close()

    async def handle_client(self, reader, writer):
        # request = (await reader.read()).decode('utf8')
        request = pickle.loads((await reader.read()))
        print('Server received', request)
        self.handle_message_received_callback(request)

    async def run_server(self, host, port):
        self.server = await asyncio.start_server(self.handle_client, host, port)
        adder = self.server.sockets[0].getsockname()
        logger.info(f'Socket now listening on {adder}')
        # logger.info('Socket now listening on ' + host + ":" + str(port))
        # print(f'Socket now listening on {adder}' + host + ":" + str(port))
        async with self.server:
            await self.server.serve_forever()

    def listen(self, host, port):
        asyncio.run(self.run_server(host, port))

    def stop(self):
        self.cancel()

    @staticmethod
    def send_msg(client, port, msg):
        async def send(_client, _port, _msg):
            try:
                reader, writer = await asyncio.open_connection(_client, _port)
            except OSError as e:
                logger.error('Error while connecting to upstream: %s', e)
                # print('Error while connecting to upstream:', e)
                return
            try:
                writer.write(_msg)
                await writer.drain()
                writer.close()
            except OSError as e:
                logger.error('Error while writing to upstream: %s', e)
                # print('Error while writing to upstream:', e)
                return

        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coroutine = send(client, port, msg)
        loop.run_until_complete(coroutine)
