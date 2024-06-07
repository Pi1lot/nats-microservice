import asyncio
import nats

async def main():
    nc = await nats.connect("192.168.233.135:5555")

    montant_max = 10000
    async def help_request(msg):
        print(f"'{msg.subject} {msg.reply}': {msg.data.decode()}")
        montant = msg.subject.split('.')
        if int(montant[2]) < montant_max:
            resultat = {"montant":True}
            await nc.publish(msg.reply, str(resultat).encode())
        else:
            resultat = {"montant":False}
            await nc.publish(msg.reply, str(resultat).encode())


    sub = await nc.subscribe("argent.*.>", "workers", help_request)

    while True:
        await asyncio.sleep(1)

    await sub.unsubscribe()

    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())