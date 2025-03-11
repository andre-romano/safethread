import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level
    # Log format
    format="%(asctime)s - [%(levelname)s] - %(name)s() - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
    handlers=[logging.StreamHandler(sys.stdout)]  # Log to stdout
)

logger = logging.getLogger(__name__)

# Função para executar comandos do Git e capturar a saída


def run_git_command(command):
    # logger.debug(f'Running command {command}')
    result = subprocess.run(command, capture_output=True, text=True)
    # logger.debug(f'Return code {result.returncode}')
    # logger.debug(f'\nStdout: \n{result.stdout}\nStderr: {result.stderr}')
    if result.returncode != 0:
        msg = f"Command '{command}'\nStderr: {result.stderr}"
        logger.error(msg)
        raise Exception(msg)
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
        tags = run_git_command(
            ["git", "tag", "--sort=-creatordate"]).splitlines()

        len_tags = len(tags)
        for i in range(len_tags):
            # get tags
            prev_tag = tags[i]
            tag = tags[i]

            if i+1 < len_tags:
                prev_tag = tags[i+1]

            # Obtém a data da tag
            tag_date = run_git_command(
                ["git", "log", "-1", "--format=%ai", tag])

            # Escreve a tag e a data no changelog
            f.write(f"## {tag} ({tag_date})\n\n")

            # Obtém os commits entre a tag e a anterior
            commits = run_git_command(
                ["git", "log", "--oneline", f"{prev_tag}^..{tag}"]).splitlines()
            for commit in commits:
                f.write(f"- {commit}\n")

            f.write("\n")

    print(f"Changelog gerado com sucesso em {changelog_file}")


# Executa a função
if __name__ == "__main__":
    generate_changelog()
