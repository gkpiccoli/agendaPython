
import datetime
import json
from IPython.display import clear_output
#erro de importação, não consegui resolver


def limpar_tela():
    clear_output(wait=True)


def salvar_agenda(agenda, filename="agenda_data.json"):
    with open(filename, 'w') as file:
        json.dump(agenda, file)


def carregar_agenda(filename="agenda_data.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def incluir_contato(agenda, nome, telefone):
    if nome in agenda:
        return "Contato já existe na agenda."
    agenda[nome] = {
        "telefone": telefone,
        "data_inclusao": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    salvar_agenda(agenda)
    return f"Contato {nome} adicionado com sucesso!"


def pesquisar_contato(agenda, nome):
    contato = agenda.get(nome)
    if contato:
        return contato["telefone"]
    return "Contato não encontrado."


def atualizar_contato(agenda, nome):
    if nome not in agenda:
        return "Contato não encontrado."

    print("\nO que você gostaria de atualizar?")
    print("1. Nome")
    print("2. Telefone")
    print("3. Nome e Telefone")
    escolha = input("Escolha uma opção (1-3): ")

    if escolha == "1":
        novo_nome = input("Digite o novo nome: ")
        agenda[novo_nome] = agenda.pop(nome)
        salvar_agenda(agenda)
        return f"Nome de '{nome}' atualizado para '{novo_nome}' com sucesso!"
    elif escolha == "2":
        novo_telefone = input("Digite o novo telefone: ")
        if not novo_telefone.isdigit() or len(novo_telefone) not in [10, 11]:
            return "Número de telefone inválido. Certifique-se de que ele contém apenas dígitos e tem 10 ou 11 números."
        agenda[nome]["telefone"] = novo_telefone
        salvar_agenda(agenda)
        return f"Telefone de {nome} atualizado com sucesso!"
    elif escolha == "3":
        novo_nome = input("Digite o novo nome: ")
        novo_telefone = input("Digite o novo telefone: ")
        if not novo_telefone.isdigit() or len(novo_telefone) not in [10, 11]:
            return "Número de telefone inválido. Certifique-se de que ele contém apenas dígitos e tem 10 ou 11 números."
        agenda[novo_nome] = {
            "telefone": novo_telefone,
            "data_inclusao": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        del agenda[nome]
        salvar_agenda(agenda)
        return f"Nome e telefone de '{nome}' atualizados com sucesso!"
    else:
        return "Opção inválida."


def excluir_contato(agenda, nome):
    if nome not in agenda:
        return "Contato não encontrado."
    del agenda[nome]
    salvar_agenda(agenda)
    return f"Contato {nome} excluído com sucesso!"


def ordenar_contatos(agenda, por="nome"):
    if por == "nome":
        return sorted(agenda.items(), key=lambda x: x[0])
    elif por == "data":
        return sorted(agenda.items(), key=lambda x: x[1]["data_inclusao"], reverse=True)
    else:
        return []


def registrar_log(mensagem):
    with open("agenda_logs.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp} - {mensagem}\n")


def interface_usuario():
    agenda = carregar_agenda()
    while True:
        limpar_tela()
        print("\n" + "=" * 40)
        print("Agenda de Contatos".center(40))
        print("=" * 40)
        print("1. Incluir Contato")
        print("2. Pesquisar Contato")
        print("3. Atualizar Contato")
        print("4. Excluir Contato")
        print("5. Mostrar Contatos Ordenados por Nome")
        print("6. Mostrar Contatos Ordenados por Data de Inclusão")
        print("7. Limpar Tela")
        print("8. Sair")
        opcao = input("Escolha uma opção (1-8): ")

        if opcao == "1":
            nome = input("Nome do Contato: ")
            telefone = input("Telefone do Contato: ")
            mensagem = incluir_contato(agenda, nome, telefone)
            print(mensagem)
            registrar_log(mensagem)
        elif opcao == "2":
            nome = input("Nome do Contato: ")
            print(f"Telefone: {pesquisar_contato(agenda, nome)}")
        elif opcao == "3":
            nome = input("Nome do Contato a ser Atualizado: ")
            mensagem = atualizar_contato(agenda, nome)
            print(mensagem)
            registrar_log(mensagem)
        elif opcao == "4":
            nome = input("Nome do Contato a ser Excluído: ")
            mensagem = excluir_contato(agenda, nome)
            print(mensagem)
            registrar_log(mensagem)
        elif opcao in ["5", "6"]:
            criterio = "nome" if opcao == "5" else "data"
            contatos_ordenados = ordenar_contatos(agenda, por=criterio)
            for nome, dados in contatos_ordenados:
                print(f"{nome}: {dados['telefone']} (Adicionado em: {dados['data_inclusao']})")
        elif opcao == "7":
            pass
        elif opcao == "8":
            print("Obrigado por usar a Agenda de Contatos!")
            break
        else:
            print("Opção inválida. Tente novamente.")
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    interface_usuario()
