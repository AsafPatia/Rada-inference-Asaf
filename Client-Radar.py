import asyncio
import config.settings as setting
import pickle
import time

sample1 = [2, 2021, 8, 25, 19, 2, 4, 100.0, 0, 150, 1, 1, 1, 1, 200, 2, 2, 2]
sample2 = [3, 2021, 8, 25, 19, 2, 4, 100.3, 0, 155, 1, 2, 3, 1, 258, 7, 6, 7, 2, 79, 1, 2, 1]
sample3 = [2, 2021, 8, 25, 19, 2, 4, 100.5, 0, 159, 1, 4, 7, 2, 298, 2, 2, 2]
sample = "asaf"


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(setting.settings.host_ip, setting.settings.host_port)
    # data_string = pickle.dumps(sample1)

    print(f'Send: {message!r}')
    # writer.write(message)

    writer.write(pickle.dumps(message))
    await writer.drain()

    # data = await reader.read()
    # print(f'Received: {data.decode()!r}')
    #
    # print('Close the connection')
    # writer.close()
    # await writer.wait_closed()

    # request = pickle.loads((await reader.read()))
    # print('Server received', request)

    # data = await reader.read()
    # message = data.decode()
    # print(message)

    print('Close the connection')
    writer.close()
    # data = await reader.read()  # should read until end of msg
    # print(f'Received: {data.decode()!r}')
    #
    # print('Close the connection')
    # writer.close()
    # await writer.wait_closed()




# asyncio.run(tcp_echo_client(sample1))
asyncio.run(tcp_echo_client(sample2))
# asyncio.run(tcp_echo_client(sample3))