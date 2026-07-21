import json

def carregar_dados():
    """Carrega o banco de dados JSON local."""
    try:
        with open('f1_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("\n[ERRO] O arquivo 'f1_data.json' não foi encontrado na pasta.")
        print("Certifique-se de que salvou o arquivo JSON no mesmo local deste script.\n")
        return None

def buscar_piloto(sobrenome, dados):
    """Busca um piloto pelo sobrenome."""
    if not dados:
        return

    pilotos = dados.get("pilotos", [])
    encontrado = False

    for driver in pilotos:
        if driver["sobrenome"].lower() == sobrenome.lower():
            encontrado = True
            print("\n" + "="*45)
            print(f" Piloto: {driver['nome']}")
            print(f" Nacionalidade: {driver['nacionalidade']}")
            print(f" Data de Nascimento: {driver['nascimento']}")
            print(f" Número: {driver['numero']}")
            print(f" Títulos Mundiais: {driver['titulos']}")
            print(f" Vitórias: {driver['vitorias']}")
            print(f" Pódios: {driver['podios']}")
            print(f" Wikipédia: {driver['wiki']}")
            print("="*45 + "\n")
            break

    if not encontrado:
        print(f"\nPiloto '{sobrenome}' não encontrado no banco de dados.\n")

def buscar_vitorias_brasileiros(dados):
    """Gera o ranking de pilotos brasileiros ordenado por vitórias."""
    if not dados:
        return

    pilotos = dados.get("pilotos", [])
    brasileiros = [p for p in pilotos if p["nacionalidade"] == "Brasileiro"]
    
    # Ordena os brasileiros pelo número de vitórias (do maior para o menor)
    ranking = sorted(brasileiros, key=lambda x: x["vitorias"], reverse=True)

    print("\n" + "="*45)
    print(" RANKING DE VENCEDORES BRASILEIROS NA F1")
    print("="*45)
    for pos, p in enumerate(ranking, 1):
        print(f" {pos}º lugar: {p['nome']} - {p['vitorias']} vitórias ({p['podios']} pódios)")
    print("="*45 + "\n")

def menu():
    dados = carregar_dados()
    if not dados:
        return

    while True:
        print("--- RADAR F1 (PYTHON - MODALIDADE LOCAL) ---")
        print("1. Buscar informações de um piloto")
        print("2. Ver ranking de vitórias brasileiras")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            sobrenome = input("Digite o sobrenome do piloto (ex: senna, massa, barrichello, bortoleto): ").strip()
            if sobrenome:
                buscar_piloto(sobrenome, dados)
            else:
                print("Nome inválido.")
        elif opcao == "2":
            buscar_vitorias_brasileiros(dados)
        elif opcao == "0":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida!\n")

if __name__ == "__main__":
    menu()