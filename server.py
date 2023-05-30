import asyncio
import sqlite3
import sqlquery
import websockets 
import pathlib
import ssl

conn = sqlite3.connect("data.db")
c = conn.cursor()
console = sqlquery.sql()
#console.get(1685335865, 1685335870, "temp")


# create handler for each connection

async def handler(websocket, path):
    while True:
        command = await websocket.recv()
        print(command)
        #data pipe and satellite communication protocol is still not known
        start_time_str = await websocket.recv()
        start_time=int(start_time_str)
        print(start_time)
        end_time_str = await websocket.recv()
        end_time=int(end_time_str)
        print(end_time)
        data_type = await websocket.recv()
        print(data_type)
        #await websocket.send("done")
        await websocket.send(console.get(start_time, end_time, data_type))

 
#security
localhost_pem = pathlib.Path(__file__).with_name("private.pem")
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(localhost_pem)
 
start_server = websockets.serve(handler, "localhost", 8000, ssl=ssl_context)
 
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()