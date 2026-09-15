# Controle de Gastos Pessoais — Regra 50/30/20

import json  # biblioteca para salvar e ler dados em arquivo JSON

# categorias organizadas por grupo
categorias = {
    "Necessidades": ["Alimentação", "Contas a Pagar", "Transporte"],
    "Desejos": ["Gastos pessoais"],
    "Investimentos": ["Investimentos"]
}

# Lista que vai gurdar todos os gastos
gastos = []

# Variavel que vai guardar o salario
salario = 0.0

def carregar_dados():
    global gastos, salario  # avisa que vai alterar as variáveis globais

    try:
        with open("dados_gastos.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)   # carrega os dados do arquivo JSON
            gastos = dados["gastos"]     # carrega a lista de gastos
            salario = dados["salario"]  # carrega o salário
            print(f"Dados carregados! Salario: R$ {salario:.2f}")
    except FileNotFoundError:   # caso o arquivo não exista, inicia do zero
        print("Bem-vindo! Nenhum dado encontrado. Começando do zero.")


# Função que vai salvar os dados em um arquivo JSON
def salvar_dados():
    # monta um dicionário com os dados atuais
    dados = {
        "salario": salario,  # salva o salário
        "gastos": gastos     # salva a lista de gastos
    }   
    with open("dados_gastos.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        #   salva os dados no arquivo - sobrescreve o arquivo existente, se houver


#Função que vai cadastrar seu salario
def cadastrar_salario():
    global salario   # avisa que vai alterar a variável global
    while True:
        try:
            salario = float(input("Digite seu salário: R$ "))
            if salario <= 0:   # verifica se o salario digitado e acima de zero
                print("Salário deve ser maior que zero!")
            else:
                print(f"\nSalário de R$ {salario:.2f} cadastrado!")
                salvar_dados()  # salva os dados no arquivo JSON apos cadastrar o salario
                break   # sai caso tenha funcionado
        except ValueError:   # captura erro se for digitado letra ao inves de numero
            print("Digite somente números!")


# função que mostra as categorias disponíveis
def mostrar_categorias():
    print("\n==== CATEGORIAS ====")
    contador = 1   # contador para numerar as opções
    opcoes = []   # lista para guardar as categorias na ordem

    # percorre cada grupo e seuas categorias
    for grupo, subcategorias in categorias.items():
        print(f"{grupo}:")   # ex: "Necessidades:"
        for sub in subcategorias:
            print(f"  {contador}. {sub}")   #ex: " 1. Alimentação"
            opcoes.append(sub)   # salva a categoria na ordem certa
            contador += 1   # proximo número

    return opcoes    # devolve para usar na escolha do usuario

# pede os dados do gasto e salva na lista de gastos
# função separada só para pedir valor válido
def pedir_valor(mensagem):
    while True:  # fica repetindo até receber valor válido
        try:
            valor = float(input(mensagem))  # tenta converter para decimal
            if valor <= 0:  # verifica se é maior que zero
                print("Digite um valor maior que zero!")
            else:
                return valor  # valor ok — devolve e sai
        except ValueError:  # captura erro se digitar letra
            print("Digite somente números!")

# função separada só para pedir número inteiro válido
def pedir_inteiro(mensagem):
    while True:  # fica repetindo até receber inteiro válido
        try:
            valor = int(input(mensagem))  # tenta converter para inteiro
            if valor <= 0:  # verifica se é maior que zero
                print("Digite um valor maior que zero!")
            else:
                return valor  # valor ok — devolve e sai
        except ValueError:  # captura erro se digitar letra
            print("Digite apenas números!")

# função separada só para pedir categoria válida
def pedir_categoria():
    opcoes = mostrar_categorias()  # mostra as categorias e guarda a lista
    while True:  # fica repetindo até receber categoria válida
        try:
            escolha = int(input("\nEscolha a categoria (número): "))  # pede a escolha
            if 1 <= escolha <= len(opcoes):  # verifica se o número existe na lista
                return opcoes[escolha - 1]  # devolve o nome da categoria escolhida
            else:
                print(f"Escolha entre 1 e {len(opcoes)}!")  # avisa se inválido
        except ValueError:  # captura erro se digitar letra
            print("Digite apenas números!")

# agora adicionar_gasto fica limpa e simples
def adicionar_gasto():
    print("\n═══ NOVO GASTO ═══")

    nome = input("Nome do gasto: ")          # pede o nome do gasto
    valor = pedir_valor("Valor: R$ ")        # chama função para pedir valor
    parcelas = pedir_inteiro("Número de parcelas (1 = à vista): ")  # chama função para pedir parcelas
    valor_parcela = round(valor / parcelas, 2)        # divide o total pelas parcelas
    data = input("Data (dd/mm/aaaa): ")      # pede a data
    categoria = pedir_categoria()            # chama função para pedir categoria

    # monta o dicionário com todos os dados do gasto
    gasto = {
        "nome": nome,
        "valor": valor,
        "parcelas": parcelas,
        "valor_parcela": valor_parcela,
        "data": data,
        "categoria": categoria
    }

    gastos.append(gasto)  # adiciona o dicionário na lista de gastos
    salvar_dados()        # salva os dados no arquivo JSON apos adicionar o gasto
    print(f"\nGasto '{nome}' de R$ {valor:.2f} adicionado!")

    if parcelas > 1:  # só mostra parcelas se for parcelado
        print(f"Parcelado em {parcelas}x de R$ {valor_parcela:.2f}")

# mostra todos os gastos organizados por categoria
def listar_gastos():
    if len(gastos) == 0:  # verifica se a lista está vazia
        print("\nNenhum gasto cadastrado ainda!")
        return  # sai da função sem fazer mais nada

    print("\n==== SEUS GASTOS ====")
    total_geral = 0.0  # começa o total em zero para ir somando

    for grupo, subcategorias in categorias.items():  # percorre cada grupo
        total_grupo = 0.0     # total do grupo começa em zero
        gastos_do_grupo = []  # lista vazia para guardar gastos deste grupo

        for sub in subcategorias:  # percorre cada subcategoria
            for gasto in gastos:   # percorre todos os gastos cadastrados
                if gasto["categoria"] == sub:      # se pertence a esta categoria
                    gastos_do_grupo.append(gasto)  # adiciona na lista do grupo
                    total_grupo += gasto["valor"]  # soma ao total do grupo

        if len(gastos_do_grupo) > 0:  # só mostra se tiver gastos neste grupo
            print(f"\n📁 {grupo} - Total: R$ {total_grupo:.2f}")

            for gasto in gastos_do_grupo:  # percorre os gastos do grupo
                print(f"  • {gasto['nome']}")                        # nome
                print(f"    Valor: R$ {gasto['valor']:.2f}")         # valor
                print(f"    Categoria: {gasto['categoria']}")        # categoria
                print(f"    Data: {gasto['data']}")                  # data

                if gasto["parcelas"] > 1:  # só mostra se for parcelado
                    print(f"    Parcelas: {gasto['parcelas']}x de R$ {gasto['valor_parcela']:.2f}")

            total_geral += total_grupo  # soma o total do grupo ao total geral

    print(f"\n💰 Total gasto: R$ {total_geral:.2f}")
    print(f"💰 Salário: R$ {salario:.2f}")
    print(f"💰 Saldo restante: R$ {salario - total_geral:.2f}")

# mostra o resumo baseado na regra 50/30/20
def resumo_50_30_20():
    if salario == 0:   # verifica se o salário foi cadastrado
        print("Cadastre um salário primeiro")
        return
    
    print("\n==== RESUMO 50/30/20 ====")

    # calcula os limites de cada grupo com base no salário
    limite_necessidades = salario * 0.50  # 50% do salário para necessidades
    limite_desejos = salario * 0.30   # 30% do salário para desejos
    limite_investimentos = salario * 0.20   # 20% do salário para investimentos

    # começa os totais gastos em zero para ir somando
    total_necessidades = 0.0
    total_desejos = 0.0
    total_investimentos = 0.0

    for gasto in gastos:
        if gasto["categoria"] in categorias["Necessidades"]:   # se é necessidades
            total_necessidades += gasto["valor"]   # some ás necessidades
        elif gasto["categoria"] in categorias["Desejos"]:   # se é desejo
            total_desejos += gasto["valor"]    # some a desejos
        elif gasto["categoria"] in categorias["Investimentos"]:   # se é investiemntos
            total_investimentos += gasto["valor"]   # soma aos investimentos

    # mostra necessidades com limite, gasto e disponível
    print(f"\n🏠 Necessidades (50%) — Limite: R$ {limite_necessidades:.2f}")
    print(f"   Gasto:       R$ {total_necessidades:.2f}")
    print(f"   Disponível:  R$ {limite_necessidades - total_necessidades:.2f}")

    # mostra desejos com limite, gasto e disponível
    print(f"\n🎯 Desejos (30%) — Limite: R$ {limite_desejos:.2f}")
    print(f"   Gasto:      R$ {total_desejos:.2f}")
    print(f"   Disponível: R$ {limite_desejos - total_desejos:.2f}")

    # mostra investimentos com limite, gasto e disponível
    print(f"\n📈 Investimentos (20%) — Limite: R$ {limite_investimentos:.2f}")
    print(f"   Gasto:      R$ {total_investimentos:.2f}")
    print(f"   Disponível: R$ {limite_investimentos - total_investimentos:.2f}")

# função que mostra o menu de opções
def mostrar_menu():
    print("\n═══════════════════════════")
    print("   CONTROLE DE GASTOS")
    print("   Regra 50/30/20")
    print("═══════════════════════════")
    print("1. Cadastrar salário")
    print("2. Adicionar gastos")
    print("3. Listar gastos")
    print("4. Resumo 50/30/20")
    print("5. Sair")
    print("═══════════════════════════")

# Programa Principal

carregar_dados()   # carrega os dados salvos quando inicia o programa

while True:   # fica rodando até o usuário escolher sair
    mostrar_menu()   # fica rodando até o usuário escolher sair
    opcao = input("Escolha uma opção: ")   # pede a escolha do usuário

    if opcao == "1":
        cadastrar_salario()
    elif opcao == "2":
        if salario == 0:
            print("\n⚠️ Cadastre seu salário primeiro!")
        else:
            adicionar_gasto()
    elif opcao == "3":
        listar_gastos()
    elif opcao == "4":
        resumo_50_30_20()
    elif opcao == "5":
        salvar_dados()
        print("\nAte logo! Continue controlando seus gastos!")
        break
    else:
        print("\nOpção invalida! Digite um número de 1 a 5.")





    
