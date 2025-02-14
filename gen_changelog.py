import os
import subprocess

# Função para executar comandos do Git e capturar a saída
def run_git_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao executar comando: {command}\n{result.stderr}")
    return result.stdout.strip()

# Função para gerar o changelog
def generate_changelog():
    changelog_file = "CHANGELOG.md"
    
    # Remove o arquivo de changelog existente, se houver
    if os.path.exists(changelog_file):
        os.remove(changelog_file)

    # Adiciona o cabeçalho
    with open(changelog_file, "w") as f:
        f.write("# Changelog\n\n")
        
        # Obtém as tags do Git ordenadas pela data de criação
        tags = run_git_command(["git", "tag", "--sort=-creatordate"]).splitlines()
        
        for tag in tags:
            # Obtém a data da tag
            tag_date = run_git_command(["git", "log", "-1", "--format=%ai", tag])
            
            # Escreve a tag e a data no changelog
            f.write(f"## {tag} ({tag_date})\n\n")
            
            # Obtém os commits entre a tag e a anterior
            commits = run_git_command(["git", "log", "--oneline", f"{tag}^..{tag}"]).splitlines()
            for commit in commits:
                f.write(f"- {commit}\n")
            
            f.write("\n")

    print(f"Changelog gerado com sucesso em {changelog_file}")

# Executa a função
if __name__ == "__main__":
    generate_changelog()
