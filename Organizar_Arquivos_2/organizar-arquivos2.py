import os
import re
import shutil

# Pasta principal onde estão os funcionários
PASTA_RAIZ = r"C:\Users\User\Desktop\Funcionário 1º sem 2026"

# Mapeamento das pastas de categoria
CATEGORIAS = {
    "Cartão de Ponto": "Cartão de Ponto",
    "Holerites": "Holerites",
    "Vale": "Vale"
}

# Mapeamento dos meses
MESES = {
    "Jan": "01 Janeiro",
    "Fev": "02 Fevereiro",
    "Mar": "03 Março",
    "Abr": "04 Abril",
    "Mai": "05 Maio",
    "Jun": "06 Junho",
    "Jul": "07 Julho",
    "Ago": "08 Agosto",
    "Set": "09 Setembro",
    "Out": "10 Outubro",
    "Nov": "11 Novembro",
    "Dez": "12 Dezembro"
}


def identificar_categoria(pasta_atual):
    """Identifica a categoria com base no nome da pasta."""
    nome_pasta = os.path.basename(pasta_atual)

    for categoria in CATEGORIAS:
        if nome_pasta.lower() == categoria.lower():
            return CATEGORIAS[categoria]

    return None


def identificar_mes(nome_arquivo):
    """Identifica o mês pelo padrão 'Mes-2026' no nome do arquivo."""
    padrao = re.search(r"([A-Za-z]{3})-2026", nome_arquivo, re.IGNORECASE)

    if not padrao:
        return None

    mes_encontrado = padrao.group(1).capitalize()

    return MESES.get(mes_encontrado)


def organizar_arquivos():
    """Percorre as pastas e move os PDFs para a estrutura correta."""
    if not os.path.isdir(PASTA_RAIZ):
        print(f"[ERRO] A pasta raiz não existe: {PASTA_RAIZ}")
        return

    for pasta_atual, subpastas, arquivos in os.walk(PASTA_RAIZ):

        categoria = identificar_categoria(pasta_atual)

        if categoria is None:
            continue

        for arquivo in arquivos:

            if not arquivo.lower().endswith(".pdf"):
                continue

            mes = identificar_mes(arquivo)

            if mes is None:
                print(f"[AVISO] Mês não identificado: {arquivo}")
                continue

            pasta_destino = os.path.join(PASTA_RAIZ, mes, categoria)
            os.makedirs(pasta_destino, exist_ok=True)

            caminho_origem = os.path.join(pasta_atual, arquivo)
            caminho_destino = os.path.join(pasta_destino, arquivo)

            # Evita sobrescrever arquivos existentes
            contador = 1
            while os.path.exists(caminho_destino):
                nome_base, extensao = os.path.splitext(arquivo)
                novo_nome = f"{nome_base} ({contador}){extensao}"
                caminho_destino = os.path.join(pasta_destino, novo_nome)
                contador += 1

            shutil.move(caminho_origem, caminho_destino)
            print(f"[MOVIDO] {arquivo} -> {pasta_destino}")


def remover_pastas_vazias():
    """Remove pastas que ficarem vazias após a organização."""
    for pasta_atual, subpastas, arquivos in os.walk(PASTA_RAIZ, topdown=False):

        if pasta_atual == PASTA_RAIZ:
            continue

        try:
            if not os.listdir(pasta_atual):
                os.rmdir(pasta_atual)
                print(f"[REMOVIDA] {pasta_atual}")
        except PermissionError:
            print(f"[AVISO] Sem permissão para remover: {pasta_atual}")


if __name__ == "__main__":
    organizar_arquivos()
    remover_pastas_vazias()