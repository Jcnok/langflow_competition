# Desafio 1:

## Desafio Semana 1 - Prompt Engineering

**🗓️ Objetivo**

Criar uma implementação no Langflow que processe um arquivo de texto fornecido, extraia o conteúdo do artigo e gere um resumo conciso e abrangente.

**✅ Requisitos**

1. O resumo deve ser o mais sucinto possível (curto em número de caracteres).
2. O resumo deve ser rico em conteúdo, contendo definições e vocabulário dos tópicos principais.
3. A saída do chat deve exibir apenas o resumo do artigo.
4. É obrigatório utilizar pelo menos um componente `Prompt` e um componente `LLM`.

🔎 **Flow de referência**

O projeto abaixo será utilizado como referência para criação do resumo e avaliação. A figura abaixo ilustra o flow com o objetivo do desafio, onde o output será criar um resumo do conteúdo do arquivo:

![https://framerusercontent.com/images/C1nZOgRCNjCA9K5ifVGwv2RWdAg.png?scale-down-to=2048](https://framerusercontent.com/images/C1nZOgRCNjCA9K5ifVGwv2RWdAg.png?scale-down-to=2048)

A ilustração abaixo demonstra como o resumo será avaliado, onde você pode simular o score do seu projeto:

![https://framerusercontent.com/images/unQevH9RDUrQzv19e05Hn2BcGTs.png?scale-down-to=1024](https://framerusercontent.com/images/unQevH9RDUrQzv19e05Hn2BcGTs.png?scale-down-to=1024)

Ao rodar o flow com todos o componentes conectados você verá um output com o resumo do texto extraído e o score de avaliação.

Abaixo estão o flow de referência e o arquivo com conteúdo a resumir:

📝 **Metodologia de Avaliação**

A avaliação da qualidade do resumo será realizada em duas etapas:

1. **Score Inicial**: computa-se a `similaridade contextual` com o artigo original.
2. **Score Final**: aplica-se um `fator de redução` para penalizar resumos longos, diminuindo o Score Inicial.

**Similaridade Contextual**

- Mede-se a similaridade contextual entre trechos relevantes do texto original e o resumo utilizando **cosine similarity**.
- Vetores de embeddings são gerados tanto para o texto original quanto para o resumo.
- Quanto mais similares os dois vetores, maior a pontuação inicial.

`embedding1 = np.array(embedding_model.embed_query(text1))embedding2 = np.array(embedding_model.embed_query(text2))# Calculate cosine similaritydot_product = np.dot(embedding1, embedding2)norm1 = np.linalg.norm(embedding1)norm2 = np.linalg.norm(embedding2)similarity = dot_product / (norm1 * norm2)`

**Ajuste pelo Comprimento do Resumo**

- Após calcular a pontuação inicial, aplica-se uma penalização para resumos mais longos.
- Resumos mais curtos recebem uma menor penalização, resultando em uma pontuação final mais alta.
- Esta parte incentiva a concisão, favorecendo resumos que sejam tanto informativos quanto breves.

`max_chars = 10000 # Limite máximo de caracteresmin_score = 0.0 # Score mínimo max_score = 1.0 # Score máximotamanho_resumo = len(resumo)if tamanho_resumo >= max_chars: score_final = min_score else: fator_reducao = (max_chars - tamanho_resumo) / max_chars score_final = score_inicial * fator_reducao score_final = max(min_score, min(max_score, score_final))`

‼️ Lembre-se que a geração de texto por modelos de linguagem pode não ser reproduzível. Seu score oficial não necessariamente será exatamente o mesmo da simulação.

**🏆 Premiação**

Os prêmios da semana 1 serão distribuídos para os primeiros 50 ranqueados, conforme a tabela abaixo:

![https://framerusercontent.com/images/eZ6StI2Vm5QuEdmnA9cHnXDPIZY.png?scale-down-to=1024](https://framerusercontent.com/images/eZ6StI2Vm5QuEdmnA9cHnXDPIZY.png?scale-down-to=1024)

- Score: Score de 0 a 1 computado a partir do algoritmo de avaliação do desafio 1.
- Ticket: Os vencedores receberão um ticket para participar do desafio final - semana 4.
- Gift Cards: mais informações em breve.

**🏅 Premiação Adicional**

Serão distribuídos prêmios extras de R$500 para os 5 melhores conteúdos produzidos e submetidos oficialmente durante a semana 1.

- Vídeos, shorts ou tutoriais sobre o projeto, a competição ou o Langflow em geral.
- Ao produzir seu video, utilize as *hashtags #langflow #iadevs* para localizarmos o seu conteúdo. No formulário você pode inserir o link do seu video.
- A avaliação do conteúdo ocorrerá de forma subjetiva pelos organizadores, considerando fatores como a qualidade, a divulgação e o alcance do material produzido em diversas plataformas.

**🚀 Submissão**

- Todas as submissões devem ser feitas através do formulário: [https://forms.gle/ZY9BSJ8AckxGyyxQ7](https://forms.gle/ZY9BSJ8AckxGyyxQ7)
- **Obrigatório:** Arquivo JSON (flow) do projeto, exportado sem API Key.
- **Opcional:** Criação de Conteúdo
- A submissão do projeto pode acontecer várias vezes por participante. Mas apenas a última submissão será considerada.
    
    ❗**O Langflow é Open-Source e sem fins lucrativos!** A submissão dos flows é exclusivamente para a avaliação. O objetivo da competição é fomentar a comunidade Open-Source no Brasil e ensinar métodos modernos de desenvolvimento. Não existe nenhum interesse comercial nos projetos.
    

**📅 Datas importantes**

- 08/07/2024: Live de Lançamento da competição no [Crowdcast](https://www.crowdcast.io/c/rx3ylk3ntbg8)
- 10/07/2024: Sessão ao vivo com o time do Langflow
- 12/07/2024: Prazo final para submissão (23:59)
- 15/07/2024: Divulgação dos vencedores e anúncio do próximo desafio.