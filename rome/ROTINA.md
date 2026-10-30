# Roma sem sentido — rotina automática (Claude + Metricool)

Roda às segundas, quartas e sextas, às 08:47 de Brasília, sem aprovação humana. Publica tudo sozinha: nada de rascunho. World in Brief Daily NÃO faz parte desta rotina (usa Make e fica intacto).

## Contas e fixos
- Blog: romasemsentido.wordpress.com (conector WordPress.com, site 258191074, português do Brasil, categoria 32176).
- Instagram: @romasemsentido no Metricool, brand 7761146, fuso Europe/Rome.
- Repositório: Vanclock/wib-slides (add_repo com acesso push; clonar uma vez). Slides ficam em `rome/AAAA-MM-DD/NN.jpg` e `story-NN.jpg`, servidos em `https://raw.githubusercontent.com/Vanclock/wib-slides/main/rome/AAAA-MM-DD/NN.jpg`.
- Lista cronológica: `rome/plano-editorial.xlsx` (aba "Linha do tempo", 1.066 pontos). Estado: `rome/estado.json` (campo `proximo`).
- Guia de estilo: `rome-style-abnt.md`. Estilo dos slides: `tools/gen_rome.py` (não alterar). Modelo do post: post n.º 46 (id 30, `posts.get`).

## Passo a passo (nesta ordem)
0. Preparar: add_repo + clone; `sh tools/setup.sh`. Se `rome/plano-editorial.xlsx` não existir, PARAR e avisar no resumo final: não inventar lista.
1. Ler `rome/estado.json` e o ponto `proximo` na planilha (título provisório, era, local da dica prática). Conferir no blog (`posts.list`, busca pelo título) que o ponto ainda não foi publicado. Se já foi, avançar para o seguinte e corrigir o estado.
2. Pesquisar em fontes confiáveis (fontes clássicas, obras acadêmicas, instituições como museus e Roma Capitale). Só citar obra verificada; sem fonte, não afirmar como fato. Linguagem para o público geral, não 100% acadêmica.
3. PRIMEIRO publicar no WordPress (`posts.create`, status publish, categoria 32176, com `user_confirmed: true`). Copiar a estrutura do post n.º 46: abertura ligando ao post anterior; seções H2; imagens com "Figura N – descrição" e "Fonte: AUTOR, ano, via Wikimedia Commons (licença)"; seção "O que dizem os historiadores"; "Dica prática: onde ver esse pedaço de Roma" com lista em negrito e link "Ver no Google Maps" (`https://www.google.com/maps/search/?api=1&query=...`); aviso para conferir horários e ingressos no site oficial; "No próximo capítulo"; "Referências" em ABNT, ordem alfabética. Sempre incluir imagens (mínimo 4 e imagem de destaque), só de fontes livres (Wikimedia Commons, domínio público ou CC) com crédito. Enviar as imagens à biblioteca de mídia do blog e inserir no post. Datas e abreviaturas como no guia ABNT.
4. Slides: montar `spec` no formato de `examples/spec-rome-example.json` (capa + 4 slides de história + "onde ver" + dica + encerramento = 8), texto só com o que está no post publicado, citações ABNT. Rodar `python3 tools/gen_rome.py spec.json`, conferir pelo menos capa, um slide de texto e o de local, copiar `rs-NN.jpg` para `rome/AAAA-MM-DD/NN.jpg` (AAAA-MM-DD = data da publicação do carrossel), commit e push na main (`git fetch origin main` e rebase antes do push).
5. Instagram (Metricool, `createScheduledPost`, NÃO rascunho: `"draft": false`, `"autoPublish": true`): carrossel com as 8 URLs raw, `instagramData.type = POST`, às **19:00 de Brasília do mesmo dia**. Legenda: título, 2 frases de gancho, "Onde ver:" com cascata numerada e link do Google Maps de cada local, aviso de horários, "Texto completo com todas as fontes: link na bio.", fontes resumidas, até 5 hashtags.
6. Stories (dia seguinte): `python3 tools/make_stories.py rome/AAAA-MM-DD 7`, commit e push. Agendar 7 stories com `createScheduledPost` (`instagramData.type = STORY`, sem texto, 1 slide cada, slides 1 a 7 em ordem), no dia seguinte, nos horários de Brasília: 06:45, 08:30, 11:30, 13:30, 14:30, 18:45, 20:30.
7. Conversão de horário: SEMPRE converter de Brasília (America/Sao_Paulo, UTC-3 fixo) para Europe/Rome com `zoneinfo` do Python, porque o Metricool usa o fuso de Roma e o horário de verão europeu muda em março e outubro. Nunca agendar no passado.
8. Atualizar `rome/estado.json` (próximo = n + 1; registrar data do blog, do carrossel e dos stories), commit e push. Conferir com `getScheduledPosts` que o carrossel e os 7 stories estão agendados.

## Regras
- Nada de rascunho e nada de pedir aprovação: a decisão de publicar é desta rotina.
- Não mudar a arquitetura nem o estilo (slides, legenda, estrutura do post). Não tocar no World in Brief Daily.
- Antes de qualquer publicação, checar duplicidade (blog e Metricool no mesmo dia). Em erro de uma etapa, não repetir o que já foi publicado: relatar e seguir só com o que falta.
- Resumo final curto: ponto publicado (n.º e título), link do post, horário do carrossel e dos stories, e qualquer falha.
