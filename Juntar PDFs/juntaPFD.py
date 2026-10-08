# Para que o script funcione intale: pip install pypdf
from pypdf import PdfWriter

# Lista com caminho dos PDF's que serão unidos
arquivos = [
    r"C:\Users\User\Desktop\Folders\File.pdf",
    r"C:\Users\User\Desktop\Folders\File.pdf",
    r"C:\Users\User\Desktop\Folders\File.pdf",
    r"C:\Users\User\Desktop\Folders\File.pdf",

]

#Cria o objeto que vai montar o novo PDF
writer = PdfWriter()

# Adiciona todas as páginas de cada arquivo na ordem definida
for caminho in arquivos:
    writer.append(caminho)

# Caminho de saída do novo arquivo
caminho_saida = r"C:\users\User\Desktop\Folders\File.pdf"

# Escrever PDF unido no Disco
writer.write(caminho_saida)

print(f"PDF unido criado em: {caminho_saida}")

