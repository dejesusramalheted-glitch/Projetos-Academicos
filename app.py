def menu ():
    print("=========== Olá ===============")
    print("======== Seja Bem-Vindo=========")
    print("1 Cadastro de produto")  
    print("2 Consulta de Produtos")
    

    estoque = []

    while True:
        print("1 - Cadastro")
        print("2 - Consulta")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastro(estoque)
        elif escolha =="2":
            consulta(estoque)
        elif escolha =="3":
            break
        else:
            print("Opção Invalida")

            
def cadastro (estoque):
        cadastra_mercadoria = input("Adicione Mercadoria: ").strip()
        if not cadastra_mercadoria:
             print("O campo não pode ser vazio")
             return
        
        categoria = input(f"Tipo de Salgado ex: Assado, Frito, Pastel: ").strip()
        quantidade = input("Digite a Quantidade produzida ex: 10: ")
        try:
             quantidade_produzida = int(quantidade)
        except ValueError:
             print("Quantidade Invalida")
             return

        produto = {
             "cadastra_mercadoria": cadastra_mercadoria,
             "categoria": categoria,
             "quantidade": quantidade_produzida,
        }
        estoque.append(produto)
        print(f"Produto: {produto['cadastra_mercadoria']} \ndescricao: {produto['categoria']} \nquantidade: {produto['quantidade']}")


def consulta (estoque):
    if not estoque:
        print("Nenhum produto cadastrado ainda.")
        return

    for produto in estoque:
        print(f"Produto: {produto['cadastra_mercadoria']} \ndescricao: {produto['categoria']} \nquantidade: {produto['quantidade']}")

if __name__ == "__main__":
    menu()