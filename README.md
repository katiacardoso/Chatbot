# Projeto para respostas automatizadas
> Implementado por : Katia Cardoso

Este repositório contém um código para criar um chatbot de perguntas e respostas usando o modelo BERT. 

## Funcionamento

De um modo geral, o funcionamento deste chatbot pode ser visualizado na figura abaixo

![Funcionamento_basico](https://github.com/katiacardoso/EMAP_Chatbot/assets/91233884/1fb53d07-ea40-4eba-9f56-79fd34dee315)

Segue abaixo uma explicação mais detalhada: 

### 1. Carregamento do modelo BERT pré-treinado e o tokenizador

Foi escolhido o modelo [bert-base-multilingual-uncased](https://huggingface.co/bert-base-multilingual-uncased), pois o BERT base demostrou um desempenho em quesito de velocidade maior se comparado com o BERT large e multilingual para entendimento da língua portuguesa. 


  
  - `model_name` : Especifica o modelo escolhido
  - Função `BertModel.from_pretrained()` : Carrega o modelo do arquivo de checkpoint especificado pelo argumento `model_name`
  - Para carregar o tokenizador, você usa a função `BertTokenizer.from_pretrained()`. Esta função carrega o tokenizador do arquivo de vocabulário especificado pelo argumento `model_name`.


### 2. Conversão para formato JSON

Esta conversão foi necessária pensamento em passos posteriores para implementação do Front-End

  - Criação da lista vazia chamada `data` : Ela será utilizada para armazenar os dados convertidos em JSON
  - Itera sobre o conjunto de dados usando o método `iterrows()` do Pandas. : Para cada linha do conjunto de dados, é obtido a pergunta e a resposta da linha. No qual as mesmas serão salvas em variáveis de respectivos nomes
  - Adiciona um dicionário à lista `data` com as chaves `pergunta` e `resposta` e seus valores
  - Após conversão dos dados para JSON, utilizou-se o método `dump()`do módulo JSON para salvar os dados como um arquivo e o método `load()` para carregar os dados no modo 'r' referente a "read" . Para realizar a extração das perguntas e respostas da lista `data`, utilizou-se o método `list()` e um `for` 

- Falar depois em algum canto das perguntas e respostas, que estão em formato csv e cada pergunta tem sua resposta . Perguntas extraidas na página de Perguntas e Respostas do Porto

### 3. Vetorização dos textos em `def vetorizar_texto(texto)`

Esta função só será chamada no próximo passo, na função chatbot(), mas esta separadamente aqui para fins de melhor explicação. Ela recebe uma string como entrada, a pergunta do usuário, e retorna um tensor de embeddings.

  - Usa o tokenizador para quebrar o texto de entrada em tokens e convertê-los em um tensor de números inteiros.
      - `texto`: O texto a ser tokenizado.
      - `return_tensors`: O tipo de tensor a ser retornado pelo tokenizador. O valor `pt` indica que o tokenizador deve retornar um tensor de números inteiros no formato PyTorch
      - `padding`: Se o texto deve ser preenchido para que todos os tensores de entrada tenham o mesmo tamanho. O valor `True` indica que o texto deve ser preenchido.
      - `truncation`: Se o texto deve ser truncado para que todos os tensores de entrada tenham o mesmo tamanho. O valor `True` indica que o texto deve ser truncado.
  
  - Calcula a média dos embeddings. Isto, pensando de outra forma, é uma maneira de representar o significado de um texto como um único vetor
  - Retorna os embeddings das palavras como um tensor.

### 4. Vetorização das perguntas

Aqui é realizada a vetorização das perguntas presentes no dataset original usando o modelo BERT

### 5. Realização da interface em `def chatbot(user_input)` 

Função responsável pela comunicação com o usuário de uma forma minimamente eficaz e buscando a melhor resposta no dataset de perguntas já vetorizadas


  - Chamada para função de vetorização da pergunta do usuário
  - Calculo da similaridade entre o embedding da pergunta do usuário e os embeddings das perguntas do conjunto de dados
  - Encontro do índice da perunta mais semelhante com a função `argmax`
  - Retorno da resposta da pergunta mais semelhante 


- Print da tela de funcionamento

## Para usar o chatbot, siga estas etapas:

- aqui colocar a questão de clonar o repositorio e seguir, entrar em localhost e utilizar 


## Apontamentos para melhoria

A precisão do chatbot pode ser melhorada de várias maneiras, incluindo:
- Refinamenento para responder apenas perguntas relacionadas ao tema do Porto do Itaqui
- Treinar com perguntas mais específicas 

## Agradecimentos

Gostaria de expressar minha sincera gratidão aos meus mentores, ao IFMA pelo apoio e orientação que recebi durante esse período.

Aprendi muito com meus mentores, tanto sobre Inteligência Artificial quanto sobre Processamento de Linguagem Natural. Eles sempre foram pacientes e compreensivos, e sempre me incentivaram a ir além.

O IFMA em parceria com a Softex me proporcionaram uma oportunidade única de aprender e crescer. Sou muito grata por ter tido a oportunidade de participar desse programa.


## Contribuições

Contribuições são bem-vindas. Se você encontrar algum erro ou tiver alguma sugestão, sinta-se à vontade para abrir uma issue ou enviar uma pull request.

