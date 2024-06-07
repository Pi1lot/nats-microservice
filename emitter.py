import asyncio
import nats
from nats.errors import TimeoutError
import time

async def main():
    nc = await nats.connect("192.168.233.135:5555")

    date =  int(time.time()) - 3600*24*11 #Pour tester une date antérieur à 10 jours

    print(date)
    try:
        response = await nc.request(f"argent.11111111.950.{date}", b'Virement', timeout=50)
        print("Réponse {message}".format(
            message=response.data.decode()))
    except TimeoutError:
        print("Request timed out")

    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())