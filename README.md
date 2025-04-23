Startup Rush 🚀

📌 Visão Geral

Sistema de simulação de torneio entre startups desenvolvido para o projeto PUCRS/DELL IT Academy 2025

✨ Funcionalidades

    ✅ Cadastro de startups (nome, slogan, ano de fundação)
    ✅ Sistema de torneio com rodadas eliminatórias
    ✅ Aplicação de eventos especiais durante as batalhas
    ✅ Mecanismo de desempate ("Shark Fight")
    ✅ Visualização do ranking completo
    ✅ Interface gráfica intuitiva
    ✅ Validação de dados de entrada

📋 Requisitos do Sistema

    - Python 3.8 ou superior
    - Bibliotecas padrão do Python (tkinter, random, datetime)
  
🚀 Instalação e Execução
    
    1ª Forma de execução: Execução direta

        1 - Certifique-se de ter o Python instalado
        2 - Baixe os arquivos do projeto
        3 - Execute o arquivo principal: python main.py
    
    2ª Forma de execução: Usando ambiente virtual (recomendado)

        1 - Crie um ambiente virtual com o comando: python -m venv venv
        2 - Ative o ambiente virtual:
            - Windows: venv\Scripts\activate
            - Linux/Mac: source venv/bin/activate
        3 - Execute o programa com o comando: python main.py

🎮  Como Usar

    #1 - Cadastro de startups

        - Preencha os campos: 
          - Name: Nome da startup (obrigatório). Aceita espaços e caracteres simples, como ".,!?&-'"
          - Slogan: Slogan da startup (obrigatório). Aceita espaços e caracteres simples, como ".,!?&-'"
          - Foundation Year: Ano de fundação da startup (entre 2010 e o ano atual)
        - Clique em "Register Startup" (ou pressione Enter)
        - !ATENÇÃO! É permitido um número mínimo de 4 startups e um número máximo de 8 startups!
        - Não é permitido o cadastro de um número ímpar de startups
  
    #2 - Início do torneio

        - Com ao menos 4 startups cadastradas, o botão "Start tournament" ficará disponível
        - Clique no botão para iniciar o torneio
        - O sistema irá sortear automaticamente os pares para as batalhas da primeira rodada
        - O sistema irá mudar da aba de cadastro para a aba de torneio
    
    #3 - Administração das batalhas

        - Na aba "tournament"
          - Alicar evento:
            - Selecione uma batalha, clicando em cima dela com o botão direito do mouse
            - Uma tela de aplicação de eventos será aberta
            - Escolha a startup entre as opções
            - Selecione o evento, clicando em cima do nome com o botão direito do mouse
            - Clique em "Apply Event"
            - O evento será aplicado à startup e aparecerá uma mensagem de confirmação
            - !ATENÇÃO! Um evento só pode ser aplicado uma vez à uma startup por rodada
          
          - Finalizar batalha(s)
            - Selecione uma batalha, clicando em cima dela com o botão direito do mouse
            - Clique em "Resolve Battle"
            - O sistema irá finalizar a batalha e determinar o vencedor
            - Quando não sobrarem mais batalhas, o sistema sorteia novamente os pares para a próxima rodada
            - Repita o processo até restar apenas um vencedor
            - O sistema irá abrir uma janela mostrando o nome do vencedor, seu slogan e seus pontos acumulados
          
          - Visualizar ranking
            - Clique em "View Ranking"
            - O sistema irá mostrar a classificação atual ordenada pelos pontos 

    #4 📊 Eventos disponíveis
   
        🎤 Pitch: +6 pontos
        🐛 Bugs: -4 pontos
        📈 Traction: +3 pontos
        🤬 Angry Investors: -6 pontos
        📰 Fake News: -8 pontos

🏆 Regras do Torneio

    - Cada startup começa com 70 pontos
    - À startup vitoriosa são concedidos 30 pontos adicionais
    - Em caso de empate é realizado um "Shark Fight":
      - As startups são sorteadas
      - A vencedora recebe +2 pontos

🔄 Fluxo do Torneio com Número Ímpar de startups (Bye)

    - O sistema implementa um mecanismo para lidar com torneios onde temos um número ímpar de startups competindo em uma rodada
    - O objetivo é não interromper abruptamente a execução e garantir a continuidade do torneio
    
    📊 Como funciona o mecanismo de Byes?
        - Ao final de cada rodada, o sistema verifica se o número de startups vencedoras é ímpar
        - Exemplo: em um torneio com 6 startups, 3 vencedores avançam para a rodada seguinte
        - O sistema identifica a startup com maior pontuação e concede o "Bye" com base nos seguintes critérios de desempate:
          1 - Maior pontuação
          2 - Menor número de byes concedidos anteriormente
          3 - Sorteio, para casos de desempate
        - O bye é concedido e a startup selecionada avança para a próxima rodada
        - Seu contador de byes é incrementado em +1
        - As startups restantes são pareadas normalmente 

📝 Licença

    - Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.

⚠️ Considerações importantes

    - Não há persistência de dados alguma, o que significa que os dados são perdidos ao fechar o programa
    - Há um limite máximo de 8 startups por torneio
    - Uma startup pode receber múltiplos byes durante o torneio

📂 Estrutura de arquivos

startup_rush/
├── main.py            # Classe principal
├── models/
│   ├── __init__.py
│   ├── battle.py      # Classe de batalhas
│   ├── rush.py        # Classe de torneios
│   └── startup.py     # Classe de startups
├── README.md          # Este arquivo
├── .gitignore         # Arquivo para ignorar no Git
└── LICENSE            # Licença do projeto