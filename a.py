#VARIAVEIS

QtdFrutas = {
    "Laranja": 10,
    "Banana": 15,
    "Melancia": 5
}

ValoresFrutas = {
    "Laranja": 1.5,
    "Banana": 0.5,
    "Melancia": 3.0
}

Pedidos = {
    "João": ("Banana", 5),
    "Maria": ("Melancia", 1),
    "Carlos": ("Laranja", 5)
}

#PRINT

print(f"Frutas restantes:")
#Printa as frutas restantes

for fruta, qtd in QtdFrutas.items():
    print(f"{fruta}: {qtd}.")

print(f"...")
print(f"Pedidos:")
#Printa os pedidos que teve

for nome, (fruta, qtd) in Pedidos.items():
    qtdsuficiente = False

    frutasrestantes = QtdFrutas.get(fruta, 0)
    frutasuficiente = frutasrestantes - qtd

    if frutasuficiente >= 0: 
        qtdsuficiente = True
    else:
        qtdsuficiente = False

    #Dai só apliquei com continha basica de >= e o frutasuficiente

    precoporfruta = ValoresFrutas.get(fruta, 0)
    precofinal = qtd * precoporfruta

    print(f"Nome: {nome}, Pedido: {fruta}, Quantidade: {qtd}, Preço total: R$ {precofinal}.")
    print(f"Quantidade de frutas restantes é suficiente para o pedido?")
    if qtdsuficiente == True:
        print(f"Sim.")
    else:
        print(f"Não.")
    #Depois so printa tudo e mostra se tem qtd suficiente pra pedido

print(f"...")

#DEPOIS DE FINALIZADO

#Quantidade restante depois de fazer os pedidos
print(f"Após os pedidos finalizados, a quantidade restante de frutas é:")
for nome, (fruta, qtd) in Pedidos.items():
    if fruta in QtdFrutas:
        QtdFrutas[fruta] -= qtd

for fruta, qtd in QtdFrutas.items():
    print(f"{fruta}: {qtd}")

print(f"...")

#VENDEDORES

#VENDEDORES TRABALHANDO
Vendedores = [
    "Leandro",
    "Fernando"
]

RegistroDeVendedores = Vendedores

SistemaUtilizado = "Registro de Vendedores Epac"

print(f"Vendedores: {Vendedores}")
print(f"Vendedores registrados: {RegistroDeVendedores}")
print(f"...")

#VENDEDOR NOVO ADMITIDO
AdmissãoDeVendedores = Vendedores.append("Gabriel")
print(f"Vendedor admitido")
print(f"Vendedores agora: {Vendedores}")

#REGISTRO DE VENDEDOR MUDA
print(f"Vendedores registrados agora: {RegistroDeVendedores}")

print(f"...")
#VENDEDOR NOVO ADMITIDO MANUALMENTE
SistemaUtilizadoManual = "Registro de Vendedores fisico em pastas"

RegistroDeVendedores = [
    "Leandro",
    "Fernando",
    "Gabriel",
    "Gustavo"
]

print(f"Vendedor admitido no registro")
print(f"Vendedores registrados agora: {RegistroDeVendedores}")
print(f"...")

if Vendedores == RegistroDeVendedores:
    print(f"Os vendedores são os mesmos que no registro.")
else:
    print(f"Os vendedores não são os mesmos que no registro.")

if SistemaUtilizado is SistemaUtilizadoManual:
    print("Os vendedores e vendedores registrados foram feitos no mesmo lugar.")
else:
    print("Os vendedores e vendedores registrados não foram feitos no mesmo lugar.")

print(f"...")