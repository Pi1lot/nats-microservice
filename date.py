import asyncio
import nats
import time
async def main():
    nc = await nats.connect("192.168.233.135:5555")

    timestamp = time.time()
    async def help_request(msg):
        print(f"'{msg.subject} {msg.reply}': {msg.data.decode()}")
        date = msg.subject.split('.')
        if int(date[3]) > timestamp - 3600*24*10:
            resultat = {"date":True}
            await nc.publish(msg.reply, str(resultat).encode())
        else:
            resultat = {"date":False}
            await nc.publish(msg.reply, str(resultat).encode())


    sub = await nc.subscribe("argent.*.*.>", "workers", help_request)

    while True:
        await asyncio.sleep(1)

    await sub.unsubscribe()

    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())