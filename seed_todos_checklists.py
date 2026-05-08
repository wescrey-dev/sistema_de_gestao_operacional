import runpy
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SEED_FILES = [
    "seed_primeiro_lote_checklists.py",
    "seed_segundo_lote_checklists.py",
    "seed_terceiro_lote_checklists.py",
    "seed_quarto_lote_checklists.py",
    "seed_quinto_lote_checklists.py",
    "seed_sexto_lote_checklists.py",
    "seed_setimo_lote_checklists.py",
    "seed_oitavo_lote_checklists.py",
    "seed_nono_lote_checklists.py",
    "seed_decimo_lote_checklists.py",
    "seed_decimo_primeiro_lote_checklists.py",
    "seed_decimo_segundo_lote_checklists.py",
    "seed_decimo_terceiro_lote_checklists.py",
    "seed_decimo_quarto_lote_checklists.py",
    "seed_decimo_quinto_lote_checklists.py",
    "seed_decimo_sexto_lote_checklists.py",
]

def main():
    print("\n=== Cadastro mestre de todos os modelos de checklist ===\n")

    arquivos_encontrados = 0
    arquivos_faltando = []

    for file_name in SEED_FILES:
        file_path = BASE_DIR / file_name

        if not file_path.exists():
            arquivos_faltando.append(file_name)
            print(f"[PULADO] Arquivo não encontrado: {file_name}")
            continue

        print(f"[EXECUTANDO] {file_name}")
        runpy.run_path(str(file_path), run_name="__main__")
        arquivos_encontrados += 1
        print(f"[OK] Finalizado: {file_name}\n")

    print("=== Resumo ===")
    print(f"Arquivos executados: {arquivos_encontrados}")

    if arquivos_faltando:
        print("\nArquivos não encontrados:")
        for file_name in arquivos_faltando:
            print(f"- {file_name}")
    else:
        print("Todos os lotes foram executados com sucesso.")

    print("\nProcesso concluído.\n")

if __name__ == "__main__":
    main()
