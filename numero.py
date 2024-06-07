import asyncio
import nats

async def main():
    nc = await nats.connect("192.168.233.135:5555")

    liste_compte = ['11223344','77889900','11111111','44554455']
    async def help_request(msg):
        print(f"'{msg.subject} {msg.reply}': {msg.data.decode()}")
        compte = msg.subject.split('.')
        if compte[1] in liste_compte:
            resultat = {"compte":True}
            await nc.publish(msg.reply, str(resultat).encode())
        else:
            resultat = {"compte":False}
            await nc.publish(msg.reply, str(resultat).encode())


    sub = await nc.subscribe("argent.>", "workers", help_request)

    while True:
        await asyncio.sleep(1)

    await sub.unsubscribe()

    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())