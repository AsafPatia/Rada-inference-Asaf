import asyncio
import json
import logging
import pickle
import socketserver
import threading
from datetime import datetime
from collections import defaultdict
import random
from utils.CLI import handle_cli
from config.settings import settings
from utils.BMAsyncSocket import BMAsyncSocket
from config.logging_config import init as init_logger
import time
import sys
import pandas as pd
import socket

init_logger()
logger = logging.getLogger(__name__)
Input_Data = dict()
OutPut_Data = dict()
curr_Time = 0
# ========================================== start Added Here =============================
sample1 = [2, 2021, 8, 25, 19, 2, 4, 100.0, 0, 150, 1, 1, 1, 1, 200, 2, 2, 2]
sample2 = [3, 2021, 8, 25, 19, 2, 4, 100.3, 0, 155, 1, 2, 3, 1, 258, 7, 6, 7, 2, 79, 1, 2, 1]
sample3 = [2, 2021, 8, 25, 19, 2, 4, 100.5, 0, 159, 1, 4, 7, 2, 298, 2, 2, 2]


# class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         data_string = self.request.recv(1024)
#         data = pickle.loads(data_string)
#         print("Server Received:", data)
#         handle_message_received(data)
#         print(Input_Data)
#         # cur_thread = threading.main_thread()
#         # response = bytes("{}: {}".format(cur_thread.name, data), "ascii")
#         # self.request.sendall(response)
#
#
# class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass


def client(ip, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.send(pickle.dumps(data))
        sock.close()
        # response = str(sock.recv(1024), "ascii")
        # print("Client Received: {}".format(response))


async def client1(message):
    reader, writer = await asyncio.open_connection(settings.host_ip, settings.host_port)
    print(f'Send: {message!r}')
    writer.write(pickle.dumps(message))
    await writer.drain()
    writer.close()

# ========================================== End Added Here =============================

# TODO: check if we need to keep only the last predictions or a history of more than one
predictions = defaultdict(dict)
plots_sliding_window = defaultdict(dict)


def bm_radar_target_classification(argv):
    logger.info("Starting...")
    read_cli_values(argv)
    start_listening()
    start_inferences()


def read_cli_values(argv):
    handle_cli(argv)
    print('BMRadarTargetClassification starting with the following parameters:')
    print('host {', settings.host_ip, ":", settings.host_port,
          '} ; client {', settings.client_ip, ":", settings.client_port, '}', sep='')
    print('unknown_prediction_code {', settings.unknown_prediction_code,
          '} ; drone_prediction_code {', settings.drone_prediction_code, '}', sep='')
    print('idle_track_purging_frequency {', settings.idle_track_purging_frequency,
          '} ; plot_sliding_window_size {', settings.plot_sliding_window_size, '}', sep='')


# def start_listening():
#     logger.debug("start_listening()")
#     HOST, PORT = settings.host_ip, settings.host_port
#     server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
#     with server:
#         ip, port = server.server_address
#
#         # Start a thread with the server -- that thread will then start one
#         # more thread for each request
#         server_thread = threading.Thread(target=server.serve_forever)
#         # Exit the server thread when the main thread terminates
#         server_thread.daemon = True
#         server_thread.start()
#         print("Server loop running in thread:", server_thread.name)
#         client(ip, port, sample1)
#         server_thread.join()
#         print("Server Shoutdown")
#         server.shutdown()


def start_listening():
    logger.debug("start_listening()")
    sock = BMAsyncSocket(settings.host_ip, settings.host_port, handle_message_received)
    sock.start()
    asyncio.run(client1(sample1))
    asyncio.run(client1(sample2))
    asyncio.run(client1(sample3))
    sock.stop()
    print("\n\n\n")
    print("Input Data So Far:")
    print(Input_Data)


def handle_message_received(data):
    # TODO: Priority 1 - insert new data to Plots data structure and delete from tail based on settings.plot_sliding_window_size
    # TODO: Match the function to its true input
    # TODO: for now, the function del prev rows based on number of rows -> need to change it to 'time' of rows

    """
    :param data: the massage_received
    :return:
    LenOfInformation is the numbers of cells is the sample for each trackID
    StartIndexOfInfoOfTrackID is the index that the information of the TrackID is starting
    limit of how many rows at each dataFrame for each TrackID
    """

    number_Of_Tracks = data[0]
    len_Of_Information_Per_TrackID = 5
    index_Start_Of_Info_Of_TrackID = 8
    index_Start_Of_Basic_Information = 1
    Columns = ["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND", "MASSAGE_LENGHT",
               "TRACK_ID", "AZIMUTH", "POS_UP", "POS_NOTRH", "POS_WEST"]
    for i in range(0, number_Of_Tracks):
        Data_Frame_Array = []

        # copy the Basic information
        for j in range(index_Start_Of_Basic_Information, index_Start_Of_Info_Of_TrackID):
            Data_Frame_Array.append(data[j])

        # copy the information of the i'th trackID
        start_Index = (len_Of_Information_Per_TrackID * i) + (j + 1)
        for k in range(start_Index, len_Of_Information_Per_TrackID + start_Index):
            Data_Frame_Array.append(data[k])

        # create a row and insert it to the DateFrame
        # key_Index is where the index of the TrackID
        key_Index = start_Index
        new_Data_Frame = pd.DataFrame([Data_Frame_Array], columns=Columns)
        if data[key_Index] not in Input_Data.keys():
            Input_Data[data[key_Index]] = new_Data_Frame
        else:

            Input_Data[data[key_Index]] = \
                Input_Data[data[key_Index]].append(new_Data_Frame, ignore_index=True)
            # delete rows from the trackID, if
            if Input_Data[data[key_Index]].tail(1).index.item() > (settings.plot_sliding_window_size - 1):
                Input_Data[data[key_Index]] = \
                    Input_Data[data[key_Index]].drop(Input_Data[data[key_Index]].index[[0]])
                Input_Data[data[key_Index]] = Input_Data[data[key_Index]].reset_index()


def start_inferences():
    # schedule inferences
    inference_frequency: float = 0.5
    try:
        while 1:
            time.sleep(inference_frequency)
            # inference_input = prepare_data_for_inference()
            # inference_output = run_inference(inference_input)
            run_inference()
            # update_predictions(inference_output)
            send_predictions()
            # purge_idle_tracks()
            break
    except KeyboardInterrupt:
        logger.info("Execution aborted by client")
        pass


def run_inference():
    # TODO: remove this mock and integrate real algorithm

    # inference_output = defaultdict(list)
    for key in Input_Data.keys():
        OutPut_Data[key] = {'Prediction': random.randint(0, 1), 'Confidence': random.uniform(0.43, 1.0),
                            'LastUpdateTS': random.randint(100, 200)}
# async def handle_client1(reader, writer):
#     request = (await reader.read(1024)).decode('utf8')  # should read until end of msg
#     print(request)
#
#     response = "thx"
#     writer.write(response.encode('utf8'))
#     await writer.drain()
#     writer.close()
# send predictions to client


def send_predictions():
    # TODO: encode data into binary structure as described in design document
    data = ""
    for key, val in OutPut_Data.items():
        data += "index:" + str(key) + \
                " Prediction:" + str(val['Prediction']) + \
                " Confidence:" + str(val['Confidence']) + \
                " LastUpdateTS:" + str(val['LastUpdateTS']) + '\n'

    # loop = asyncio.get_event_loop()
    # loop.create_task(asyncio.start_server(handle_client1, settings.client_ip, settings.client_port))
    # loop.run_forever()
    BMAsyncSocket.send_msg(settings.client_ip, 7034, data.encode())


# ===================================== Currently unused ===========================================
# prepare data for inference
def prepare_data_for_inference():
    # TODO: read data from plots and prepare it as input for inference - preferably minimum CPU time here

    # TODO: remove this section - generating some random data for testing
    inference_input = defaultdict(list)

    for i in range(10):
        track_id = random.randrange(20001, 99000)
        inference_input[track_id].append({})

    return inference_input


# ===================================== Currently unused ===========================================
# update predictions with inference results
def update_predictions(data):
    # TODO: Priority 1 - update predictions with inference results
    # TODO: Understand from a research team exactly what the data is going to look like
    """
    the Post_Proc_Dict is a Dictionary that each key is a trackID and for each trackID there is an Array
    that looks like this:
    Array[0] = trackID
    Array[1] = prediction
    Array[2] = confidence
    :param data: Assuming data is an Array that:
    data[0] -> trackID
    data[1] -> prediction
    data[2] -> confidence
    :return:
    """
    trackID = data[0]
    prediction = data[1]
    confidence = data[2]
    to_Insert_Array = [trackID, prediction, confidence]
    OutPut_Data[trackID] = to_Insert_Array


# ===================================== Currently unused ===========================================
# purge idle tracks
def purge_idle_tracks():
    # TODO: ask Lyudmyla if its ok to assume that Time is determined by the last income of the trackID
    # TODO: change the function, it Suitable for the dataframe input
    """
    In order to match Time we will multiply by 10 ^ -6 the pro_Time

    :return:
    """
    global curr_Time
    idle_Time_In_Seconds = settings.idle_track_purging_frequency
    idle_Time_In_MicroSeconds = idle_Time_In_Seconds * pow(10, 6)

    for trackID in list(Input_Data.keys()):
        trackID_Last_Insert = Input_Data[trackID][1]
        if curr_Time - trackID_Last_Insert > idle_Time_In_MicroSeconds:
            Input_Data.pop(trackID)


def main(argv):
    bm_radar_target_classification(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
