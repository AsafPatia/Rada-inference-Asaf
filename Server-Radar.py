import asyncio


async def handle_client(reader, writer):
    request = (await reader.read(1024)).decode('utf8')  # should read until end of msg
    print(request)


loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, '127.0.0.1', 7034))
loop.run_forever()
