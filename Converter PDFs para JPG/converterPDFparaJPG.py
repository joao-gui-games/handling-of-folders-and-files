from pathlib import Path
from pdf2image import convert_from_path


def converter_pdf_para_jpg(
    pdf_path: Path,
    output_folder: Path,
    dpi: int = 300,
    poppler_path: str | None = None,
) -> list[Path]:
    """
    Converte cada página de um PDF em arquivos JPG.

    Regra de nomeação:
      - 1 página:  nome_original.jpg
      - + páginas: nome_original_pag_001.jpg, nome_original_pag_002.jpg, ...
    """
    imagens = convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=poppler_path,
    )

    base_name = pdf_path.stem  # nome sem .pdf
    caminhos_gerados = []

    if len(imagens) == 1:
        # Apenas uma página: usa exatamente o mesmo nome do PDF
        nome_arquivo = f"{base_name}.jpg"
        caminho_imagem = output_folder / nome_arquivo
        imagens[0].save(caminho_imagem, "JPEG", quality=95)
        caminhos_gerados.append(caminho_imagem)
    else:
        # Várias páginas: adiciona sufixo numérico
        for i, img in enumerate(imagens, start=1):
            nome_arquivo = f"{base_name}_pag_{i:03d}.jpg"
            caminho_imagem = output_folder / nome_arquivo
            img.save(caminho_imagem, "JPEG", quality=95)
            caminhos_gerados.append(caminho_imagem)

    return caminhos_gerados


def converter_todos_pdfs_da_pasta(
    pasta_pdf: str,
    pasta_saida: str,
    dpi: int = 300,
    poppler_path: str | None = None,
) -> None:
    """
    Converte todos os PDFs de uma pasta para JPG, mantendo o nome original.
    """
    pasta_pdf = Path(pasta_pdf)
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    pdfs = list(pasta_pdf.glob("*.pdf"))

    if not pdfs:
        print("Nenhum arquivo PDF encontrado na pasta informada.")
        return

    for pdf_path in pdfs:
        print(f"Convertendo: {pdf_path.name}")
        try:
            converter_pdf_para_jpg(
                pdf_path,
                pasta_saida,
                dpi=dpi,
                poppler_path=poppler_path,
            )
        except Exception as e:
            print(f"Erro ao converter {pdf_path.name}: {e}")

    print("Conversão concluída.")


if __name__ == "__main__":
    # ===== CONFIGURAÇÃO =====
    # Pasta onde estão os PDFs
    pasta_pdf = r"C:\Users\User\Folder"

    # Pasta onde os JPGs serão salvos
    pasta_saida = r"C:\Users\User\Folder"

    # Se não adicionou o Poppler ao PATH, informe a pasta 'bin' dele:
    # Exemplo: r"C:\tools\poppler-24.09.0\bin"
    # Se já estiver no PATH, deixe como None
    poppler_bin = None  # ou r"C:\tools\poppler-24.09.0\bin"

    # Qualidade / resolução (DPI)
    dpi = 300
    # =========================

    converter_todos_pdfs_da_pasta(
        pasta_pdf,
        pasta_saida,
        dpi=dpi,
        poppler_path=poppler_bin,
    )