import os
import re
import shutil
from pathlib import Path

def organizar_arquivos_por_ano(pasta_raiz: str) -> None:
    pasta = Path(pasta_raiz)
    
    # Regex para capturar anos de 2018 a 2099
    padrao_ano = re.compile(r'\b(20[1-9]\d|2[1-9]\d{2})\b')
    # Explicação:
    # 20[1-9]\d  → 2018 a 2099
    # 2[1-9]\d{2} → 2100 a 2999 (caso queira estender no futuro)
    # Se quiser restrito só até 2099, use: r'\b(20[1-9]\d)\b'

    for arquivo in pasta.iterdir():
        if not arquivo.is_file():
            continue
        
        nome = arquivo.stem
        match = padrao_ano.search(nome)
        
        if not match:
            print(f"Sem ano válido (2018+) em: {arquivo.name}")
            continue
        
        ano = match.group(1)
        pasta_destino = pasta / ano
        pasta_destino.mkdir(exist_ok=True)
        
        destino = pasta_destino / arquivo.name
        
        # Evita sobrescrever arquivos com mesmo nome
        if destino.exists():
            base, ext = destino.stem, destino.suffix
            contador = 1
            while destino.exists():
                novo_nome = f"{base}_{contador}{ext}"
                destino = pasta_destino / novo_nome
                contador += 1
        
        shutil.move(str(arquivo), str(destino))
        print(f"Movido: {arquivo.name} → {pasta_destino.name}/")

if __name__ == "__main__":
    organizar_arquivos_por_ano(r"C:\Users\User\Desktop\Folders")

    print("Arquivos organizados com sucesso!")