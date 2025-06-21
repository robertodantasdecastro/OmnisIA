"""
OMNISIA - Sistema Integrado de IA Multimodal / Integrated Multimodal AI System
=============================================================================

Sistema completo de IA com suporte para:
- Modelos locais (DeepSeek R1, Llama, Mistral, etc.)
- APIs externas (OpenAI, DeepSeek, Anthropic, AWS Bedrock)
- Múltiplos bancos de dados (PostgreSQL, MongoDB, Redis, SQLite)
- Protocolos remotos (FTP, SFTP, HTTP, WebDAV)
- Treinamento LoRA avançado
- Interface web intuitiva com assistente IA
- Integração com Jupyter, Kaggle, SageMaker

Autor: Roberto Dantas de Castro
Email: robertodantasdecastro@gmail.com
Versão: 2.0.0
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(str(Path(__file__).parent))

# Importar configurações
from config import (
    SYSTEM_INFO,
    setup_logging,
    DEVELOPMENT_MODE,
    DEBUG_MODE,
    API_HOST,
    API_PORT,
    FRONTEND_HOST,
    FRONTEND_PORT,
    JUPYTER_CONFIG,
    validate_config,
)

# CLI App
app = typer.Typer(
    name="omnisia",
    help="🤖 OmnisIA - Sistema Integrado de IA Multimodal",
    rich_markup_mode="rich",
)

console = Console()
logger = setup_logging()


def display_banner():
    """Exibe o banner do sistema"""
    banner_text = f"""
[bold cyan]  ___  __  __ _   _ ___ ____ ___    _    [/bold cyan]
[bold cyan] / _ \\|  \\/  | \\ | |_ _/ ___|_ _|  / \\   [/bold cyan]
[bold cyan]| | | | |\\/| |  \\| || |\\___ \\| |  / _ \\  [/bold cyan]
[bold cyan]| |_| | |  | | |\\  || | ___) | | / ___ \\ [/bold cyan]
[bold cyan] \\___/|_|  |_|_| \\_|___|____/___/_/   \\_\\[/bold cyan]

[bold green]🤖 Sistema Integrado de IA Multimodal[/bold green]
[dim]Integrated Multimodal AI System[/dim]

[bold]Versão:[/bold] {SYSTEM_INFO['version']}
[bold]Autor:[/bold] {SYSTEM_INFO['author']}
[bold]Email:[/bold] {SYSTEM_INFO['email']}
[bold]Build:[/bold] {SYSTEM_INFO['build_date']}
"""

    console.print(Panel(banner_text, border_style="cyan", padding=(1, 2)))


def display_features():
    """Exibe as funcionalidades do sistema"""
    features = """
[bold green]🎯 Funcionalidades Principais / Main Features:[/bold green]

[bold cyan]🤖 Modelos de IA / AI Models:[/bold cyan]
• DeepSeek R1 (Recomendado/Recommended)
• Llama 3.1 8B, Mistral 7B, CodeLlama
• OpenAI GPT-4, Anthropic Claude, Google Gemini
• AWS Bedrock, Azure OpenAI

[bold cyan]🎓 Treinamento / Training:[/bold cyan]
• LoRA Fine-tuning avançado
• Treinamento distribuído (DeepSpeed, FSDP)
• Suporte para datasets customizados
• Integração com Kaggle, SageMaker

[bold cyan]💾 Banco de Dados / Databases:[/bold cyan]
• PostgreSQL (Produção)
• MongoDB (NoSQL)
• Redis (Cache)
• SQLite (Desenvolvimento)
• DynamoDB (AWS)

[bold cyan]🌐 Protocolos Remotos / Remote Protocols:[/bold cyan]
• FTP/SFTP para transferência de arquivos
• HTTP/HTTPS para downloads
• WebDAV para sincronização
• APIs REST para integração

[bold cyan]📊 Interface / Interface:[/bold cyan]
• Streamlit Web UI intuitiva
• Jupyter Notebooks integrado
• Chat com assistente IA
• Dashboard de monitoramento

[bold cyan]🔧 Processamento / Processing:[/bold cyan]
• OCR multiidioma (Tesseract)
• Speech-to-Text (Whisper)
• Processamento de vídeo
• Análise de documentos
"""

    console.print(Panel(features, border_style="green", padding=(1, 2)))


@app.command()
def info():
    """📋 Exibe informações do sistema / Show system information"""
    display_banner()
    display_features()

    # Validar configuração
    errors = validate_config()
    if errors:
        console.print(
            "\n[bold red]⚠️  Avisos de Configuração / Configuration Warnings:[/bold red]"
        )
        for error in errors:
            console.print(f"  • [yellow]{error}[/yellow]")
    else:
        console.print(
            "\n[bold green]✅ Configuração validada com sucesso![/bold green]"
        )


@app.command()
def web(
    host: str = typer.Option(FRONTEND_HOST, "--host", "-h", help="Host do servidor"),
    port: int = typer.Option(FRONTEND_PORT, "--port", "-p", help="Porta do servidor"),
    dev: bool = typer.Option(False, "--dev", help="Modo desenvolvimento"),
):
    """🌐 Iniciar interface web / Start web interface"""
    console.print(
        f"[bold green]🚀 Iniciando interface web em http://{host}:{port}[/bold green]"
    )

    try:
        import subprocess

        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "web/frontend.py",
            "--server.address",
            host,
            "--server.port",
            str(port),
        ]

        if not dev:
            cmd.extend(["--server.headless", "true"])

        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Interface web encerrada[/yellow]")
    except ImportError:
        console.print(
            "[red]❌ Streamlit não instalado. Execute: pip install streamlit[/red]"
        )
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar interface web: {e}[/red]")


@app.command()
def api(
    host: str = typer.Option(API_HOST, "--host", "-h", help="Host da API"),
    port: int = typer.Option(API_PORT, "--port", "-p", help="Porta da API"),
    reload: bool = typer.Option(
        DEVELOPMENT_MODE, "--reload", help="Auto-reload em desenvolvimento"
    ),
):
    """🔌 Iniciar servidor da API / Start API server"""
    console.print(f"[bold green]🚀 Iniciando API em http://{host}:{port}[/bold green]")

    try:
        import uvicorn
        from web.api import app as api_app

        uvicorn.run(
            api_app,
            host=host,
            port=port,
            reload=reload,
            log_level="debug" if DEBUG_MODE else "info",
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 API encerrada[/yellow]")
    except ImportError:
        console.print(
            "[red]❌ Uvicorn não instalado. Execute: pip install uvicorn[/red]"
        )
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar API: {e}[/red]")


@app.command()
def jupyter(
    host: str = typer.Option(
        JUPYTER_CONFIG["host"], "--host", "-h", help="Host do Jupyter"
    ),
    port: int = typer.Option(
        JUPYTER_CONFIG["port"], "--port", "-p", help="Porta do Jupyter"
    ),
    token: Optional[str] = typer.Option(
        JUPYTER_CONFIG.get("token"), "--token", help="Token de acesso"
    ),
):
    """📓 Iniciar Jupyter Lab / Start Jupyter Lab"""
    console.print(
        f"[bold green]🚀 Iniciando Jupyter Lab em http://{host}:{port}[/bold green]"
    )

    try:
        import subprocess

        cmd = [
            sys.executable,
            "-m",
            "jupyter",
            "lab",
            "--ip",
            host,
            "--port",
            str(port),
            "--no-browser",
            "--allow-root" if JUPYTER_CONFIG["allow_root"] else "",
        ]

        if token:
            cmd.extend(["--ServerApp.token", token])

        # Filtrar argumentos vazios
        cmd = [arg for arg in cmd if arg]

        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Jupyter Lab encerrado[/yellow]")
    except ImportError:
        console.print(
            "[red]❌ Jupyter não instalado. Execute: pip install jupyterlab[/red]"
        )
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar Jupyter: {e}[/red]")


@app.command()
def train(
    model: str = typer.Option(
        "deepseek-r1", "--model", "-m", help="Modelo para treinamento"
    ),
    dataset: str = typer.Option("", "--dataset", "-d", help="Caminho do dataset"),
    epochs: int = typer.Option(3, "--epochs", "-e", help="Número de épocas"),
    batch_size: int = typer.Option(2, "--batch-size", "-b", help="Tamanho do batch"),
):
    """🎓 Iniciar treinamento LoRA / Start LoRA training"""
    if not dataset:
        console.print(
            "[red]❌ Dataset obrigatório. Use --dataset /caminho/para/dataset[/red]"
        )
        return

    console.print(f"[bold green]🎓 Iniciando treinamento LoRA[/bold green]")
    console.print(f"[cyan]📦 Modelo:[/cyan] {model}")
    console.print(f"[cyan]📊 Dataset:[/cyan] {dataset}")
    console.print(f"[cyan]📈 Épocas:[/cyan] {epochs}")
    console.print(f"[cyan]📦 Batch Size:[/cyan] {batch_size}")

    try:
        from modelos.treinamento import iniciar_treinamento_lora

        asyncio.run(
            iniciar_treinamento_lora(
                model_name=model,
                dataset_path=dataset,
                epochs=epochs,
                batch_size=batch_size,
            )
        )

        console.print("[bold green]✅ Treinamento concluído com sucesso![/bold green]")

    except ImportError as e:
        console.print(f"[red]❌ Erro de importação: {e}[/red]")
        console.print(
            "[yellow]Verifique se todas as dependências estão instaladas[/yellow]"
        )
    except Exception as e:
        console.print(f"[red]❌ Erro durante treinamento: {e}[/red]")


@app.command()
def chat():
    """💬 Iniciar chat interativo / Start interactive chat"""
    console.print("[bold green]💬 Chat Interativo OmnisIA[/bold green]")
    console.print("[dim]Digite 'exit' para sair[/dim]\n")

    try:
        from agentes.assistente import AssistenteIA

        assistente = AssistenteIA()

        while True:
            try:
                pergunta = input("👤 Você: ")
                if pergunta.lower() in ["exit", "quit", "sair"]:
                    break

                if pergunta.strip():
                    resposta = asyncio.run(assistente.responder(pergunta))
                    console.print(f"🤖 [bold cyan]OmnisIA:[/bold cyan] {resposta}")

            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]❌ Erro: {e}[/red]")

        console.print("\n[yellow]👋 Chat encerrado![/yellow]")

    except ImportError:
        console.print("[red]❌ Módulo de chat não disponível[/red]")
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar chat: {e}[/red]")


@app.command()
def setup():
    """🔧 Configurar sistema / Setup system"""
    console.print("[bold green]🔧 Configurando OmnisIA...[/bold green]")

    try:
        # Verificar dependências
        console.print("📋 Verificando dependências...")

        # Criar diretórios necessários
        from config import DIRECTORIES_TO_CREATE

        console.print("📁 Criando diretórios...")

        for directory in DIRECTORIES_TO_CREATE:
            directory.mkdir(parents=True, exist_ok=True)
            console.print(f"  ✅ {directory}")

        # Validar configuração
        console.print("⚙️  Validando configuração...")
        errors = validate_config()

        if errors:
            console.print("\n[yellow]⚠️  Avisos encontrados:[/yellow]")
            for error in errors:
                console.print(f"  • {error}")
        else:
            console.print("  ✅ Configuração válida")

        console.print("\n[bold green]✅ Setup concluído![/bold green]")
        console.print("\n[cyan]Próximos passos:[/cyan]")
        console.print("1. Configure as variáveis de ambiente no arquivo .env")
        console.print("2. Execute: omnisia web (para interface web)")
        console.print("3. Execute: omnisia api (para servidor API)")
        console.print("4. Execute: omnisia info (para mais informações)")

    except Exception as e:
        console.print(f"[red]❌ Erro durante setup: {e}[/red]")


@app.command()
def status():
    """📊 Status do sistema / System status"""
    console.print("[bold green]📊 Status do Sistema OmnisIA[/bold green]\n")

    # Informações básicas
    console.print(f"[bold]Versão:[/bold] {SYSTEM_INFO['version']}")
    console.print(
        f"[bold]Modo Desenvolvimento:[/bold] {'✅ Ativo' if DEVELOPMENT_MODE else '❌ Inativo'}"
    )
    console.print(
        f"[bold]Modo Debug:[/bold] {'✅ Ativo' if DEBUG_MODE else '❌ Inativo'}"
    )

    # Status dos diretórios
    console.print("\n[bold cyan]📁 Diretórios:[/bold cyan]")
    from config import DIRECTORIES_TO_CREATE

    for directory in DIRECTORIES_TO_CREATE:
        status = "✅ OK" if directory.exists() else "❌ Não encontrado"
        console.print(f"  {directory.name}: {status}")

    # Validação da configuração
    console.print("\n[bold cyan]⚙️  Configuração:[/bold cyan]")
    errors = validate_config()

    if not errors:
        console.print("  ✅ Configuração válida")
    else:
        console.print("  ⚠️  Avisos encontrados:")
        for error in errors:
            console.print(f"    • {error}")


@app.command()
def full(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host dos serviços"),
    web_port: int = typer.Option(
        FRONTEND_PORT, "--web-port", help="Porta da interface web"
    ),
    api_port: int = typer.Option(API_PORT, "--api-port", help="Porta da API"),
    jupyter_port: int = typer.Option(
        JUPYTER_CONFIG["port"], "--jupyter-port", help="Porta do Jupyter"
    ),
):
    """🚀 Iniciar todos os serviços / Start all services"""
    console.print("[bold green]🚀 Iniciando todos os serviços OmnisIA...[/bold green]")

    import subprocess
    import time

    processes = []

    try:
        # Iniciar API
        console.print(f"[cyan]🔌 Iniciando API na porta {api_port}...[/cyan]")
        api_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "web.api:app",
                "--host",
                host,
                "--port",
                str(api_port),
            ]
        )
        processes.append(("API", api_process))
        time.sleep(2)

        # Iniciar Web Interface
        console.print(f"[cyan]🌐 Iniciando interface web na porta {web_port}...[/cyan]")
        web_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "web/frontend.py",
                "--server.address",
                host,
                "--server.port",
                str(web_port),
                "--server.headless",
                "true",
            ]
        )
        processes.append(("Web", web_process))
        time.sleep(2)

        # Iniciar Jupyter (opcional)
        try:
            console.print(
                f"[cyan]📓 Iniciando Jupyter na porta {jupyter_port}...[/cyan]"
            )
            jupyter_process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "jupyter",
                    "lab",
                    "--ip",
                    host,
                    "--port",
                    str(jupyter_port),
                    "--no-browser",
                    "--allow-root",
                ]
            )
            processes.append(("Jupyter", jupyter_process))
        except FileNotFoundError:
            console.print("[yellow]⚠️  Jupyter não encontrado, pulando...[/yellow]")

        console.print("\n[bold green]✅ Todos os serviços iniciados![/bold green]")
        console.print(f"[cyan]🌐 Interface Web:[/cyan] http://{host}:{web_port}")
        console.print(f"[cyan]🔌 API:[/cyan] http://{host}:{api_port}")
        console.print(f"[cyan]📓 Jupyter:[/cyan] http://{host}:{jupyter_port}")
        console.print("\n[dim]Pressione Ctrl+C para parar todos os serviços[/dim]")

        # Aguardar interrupção
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Parando todos os serviços...[/yellow]")

        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                console.print(f"  ✅ {name} parado")
            except subprocess.TimeoutExpired:
                process.kill()
                console.print(f"  ⚠️  {name} forçado a parar")
            except Exception as e:
                console.print(f"  ❌ Erro ao parar {name}: {e}")

        console.print("[green]👋 Todos os serviços foram encerrados[/green]")


def main():
    """Função principal"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 OmnisIA encerrado[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Erro: {e}[/red]")
        if DEBUG_MODE:
            raise


if __name__ == "__main__":
    main()
