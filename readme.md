# Conceito
O sistema versiona arquivos, não diretórios.

Preciso iniciar o versionamento (git init) (criar a pasta invisivel de versionamento no local do arquivo). 
Depois devo adicionar a versão inicial dentro do versionador.

Para salvar a nova versão eu devo dar um comando tipo save. 
Quando salva, deve pegar a versão anterior e quais linhas (e posições) foram removidas e adicionadas, salvando só isso. 
Cada salvamento também precisa de uma mensagem de epxlicação.

Toda versão salva deve ter um hash, e a partir dele pode ver se foi modificado o arquivo.
Para ver o que foi modificado pode dar um comando que vai mostrar as linhas que foram removidas e adicionadas desde o ultimo salvamento.

Deve haver um comando para exibir a lista com todas as versões anteriores, com data, hash e comentário.
Para voltar pra uma etapa anterior deve-se dar um comando seguido do número de etapas para voltar, ou o hash em questão.

---

# Geral
- [ ] Continuar com a tradução do sistema para inglês, junto com a melhoria das nomenclaturas
- [ ] Adicionar um sistema de compressão e descompressão dos arquivos salvos
- [ ] Fazer o jump saltar também com números para frente ou para trás
- [ ] Modificar os aruquivos salvos para uma lista de linhas removidas e inseridas considerando a versão anterior
- [ ] Adicionar nomes para cada linhagem. A primeira será main, mas toda vez que fizer uma bifurcação deve ser necessário nomea-la

---
# Comandos pendentes

### QUIT
- [ ] Criar o comando QUIT para parar de versionar o arquivo
### TREE
- [ ] Criar o comando TREE para exibir todas as ramificações do projeto de forma visual
  - Deve ser impressa como uma estrutura de diretórios contendo hash e comentário, tendo os filhos abaixo com identação
### NEXT
- [ ] Criar o comando NEXT para ver todas as próximas versões do projeto (inclusive as divisões posteriores)
  - Seria o inverso do prev, mostrandor todas sa versões derivadas a partir da atual (inclusive com as remificações)
### BACK
- [ ] Criar o comando BACK para voltar pra o save indicado e apagar os outros da frente (precisa do encadeamento)
  - Ele faz um jump para o hash indicado e executa trim no filho desse hash que levaria até o current anterior
  - Precisa validar se a versão do hash está dentro do prev do current
  - Além disso, tem que saber como tratar caso no meio do caminho tenha uma ramificação (apagar ou pedir confirmação)
### TRIM 
- [ ] Criar o comando TRIM para apagar um determinado ramo (apagando ramos futuros de forma recurssiva)
  - O trim deve apagar o próprio arquivo que foi indicado, e todos os outros que derivam dele
  - Antes de executar o trim é importante verificar se o current está no cominho, caso ondo o trim não pode ser fito
  - O Comando trim pode ser usado pelo comando back para apagar o filho do hash passado que leva até o current
### MONO
- [ ] Criar o comando MONO apagar todas as ramificações, deixando apenas a da versão que foi informada
  - Basicamente vai executar um prev e um next, e remover todos os saves que não estão dentro dessas rotas
### JOIN
- [ ] Criar um comando JOIN para conseguir unir duas versões de um arquivo em um novo arquivo
  - Será necessário trabalhar na correção de alterações em uma mesma linha
  - Caso os dois arquivos sejam de um mesmo ramo, o arquvo reultante será um novo save neste ramo
- Caso os arquivos sejam de ramos diferentes, o arquivo vai ser um save no maior ramo (como dizer que veio de outro?)

---
# Comandos existentes

### INIT
- Deve realiar a configuração do sistema de versionamento para aquele arquivo em questão
- Caso o arquivo já tenha seu sistema de configuração, o comando é simplesmente ignorado
- A configuração se dá atavés da criação de uma pasta invisível, de mesmo nome do arquivo
- Dentro da pasta deverá haver os arquivos necessários para realizar o versionamento (ainda não sei quais)

### SAVE
- Ao executar este comando, os arquivos da pasta de configuração do arquivo salvo devem ser alterados
- Deve haver um sistema para enumerar as linhas da versão antiga e da atual
- Outro deve verificar quais linhas estão em um e não no outro
- As linhas do antigo que não estão no novo foram as removidas
- As linhas do novo que não estão no antigo são as que foram inseridas
- O versionamento deve conter as linhas removidas e linhas inseridas, junto com o hash do salvamento
- O histórico também deve ser atualizado, com dado de data, hash e mensagem de salvamento
- O histórico também deve apontar para as informações que foram modificadas entre as versões

### HIST
- Este é simplesmente o histórico de salvamentos do arquivo
- Ele deve estar separado da estrutura que indica os conteúdos alterados
- Ele deve conter a data, o hash e a mensagem do salvamento
- Ao ser chamada, deve listar as informações de todos os os salvamentos feitos até agora
- Pode ser melhorado para no futuro retornar informações apenas de um salvamento especifico informado (hash ou número)

### DIFF
- Verifica se o arquivo esta diferente da ultima versao salva (e mostra o que esta diferente)
- Aplicar o sistema de verificação de remoções e inserções no arquivo atual e na ultima vesão
- Deve retornar se há alguma alteração não salva
- Além disso deve indicar quais linhas forma inseridas e quais foram removidas

### JUMP
- Restaurar uma versão anterior:
  - Deve ver cada linha que foi adicionada e remover
  - Ver cada linha removida e adicionar em suas respectivas posições
- Restaurar uma versão posterior:
  - Deve ver quais linhas foram removidas e remove
  - Ver quais linhas foram adicionadas e adicionar em suas respectivas posições
- Voltar ou avançar muitas estapas de uma vez:
  - É necessário executar o procedimento em um loop, considerando o número de vezes e a direção desejada
- Também é necessário realizar validações:
  - Hash: se o hash existe, se está na frente ou atrás, quantas etapas até lá...
  - Número: verificar se é maior que as etapas para trás ou para frente
