# Just-Pente

# Instruções para Executar o Projeto

Bem-vindo ao projeto Just Pente! Este repositório contém os arquivos necessários para executar a interface Unity juntamente com o rastreamento de pose em Python. Siga as etapas abaixo para configurar e rodar as diferentes partes do projeto.

## Parte do Unity (Interface)

1. **Importar o Projeto no Unity Hub:**
   - Abra o Unity Hub (certifique-se de ter instalado o Unity previamente).
   - Clique em "Add" e selecione a pasta contendo este repositório.
   - Aguarde enquanto o Unity importa os arquivos.

2. **Carregar a Cena:**
   - Após a importação, navegue até a pasta do projeto no Unity Hub e abra-o.
   - No Unity, navegue até a pasta de cenas e abra o arquivo "menu". Isso carregará a página inicial do projeto, através da qual você acessa as outras.

## Parte do Python (Rastreamento de Pose)

1. **Executar a Geração de Arquivos TXT:**
   - Navegue até a pasta do projeto no terminal.
   - Execute o arquivo "main.py" para gerar arquivos "txt" necessários para o Unity.
     ```
     python main.py
     ```

2. **Executar o Rastreamento de Pose e Geração da Pontuação:**
   - Certifique-se de ter o Python instalado em sua máquina (versão recomendada: Python 3.11).
   - Execute o arquivo "StreamFlow.py" para iniciar o rastreamento de pose usando a webcam e enviar a pontuação, que define a similaridade do que é detectado pela webcam com os videos da coreografias, para o Unity.
     ```
     python StreamFlow.py
     ```

3. **Integração com Unity:**
   - Com o rastreamento de pose sendo executado, ele enviará o resultado da comparação de poses para o Unity em tempo real. Certifique-se de que o Unity também esteja em execução.

## Observações Importantes

- Certifique-se de ter todas as dependências necessárias instaladas, incluindo as bibliotecas Python requeridas para o rastreamento de pose.
- Este projeto pode exigir ajustes dependendo da sua configuração de hardware e software.
- Caso encontre problemas ou queira fazer melhorias, sinta-se à vontade para contribuir com o projeto ou entrar em contato com os mantenedores.

Agora você está pronto para rodar o projeto Just Pente! Divirta-se dançando e explorando a interação entre a interface Unity e o rastreamento de pose em Python.
