import asyncio

class Processador:
    def __init__(self, produtos, broadcast_func):
        self.produtos = produtos
        self.broadcast = broadcast_func
        self.is_processing = False
        self.is_paused = False

    async def iniciar(self):
        if self.is_processing:
            return

        self.is_processing = True
        self.is_paused = False

        for produto in self.produtos:
            while self.is_paused:
                await asyncio.sleep(0.5)

            if not self.is_processing:
                break

            produto["status"] = "Processando"
            produto["detalhes"] = "Iniciando análise..."
            await self.broadcast({"action": "update", "produto": produto})
            await asyncio.sleep(2)

            produto["status"] = "Atualizando no Bling"
            produto["detalhes"] = "Enviando dados corrigidos..."
            await self.broadcast({"action": "update", "produto": produto})
            await asyncio.sleep(2)

            produto["status"] = "Concluído"
            produto["detalhes"] = "Produto atualizado com sucesso."
            await self.broadcast({"action": "update", "produto": produto})

        self.is_processing = False
        await self.broadcast({"action": "finished"})

    def pausar(self):
        self.is_paused = True

    def continuar(self):
        self.is_paused = False

    def parar(self):
        self.is_processing = False
        self.is_paused = False
