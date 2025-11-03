import asyncio
import websockets
import argparse

# {websocket: {"id": str, "is_source": bool}}
clients = {}

async def relay(websocket):
    # Assign a unique ID to the client
    client_id = id(websocket)
    clients[websocket] = {"id": client_id, "is_source": False}
    print(f"New client connected (ID: {client_id}). Total clients: {len(clients)}")

    try:
        async for message in websocket:
            message_str = message.strip()
            print(f"Received from client {client_id}: {message_str}")

            # Check if the message marks the client as the data source
            if message_str == "notrenji":
                clients[websocket]["is_source"] = True
                print(f"Client {client_id} is now marked as the data source.")
                await websocket.send(f"ACK: You are now the data source (ID: {client_id}).")
                continue

            # Relay the message to all receivers (non-source clients)
            for client, info in clients.items():
                if client != websocket and not info["is_source"]:
                    await client.send(message_str)
                    print(f"Relayed to receiver {info['id']}: {message_str}")

    finally:
        del clients[websocket]
        print(f"Client {client_id} disconnected. Total clients: {len(clients)}")

async def run_server(host, port):
    try:
        async with websockets.serve(relay, host, port) as server:
            print(f"Texthooker proxy server running at ws://{host}:{port}")
            print("Clients sending 'notrenji' will be marked as the data source.")
            await server.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"Error: Address {host}:{port} is already in use.")
        else:
            print(f"Server error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Texthooker relay proxy server.")
    parser.add_argument(
        "--port",
        type=int,
        default=6677,
        help="Port number for the websocket server (default: 6677)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host of the websocket server (default: localhost)"
    )
    args = parser.parse_args()

    asyncio.run(run_server(args.host, args.port))

if __name__ == "__main__":
    main()
