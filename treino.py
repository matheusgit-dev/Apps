#Imports
import math
import time

#Variaveis
name = "Matheus"
age = 17
height = 1.75
number1 = 67
number2 = 69

#Holders
numbers = {
    "1": number1,
    "2": number2
}

me = {
    "name": name,
    "age": age,
    "height": height,
}

#Base
print("Antes: ", me)

time.sleep(3)

#Contas (math)

contas = {
    "conta1": numbers["1"] + numbers["2"],
    "conta2": numbers["1"] - numbers["2"],
    "conta3": numbers["1"] * numbers["2"],
    "conta4": numbers["1"] / numbers["2"],
    "conta5": numbers["1"] // numbers["2"],
    "conta6": numbers["1"] % numbers["2"],
    "conta7": numbers["1"] ** 2,
    "conta8": numbers["2"] ** 2,
    "conta9": math.sqrt(numbers["1"]),
    "conta10": math.sqrt(numbers["2"]),
    "conta11": numbers["1"] ** 0.5,
    "conta12": numbers["2"] ** 0.5
}

for chave, valor in contas.items():
    print(chave, valor)

time.sleep(3)

#Tipos (types)
for chave, valor in me.items():
    print(chave, valor, type(valor))

#Obs: não eu não usei outra IA pra fazer kk, eu so fui no forum e fiquei olhando como fazia, eu também fiz no vscode, algumas coisas ele mesmo explica como funciona e como arrumar 
#Eu fiz assim pra ter mais movimentação e organização, afinal se eu for mecher com os trem fica mais facil ne, igual no print das contas e os tipos, é como dev de verdade costuma fazer
#Literal é um monte de função num código (funções organizadas, nada mal feito) e depois so chama num negocinho véi besta, eu faço muito isso no roblox tlgd