from datetime import datetime

def menu_inicial():
    print('''
======== ESCOLHA A OPÇÃO DESEJADA ========

        (1) - DEPOSITAR
        (2) - SACAR
        (3) - EXTRATO
        (4) - NOVA CONTA
        (5) - LISTAR CONTAS
        (6) - NOVO USUÁRIO
        (7) - SAIR
          
==========================================
    ''')
    while True:
        try:
            valor_menu_inicial=int(input("Digite o valor da opção desejada.\n=> "))
            if valor_menu_inicial in [1,2,3,4,5,6,7]:
                return valor_menu_inicial
            else:
                print("valor digitado incorreto")
        except ValueError:
            print("ERRO! - Valor digitado é invalido\nEscolha uma das opções do MENU.")
            continue
        if valor_menu_inicial is None:
            continue

def depositar(saldo,valor,/,*,extrato):# a / indica que antes da / deve ser argumento posicionais.
    if valor > 0:
        saldo += valor
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extrato.append(f"{data_hora} Valor depositado: R${valor:.2f}")
        print(f"Valor de R${valor:.2f} foi depositado com sucesso!")
        return saldo,extrato
    else:
        print("Valor digitado é invalido!\nTente novamente.")
        return saldo,extrato

def valor_digitado(operacao):
    while True:
        try:
            valor = float(input(f"Digite o valor de {operacao}.\n=> R$ "))
            if valor > 0:
                return valor
            elif valor == 0:
                return None
            else:
                print("Valor digitado incorreto\nEscolha um valor novamente ou\ndigite 0(zero) para voltar ao MENU. ")
        except ValueError:
            print("Digite um valor válido!\n Ou 0(zero) para voltar ao MENU.")
            continue
        if valor is None:
            continue

def sacar(*,saldo,valor,extrato,LIMITE_SAQUE,LIMITE_VALOR):#por chamada
    if valor >0 and (LIMITE_SAQUE > 0) and valor <= saldo and (valor <= LIMITE_VALOR):
        LIMITE_SAQUE -=1
        saldo-=valor
        data_hora =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extrato.append(f"{data_hora} Valor de saque: R${valor:.2f}")
        print(f"Saque de R${valor:.2f} realizado com sucesso!")
        
    else:
        print("Não foi possivel realizar seu saque. Verifique seu extrato.")
    return saldo,extrato,LIMITE_SAQUE

def exibir_extrato(saldo,LIMITE_SAQUE,LIMITE_VALOR,/,*,extrato):
    print("-"*16 + ("EXTRATO") + ("-")*16+"\n")
    if extrato:
        for transacao in extrato:
            print(transacao)
    else:
        print("Não foram realizadas transações.\n")

    print(f"\nSALDO: R${saldo:.2f}.")
    print(f"LIMITE DE SAQUE RESTANTE:{LIMITE_SAQUE}.")
    print(f"LIMITE DE VALOR POR SAQUE: R${LIMITE_VALOR:.2f}.")
    print("-"*40)
    return saldo,LIMITE_SAQUE,LIMITE_VALOR,extrato

def novo_usuario(usuarios):
    cpf = int(input("Digite seu CPF:\n=> "))
    usuario= filtrar_usuarios(cpf,usuarios)

    if usuario:
        print("Usuário cadastrado")
        return
    
    nome = input("Digite seu nome completo.\n=> ")
    endereco = input("Digite seu endereco(Logradouro , nro - bairro - cidade/ sigla estado).\n=> ")
    data_nascimento = input("Digite sua data de nascimento(dd-mm-aaaa).\n=> ")
    usuarios.append({"cpf":cpf,"nome":nome,"endereco":endereco,"data_nascimento":data_nascimento})

    print("Usuário cadastrado com sucesso.")

def filtrar_usuarios(cpf,usuarios):
    usuarios_filtrados=[usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia,numero_conta,usuarios):
    cpf=int(input("Digite seu cpf(somente numero).\n=> "))
    usuario=filtrar_usuarios(cpf,usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia":agencia,"numero_conta":numero_conta,"usuario":usuario}
    
    print("ERRO! Usuário não encontrado.")

def listar_conta(contas):
    for conta in contas:
        linha=f"""
        AGÉNCIA:{conta["agencia"]}
        CONTA:{conta["numero_conta"]}
        TITULAR:{conta["usuario"]["nome"]}
        """
        print("="*120)
        print(linha)

def main():
    saldo = 0.0
    extrato = []
    usuarios=[]
    contas =[]
    LIMITE_SAQUE=3
    LIMITE_VALOR=500
    AGENCIA="0001"

    while True:
        
        valor_menu_inicial=menu_inicial()

        if valor_menu_inicial == 1:
            valor = valor_digitado("depósito")
            if valor is not None:
                saldo,extrato = depositar(saldo,valor,extrato=extrato)
            else:
                print("Não foi possível realizar seu depósito.")       
    
        elif valor_menu_inicial == 2:
            valor=valor_digitado("saque")
            if valor is not None:
                saldo,extrato,LIMITE_SAQUE=sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    LIMITE_SAQUE=LIMITE_SAQUE,
                    LIMITE_VALOR=LIMITE_VALOR
                    )
        
        elif valor_menu_inicial == 3:
            exibir_extrato(saldo,LIMITE_SAQUE,LIMITE_VALOR,extrato=extrato)
        
        elif valor_menu_inicial == 4:
            numero_conta = len(contas) +1
            conta = criar_conta(AGENCIA,numero_conta,usuarios)

            if conta:
                contas.append(conta)

        elif valor_menu_inicial == 5:
            listar_conta(contas)

        elif valor_menu_inicial == 6:
            novo_usuario(usuarios)

        elif valor_menu_inicial == 7:
            print("Obrigado por usar nosso sistema\nSaindo...")
            return False

        else:
            print("ERRO NÃO IDENTIFICADO")
            continue

main()
