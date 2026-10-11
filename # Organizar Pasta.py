import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


CATEGORIAS = {
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".jfif"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"},
    "Vídeos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".m4v"},
    "Músicas": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Programas": {".exe", ".msi", ".apk", ".bat", ".cmd", ".dmg", ".msix"},
}


def criar_pastas(base_dir: Path):
    for nome in CATEGORIAS:
        (base_dir / nome).mkdir(exist_ok=True)
    (base_dir / "Outros").mkdir(exist_ok=True)


def organizar_pasta(pasta: str):
    pasta = Path(pasta)
    if not pasta.exists() or not pasta.is_dir():
        raise FileNotFoundError(f"Pasta inválida: {pasta}")

    criar_pastas(pasta)

    movidos = []
    ignorados = []

    for item in pasta.iterdir():
        if item.is_dir():
            continue

        extensao = item.suffix.lower()
        destino = None

        for nome_pasta, extensoes in CATEGORIAS.items():
            if extensao in extensoes:
                destino = pasta / nome_pasta
                break

        if destino is None:
            destino = pasta / "Outros"

        if item.parent == destino:
            ignorados.append(item.name)
            continue

        nome_final = item.name
        destino_arquivo = destino / nome_final
        contador = 1

        while destino_arquivo.exists():
            nome_final = f"{item.stem}_{contador}{item.suffix}"
            destino_arquivo = destino / nome_final
            contador += 1

        shutil.move(str(item), str(destino_arquivo))
        movidos.append(f"{item.name} → {destino_arquivo.relative_to(pasta)}")

    return movidos, ignorados


def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta para organizar")
    if pasta:
        caminho_entry.delete(0, tk.END)
        caminho_entry.insert(0, pasta)


def executar_organizacao():
    pasta = caminho_entry.get().strip().strip('"')

    if not pasta:
        messagebox.showwarning("Atenção", "Selecione uma pasta antes de continuar.")
        return

    try:
        movidos, ignorados = organizar_pasta(pasta)

        mensagem = [f"Arquivos movidos: {len(movidos)}\n"]
        if movidos:
            mensagem.extend(f"- {item}\n" for item in movidos[:20])
            if len(movidos) > 20:
                mensagem.append(f"... e mais {len(movidos) - 20} arquivos.\n")
        else:
            mensagem.append("Nenhum arquivo foi movido.\n")

        if ignorados:
            mensagem.append(f"\nArquivos ignorados: {len(ignorados)}\n")
            for nome in ignorados[:10]:
                mensagem.append(f"- {nome}\n")

        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert(tk.END, "".join(mensagem))
        status_var.set("Status: organização concluída.")
        messagebox.showinfo("Concluído", "Organização finalizada com sucesso!")

    except FileNotFoundError:
        status_var.set("Status: pasta inválida.")
        messagebox.showerror("Erro", "Pasta inválida. Verifique o caminho informado.")
    except Exception as erro:
        status_var.set("Status: erro ao processar.")
        messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")


if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Organizador de Pasta")
    janela.geometry("720x540")
    janela.minsize(620, 480)
    janela.configure(bg="#eef2ff")

    estilo = {
        "bg": "#eef2ff",
        "panel": "#ffffff",
        "primary": "#2563eb",
        "primary_dark": "#1d4ed8",
        "text": "#111827",
        "muted": "#475569",
        "border": "#cbd5e1",
    }

    topo = tk.Frame(janela, bg=estilo["panel"], padx=24, pady=18)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Organizador de arquivos por extensão",
        font=("Arial", 18, "bold"),
        fg=estilo["text"],
        bg=estilo["panel"],
        anchor="w",
    ).pack(anchor="w")

    tk.Label(
        topo,
        text="Organiza automaticamente imagens, documentos, vídeos, músicas, compactados e programas.",
        font=("Arial", 10),
        fg=estilo["muted"],
        bg=estilo["panel"],
        anchor="w",
    ).pack(anchor="w", pady=(6, 0))

    frame_caminho = tk.Frame(janela, bg=estilo["bg"], padx=20, pady=18)
    frame_caminho.pack(fill="x")

    tk.Label(frame_caminho, text="Pasta de origem:", font=("Arial", 11, "bold"), bg=estilo["bg"], fg=estilo["text"]).pack(anchor="w")

    caminho_entry = tk.Entry(frame_caminho, width=80, font=("Arial", 10), bd=1, relief="solid")
    caminho_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=(6, 0))

    btn_pasta = tk.Button(frame_caminho, text="Selecionar", command=selecionar_pasta, bg="#e2e8f0", fg=estilo["text"], font=("Arial", 10, "bold"), bd=0, padx=12, pady=8)
    btn_pasta.pack(side="right", pady=(6, 0))

    btn_organizar = tk.Button(
        janela,
        text="Organizar Pasta",
        command=executar_organizacao,
        width=22,
        height=2,
        bg=estilo["primary"],
        fg="white",
        font=("Arial", 11, "bold"),
        bd=0,
        activebackground=estilo["primary_dark"],
        cursor="hand2",
    )
    btn_organizar.pack(pady=(6, 12))

    status_var = tk.StringVar(value="Status: pronto para organização.")
    status_label = tk.Label(janela, textvariable=status_var, font=("Arial", 10), fg=estilo["muted"], bg=estilo["bg"])
    status_label.pack(anchor="w", padx=20)

    resultado_frame = tk.Frame(janela, bg=estilo["panel"], padx=16, pady=12, bd=1, relief="solid")
    resultado_frame.pack(fill="both", expand=True, padx=20, pady=(12, 18))

    tk.Label(resultado_frame, text="Resultado:", font=("Arial", 11, "bold"), bg=estilo["panel"], fg=estilo["text"]).pack(anchor="w")

    resultado_texto = tk.Text(resultado_frame, height=15, width=90, wrap="word", bg="#f8fafc", fg=estilo["text"], bd=0, font=("Consolas", 10))
    resultado_texto.pack(fill="both", expand=True, pady=(8, 0))

    janela.mainloop()

# Desenvolvedor: Leanderson Viana