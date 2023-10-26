# TODO: Tratar a chamada de arquivos com espaços no título, para evitar a quebra pelo espaço

from tig import Tig

class System:

    def __init__(self):
        self._tig = Tig()

    def run(self):
        while True:
            entrada = input("")
            comando, *conteudo = entrada.split(" ")
            if comando == "exit":
                break
            elif comando == "init":
                self._tig.init(*conteudo)
            elif comando == "save":
                self._tig.save(*conteudo)
            elif comando == "hist":
                self._tig.hist(*conteudo)
            elif comando == "jump":
                self._tig.jump(*conteudo)
            elif comando == "prev":
                self._tig.prev(*conteudo)
            elif comando == "diff":
                self._tig.diff(*conteudo)
            else:
                print("Invalid command")


sistema = System()
sistema.run()
