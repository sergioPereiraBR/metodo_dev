#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seletor de Método de Desenvolvimento de Software - CLI
Um aplicativo interativo que guia o usuário através de perguntas fechadas
para recomendar o método de desenvolvimento mais adequado.
"""

import sys


def print_header():
    """Exibe o cabeçalho do aplicativo."""
    print("=" * 60)
    print("  SELETOR DE MÉTODO DE DESENVOLVIMENTO DE SOFTWARE")
    print("=" * 60)
    print("Responda às perguntas para descobrir o método ideal.\n")


def ask_question(question_text, options):
    """
    Faz uma pergunta e retorna a resposta do usuário.

    Args:
        question_text: Texto da pergunta
        options: Lista de tuplas (valor, texto_exibido)

    Returns:
        O valor da opção escolhida
    """
    print(f"\n{'─' * 60}")
    print(f"❓ {question_text}")
    print(f"{'─' * 60}")

    for i, (value, text) in enumerate(options, 1):
        print(f"   [{i}] {text}")

    while True:
        try:
            choice = input("\n👉 Escolha uma opção: ").strip()

            # Verifica se é um número válido
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx][0]

            # Verifica se é a letra da opção (S/N)
            choice_upper = choice.upper()
            for value, text in options:
                if choice_upper == value:
                    return value

            print("⚠️  Opção inválida. Tente novamente.")

        except (EOFError, KeyboardInterrupt):
            print("\n\n❌ Operação cancelada pelo usuário.")
            sys.exit(0)


def print_result(method, description, practices=None):
    """
    Exibe o resultado final com formatação.

    Args:
        method: Nome do método recomendado
        description: Descrição do método
        practices: Lista de práticas complementares (opcional)
    """
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " RESULTADO FINAL ".center(58) + "║")
    print("╠" + "═" * 58 + "╣")

    # Quebra o nome do método em linhas se for muito longo
    method_lines = [method[i:i+54] for i in range(0, len(method), 54)]
    for line in method_lines:
        print("║" + f"  🏆 {line}".ljust(58) + "║")

    print("╠" + "═" * 58 + "╣")

    # Descrição com quebra de linha
    desc_words = description.split()
    desc_lines = []
    current_line = "  📋 "
    for word in desc_words:
        if len(current_line) + len(word) + 1 > 56:
            desc_lines.append(current_line)
            current_line = "      " + word + " "
        else:
            current_line += word + " "
    desc_lines.append(current_line)

    for line in desc_lines:
        print("║" + line.ljust(58) + "║")

    if practices:
        print("║" + " " * 58 + "║")
        print("║" + "  🔧 Práticas Complementares:".ljust(58) + "║")
        for practice in practices:
            practice_lines = [practice[i:i+50] for i in range(0, len(practice), 50)]
            for i, pline in enumerate(practice_lines):
                prefix = "     • " if i == 0 else "       "
                print("║" + f"{prefix}{pline}".ljust(58) + "║")

    print("╚" + "═" * 58 + "╝")
    print("\n")


def ask_continue():
    """Pergunta se o usuário deseja reiniciar."""
    print("\n" + "─" * 60)
    choice = input("🔄 Deseja realizar uma nova consulta? (S/N): ").strip().upper()
    return choice == "S"


# ═══════════════════════════════════════════════════════════════
# FLUXO DE DECISÃO
# ═══════════════════════════════════════════════════════════════

def nivel_1():
    """Nível 1: Contexto do Projeto"""
    resposta = ask_question(
        "Q1. Os requisitos do projeto são estáveis e bem definidos desde o início?",
        [("S", "Sim — Requisitos claros e pouco mutáveis"),
         ("N", "Não — Requisitos incertos ou sujeitos a mudanças")]
    )

    if resposta == "S":
        return nivel_1a_criticidade()
    else:
        return nivel_2_flexibilidade()


def nivel_1a_criticidade():
    """Q2: Alta criticidade / regulamentação"""
    resposta = ask_question(
        "Q2. O projeto possui alta criticidade e/ou requer conformidade regulatória rigorosa?",
        [("S", "Sim — Software crítico (médico, aeroespacial, financeiro regulado)"),
         ("N", "Não — Projeto comum sem restrições regulatórias especiais")]
    )

    if resposta == "S":
        return print_result(
            "Waterfall / V-Model / Cleanroom",
            "Modelos sequenciais com forte ênfase em documentação, verificação formal e conformidade. Cada fase é concluída antes da próxima iniciar. Ideal para sistemas críticos onde erros são inaceitáveis.",
            ["Documentação extensiva", "Revisões formais", "Testes de aceitação rigorosos", "Métodos formais (opcional)"]
        )
    else:
        return print_result(
            "Cascata Incremental",
            "Combina a estrutura sequencial do Waterfall com entregas incrementais. O sistema é construído em partes funcionais, permitindo feedback parcial sem abandonar o planejamento inicial.",
            ["Documentação por incremento", "Revisões de milestone", "Integração incremental"]
        )


def nivel_2_flexibilidade():
    """Nível 2: Flexibilidade e Velocidade"""
    resposta = ask_question(
        "Q3. O projeto exige entregas frequentes e adaptação rápida a mudanças?",
        [("S", "Sim — Mercado dinâmico, feedback contínuo do cliente"),
         ("N", "Não — Prazos definidos, escopo mais previsível")]
    )

    if resposta == "S":
        return nivel_3_agil()
    else:
        return nivel_4_especificidades()


def nivel_3_agil():
    """Nível 3: Ágil na Prática"""
    resposta = ask_question(
        "Q4. A equipe é pequena (até 9 pessoas) e autônoma?",
        [("S", "Sim — Time enxuto com poder de decisão"),
         ("N", "Não — Equipe grande ou dependente de outras áreas")]
    )

    if resposta == "S":
        return nivel_3a_rigor_tecnico()
    else:
        return nivel_3b_escala()


def nivel_3a_rigor_tecnico():
    """Q6: Rigor técnico"""
    resposta = ask_question(
        "Q6. A equipe precisa de rigor técnico (TDD, pair programming, integração contínua)?",
        [("S", "Sim — Qualidade de código é prioridade máxima"),
         ("N", "Não — Foco em entrega de valor com processo leve")]
    )

    if resposta == "S":
        return print_result(
            "Extreme Programming (XP)",
            "Metodologia ágil com práticas técnicas rigorosas. Enfatiza excelência técnica, simplicidade do design e feedback constante através de testes automatizados e programação em par.",
            ["Test-Driven Development (TDD)", "Programação em Par", "Integração Contínua", "Refatoração constante", "Cliente presente", "Releases frequentes"]
        )
    else:
        return print_result(
            "Scrum",
            "Framework ágil mais adotado mundialmente. Baseado em sprints de 1-4 semanas com papéis definidos (Product Owner, Scrum Master, Dev Team) e eventos estruturados para inspeção e adaptação.",
            ["Sprints fixos", "Daily Stand-ups", "Backlog de Produto", "Sprint Review & Retrospective", "Burndown charts"]
        )


def nivel_3b_escala():
    """Q7: Escala organizacional"""
    resposta = ask_question(
        "Q7. A organização possui múltiplas equipes (mais de 50 pessoas) trabalhando no mesmo produto?",
        [("S", "Sim — Grande empresa com dezenas de desenvolvedores"),
         ("N", "Não — Poucas equipes ou projeto de médio porte")]
    )

    if resposta == "S":
        return print_result(
            "SAFe / LeSS / Nexus",
            "Frameworks para escalar ágil em grandes organizações. Coordenam múltiplas equipes através de estruturas de governança, programas de release e alinhamento estratégico.",
            ["Agile Release Trains (ART)", "Program Increments (PI)", "Scrum of Scrums", "Backlog unificado", "Sincronização entre equipes"]
        )
    else:
        return nivel_3c_fluxo()


def nivel_3c_fluxo():
    """Q8: Trabalho contínuo"""
    resposta = ask_question(
        "Q8. O trabalho é contínuo (manutenção, suporte, operações) sem iterações fixas?",
        [("S", "Sim — Fluxo constante de tarefas sem datas de sprint"),
         ("N", "Não — Trabalho organizado em ciclos de entrega")]
    )

    if resposta == "S":
        return print_result(
            "Kanban",
            "Método visual baseado em fluxo contínuo. Utiliza quadro com colunas e limites de WIP (Work In Progress) para otimizar o throughput e reduzir gargalos. Sem sprints fixos.",
            ["Quadro visual", "Limites de WIP", "Métricas de fluxo (lead time, cycle time)", "Políticas explícitas", "Melhoria contínua (Kaizen)"]
        )
    else:
        return print_result(
            "Scrumban",
            "Híbrido que combina a estrutura de sprints do Scrum com a visualização de fluxo e limites de WIP do Kanban. Ideal para equipes que precisam de previsibilidade com flexibilidade.",
            ["Sprints com visualização Kanban", "Limites de WIP por coluna", "Métricas híbridas", "Flexibilidade de priorização"]
        )


def nivel_4_especificidades():
    """Nível 4: Especificidades Técnicas"""
    resposta = ask_question(
        "Q5. O projeto envolve alto risco técnico ou incertezas significativas?",
        [("S", "Sim — Tecnologia nova, arquitetura inexplorada, requisitos voláteis"),
         ("N", "Não — Tecnologia madura, arquitetura conhecida")]
    )

    if resposta == "S":
        return print_result(
            "Modelo Espiral / Prototipagem Evolutiva",
            "Abordagem iterativa com análise de riscos em cada ciclo. O protótipo evolui para o sistema final através de refinamentos sucessivos baseados em aprendizado e mitigação de riscos.",
            ["Análise de riscos por ciclo", "Protótipos operacionais", "Revisões de milestone", "Documentação evolutiva", "Stakeholder frequente"]
        )
    else:
        return nivel_4a_dominio()


def nivel_4a_dominio():
    """Q9: Domínio complexo"""
    resposta = ask_question(
        "Q9. O domínio do negócio é complexo e central para o design do sistema?",
        [("S", "Sim — Regras de negócio intrincadas, múltiplos contextos"),
         ("N", "Não — Domínio simples ou técnico puro")]
    )

    if resposta == "S":
        return print_result(
            "Domain-Driven Design (DDD) + Método Ágil",
            "DDD é uma abordagem de design que coloca o domínio do negócio no centro da arquitetura. Deve ser combinado com Scrum, Kanban ou XP. Usa linguagem ubíqua, bounded contexts e agregados.",
            ["Linguagem ubíqua", "Bounded Contexts", "Entidades e Value Objects", "Repositórios e Serviços de Domínio", "Event Storming", "Context Mapping"]
        )
    else:
        return nivel_4b_devops()


def nivel_4b_devops():
    """Q10: Automação"""
    resposta = ask_question(
        "Q10. O projeto exige automação de infraestrutura e entrega contínua?",
        [("S", "Sim — Deploy frequente, infraestrutura como código, monitoramento"),
         ("N", "Não — Deploys manuais, infraestrutura tradicional")]
    )

    if resposta == "S":
        return print_result(
            "DevOps / GitOps",
            "Cultura e práticas que integram desenvolvimento e operações. Foca em automação, CI/CD, infraestrutura como código e feedback rápido. GitOps usa Git como fonte única de verdade.",
            ["CI/CD Pipeline", "Infraestrutura como Código (IaC)", "Monitoramento contínuo", "Feature Flags", "GitOps com reconciliação automática", "Shift-left testing"]
        )
    else:
        return print_result(
            "Método Incremental Tradicional",
            "Desenvolvimento em incrementos funcionais com planejamento moderado. Cada incremento adiciona funcionalidade ao produto. Equilíbrio entre previsibilidade e flexibilidade.",
            ["Planejamento por incremento", "Entregas parciais documentadas", "Revisões de milestone", "Gestão de mudanças controlada"]
        )


def nivel_5_dados():
    """Nível 5: Dados e Machine Learning (chamado após qualquer resultado)"""
    resposta = ask_question(
        "Q11. O projeto envolve pipeline de dados ou modelos de machine learning?",
        [("S", "Sim — Processamento de dados, ETL, modelos preditivos"),
         ("N", "Não — Aplicação tradicional sem componente de dados/ML")]
    )

    if resposta == "S":
        return nivel_5a_tipo_dados()
    else:
        print("\n✅ Fluxo de decisão concluído. Método definido acima.")
        return False


def nivel_5a_tipo_dados():
    """Q12: Tipo de projeto de dados"""
    resposta = ask_question(
        "Q12. O foco é operações de dados (ETL, pipelines, qualidade) ou modelos de ML?",
        [("S", "Sim — Operações de dados, pipelines, governança"),
         ("N", "Não — Modelos de machine learning, treinamento, deploy de IA")]
    )

    if resposta == "S":
        print_result(
            "DataOps",
            "Aplica princípios ágeis e DevOps a pipelines de dados. Foca em qualidade, automação, colaboração entre engenheiros de dados e operações. Garante dados confiáveis e disponíveis.",
            ["Pipeline de dados automatizado", "Data Quality Gates", "Versionamento de dados", "Testes de dados", "Observabilidade de pipelines", "Data Catalog"]
        )
    else:
        print_result(
            "MLOps",
            "Extensão do DevOps para o ciclo de vida de modelos de machine learning. Gerencia experimentação, treinamento, implantação, monitoramento de drift e retreinamento automatizado.",
            ["Experiment Tracking", "Model Registry", "Feature Store", "A/B Testing de modelos", "Monitoramento de Model Drift", "Auto-retraining pipelines"]
        )
    return False


# ═══════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def main():
    """Função principal que executa o fluxo de decisão."""
    while True:
        print_header()

        # Executa o fluxo principal (Níveis 1-4)
        nivel_1()

        # Pergunta sobre dados/ML (Nível 5) - opcional para todos os caminhos
        print("\n" + "=" * 60)
        print("  VERIFICAÇÃO ADICIONAL: COMPONENTES DE DADOS/ML")
        print("=" * 60)

        nivel_5_dados()

        if not ask_continue():
            print("\n👋 Obrigado por usar o Seletor de Métodos!")
            print("=" * 60)
            break

        print("\n" * 2)


if __name__ == "__main__":
    main()
