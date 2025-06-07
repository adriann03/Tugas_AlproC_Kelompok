
import os
loggedInIndex = -1
class Scene:
    def __init__(self, name, scene, cfg={}):
        self.name = name
        self.scene = scene
        self.cfg = cfg
    def show(self):
        global loggedInIndex # Declare loggedInIndex as global for the entire method
        os.system("cls")
        excludedPrintFirstScene = ["menu", "confirmwithdraw", "success", "balance"]
        if self.name not in excludedPrintFirstScene:
            print(self.scene)
        if self.name == "main":
            loggedInIndex = -1 # Now correctly modifies the global
            idList = []
            for x in clients:
                idList.append(x.id)
            while True:
                x = input("ID: ")
                if x in idList:
                    chosenID = idList.index(x)
                    loggedInIndex = chosenID # Now correctly modifies the global
                    changeScene("enterpin", {"pin": clients[chosenID].pin})
                    break
                else:
                    print("Invalid ID")
        elif self.name == "enterpin":
            trials = 3
            while True:
                x = input("PIN: ")
                if x == self.cfg.get("pin"):
                    changeScene("menu")
                    break
                else:
                    trials -= 1
                    if trials == 0:
                        loggedInIndex = -1 # Now correctly modifies the global
                        changeScene("main")
                        break
                    print("Invalid PIN. " + str(trials) + " percobaan tersisa")
        elif self.name == "menu":
            newScene = self.scene.format(client_name=clients[loggedInIndex].name)
            print(newScene)
            while True:
                x = input("Pilihan: ")
                fixedWDs  = ["1", "2", "3", "4"]
                WDAmounts = [1e5, 2.5e5, 5e5, 1e6]
                if x in fixedWDs:
                    if clients[loggedInIndex].balance - WDAmounts[fixedWDs.index(x)] < 0:
                        print("Saldo tidak mencukupi")
                    else:
                        # clients[loggedInIndex].subBal(WDAmounts[fixedWDs.index(x)])
                        changeScene("confirmwithdraw", {"WDAmt": WDAmounts[fixedWDs.index(x)]})
                        break
                elif x == "5":
                    amount = float(input("Nominal: "))
                    if amount < 5e4:
                        print("Nominal terlalu kecil")
                    elif clients[loggedInIndex].balance - amount < 0:
                        print("Saldo tidak mencukupi")
                    else:
                        # clients[loggedInIndex].subBal(amount)
                        changeScene("confirmwithdraw", {"WDAmt": amount})
                        break
                elif x == "6":
                    changeScene("othermenu")
                    break
                else:
                    break
        elif self.name == "success":
            overwriteUsersTxt()
            bal = f"{self.cfg.get("bal"):,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
            newScene = self.scene.format(balance=bal)
            print(newScene)
            while True:
                x = input("Y/N: ").upper()
                if x == "Y":
                    changeScene("menu")
                    break
                elif x == "N":
                    changeScene("main")
                    break
                else:
                    print("Invalid input")
        elif self.name == "confirmwithdraw":
            amount = self.cfg.get("WDAmt")
            num = f"{self.cfg.get("WDAmt"):,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
            newScene = self.scene.format(amount=num)
            print(newScene)
            while True:
                x = input("Y/N: ").upper()
                if x == "Y":
                    clients[loggedInIndex].subBal(amount)
                    changeScene("success", {"bal": float(clients[loggedInIndex].balance)})
                    break
                elif x == "N":
                    changeScene("menu")
                    break
                else:
                    print("Invalid input")
        elif self.name == "othermenu":
            while True:
                x = input("Pilihan: ")
                if x == "1":
                    changeScene("balance", {"bal": float(clients[loggedInIndex].balance)})
                    break
                elif x == "2":
                    changeScene("enteroldpin")
                    break
                elif x == "3":
                    break
                else:
                    print("Invalid input")
        elif self.name == "balance":
            bal = f"{self.cfg.get("bal"):,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
            newScene = self.scene.format(balance=bal)
            print(newScene)
            while True:
                x = input("Y/N: ").upper()
                if x == "Y":
                    changeScene("menu")
                    break
                elif x == "N":
                    changeScene("main")
                    break
                else:
                    print("Invalid input")
        elif self.name == "enteroldpin":
            trials = 3
            while True:
                x = input("PIN: ")
                if x == clients[loggedInIndex].pin:
                    changeScene("enternewpin")
                    break
                else:
                    trials -= 1
                    if trials == 0:
                        loggedInIndex = -1 # Now correctly modifies the global
                        changeScene("main")
                        break
                    print("Invalid PIN. " + str(trials) + " percobaan tersisa")
        elif self.name == "enternewpin":
            while True:
                x = input("PIN: ")
                print("", end="\r")
                y = input("Konfirmasi PIN: ")
                if x == y:
                    clients[loggedInIndex].changePin(x)
                    changeScene("changepinsuccess")
                    break
                else:
                    print("PIN tidak sama")
        elif self.name == "changepinsuccess":
            overwriteUsersTxt()
            while True:
                x = input("Y/N: ").upper()
                if x == "Y":
                    changeScene("menu")
                    break
                elif x == "N":
                    changeScene("main")
                    break


            


            

def changeScene(name, cfg={}):
    l = []
    for x in scenes:
        l.append(x.name)
    try:
        chosen = l.index(name)
        scenes[chosen].cfg = cfg
        scenes[chosen].show()
        # print(clients[0].id, type(clients[0].id))
    except ValueError:
        print("Scene " + str(name) + " does not exist")

scenes = [
    Scene("main", """
\t\t\tSelamat Datang di Bank VENA
\t\t\tSilahkan masukkan ID
    """),
    Scene("enterpin", """
\t\t\tMasukkan PIN anda
\t\t\t
    """),
    Scene("enteroldpin", """
\t\t\tMasukkan PIN lama anda
\t\t\t
    """),
    Scene("enternewpin", """
\t\t\tMasukkan PIN baru anda
\t\t\t
    """),
    Scene("menu", """
\t\t\tSugeng Rawuh, {client_name}
\t\t\tPilihan menu
1 => Tarik Rp100.000
2 => Tarik Rp250.000
3 => Tarik Rp500.000
4 => Tarik Rp1.000.000
5 => Tarik custom (min Rp50.000)
6 => Lainnya
7 => Keluar          
    """),
    Scene("othermenu", """
1. Cek Saldo
2. Ubah PIN
3. Transfer
"""),
    Scene("balance", """
\t\t\tSisa saldo: Rp{balance}
\t\t\tIngin transaksi lagi? (Y/N)
"""),
    Scene("success", """
\t\t\tTransaksi sudah berhasil
\t\t\tSisa saldo: Rp{balance}
\t\t\tIngin transaksi lagi? (Y/N)
    """),
    Scene("changepinsuccess", """
\t\t\tPIN berhasil diubah
\t\t\tIngin transaksi lagi? (Y/N)
"""),
    Scene("confirmwithdraw", """
\t\t\tAnda akan melakukan penarikan sebesar Rp{amount}
\t\t
\t\t\tKonfirmasi? (Y/N)
    """)
]

class Client:
    def __init__(self, id, name, pin, balance):
        self.id = id
        self.name = name
        self.pin = pin
        self.balance = balance
    def __str__(self):
        return f"Client(ID: {self.id}, Name: {self.name}, PIN: {self.pin}, Bal: {self.balance})"
    def changePin(self, newPin):
        self.pin = newPin
    def addBal(self, amount):
        self.balance += amount
    def subBal(self, amount):
        if self.balance - amount < 0:
            print("no")
        else:
            self.balance -= amount
clients = []
def overwriteUsersTxt():
    lines = []
    for x in clients:
        lines.append(f"{x.id};{x.name};{x.pin};{x.balance}")
    with open("users.txt", "w") as f:
        f.write("\n".join(lines))
with open("users.txt", "r") as f:
    for line in f.readlines():
        line2 = line.strip().split(";")
        clients.append(
            Client(
                line2[0],
                line2[1],
                line2[2],
                float(line2[3]),
            )
        )
        # print(line.strip())

changeScene("main")