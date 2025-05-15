
# 🕒 Sincronização de Relógios Distribuídos com Algoritmo de Berkeley

Este projeto simula a **sincronização de relógios em sistemas distribuídos** utilizando o **Algoritmo de Berkeley**. Um processo mestre coleta os horários de múltiplos slaves (clientes), calcula uma média ajustada e envia um novo horário sincronizado para todos.

## 👥 Autores
- Caio Henrique (caio14.poke@gmail.com)  
- Leonardo Lima (leo_2002_mario@hotmail.com)  
- Marcelly Silva (marcelly.silva@arapiraca.ufal.br)

---

## 📁 Estrutura do Projeto

```
/
├── master.py         # Servidor mestre que coordena a sincronização dos relógios
├── slave.py          # Cliente que representa um relógio com desvio aleatório
```

---

## ⚙️ Funcionalidades

### 🧠 Algoritmo de Berkeley
- O mestre envia uma requisição para os slaves solicitando seus horários locais.
- Cada slave responde com o seu tempo local (com desvio aleatório entre -10 e +10 segundos).
- O mestre calcula a média dos tempos e envia o novo horário sincronizado para todos os slaves.

### 📌 `master.py`
- Escuta conexões TCP na porta `8080`.
- Aceita múltiplas conexões de slaves (em sequência).
- Coleta os horários e imprime os tempos individuais de cada slave.
- Calcula o tempo médio entre todos (inclusive o mestre).
- Envia a hora sincronizada de volta aos slaves.

### 📌 `slave.py`
- Cada slave inicia com um relógio local desviado aleatoriamente.
- Conecta ao mestre e espera o comando `REQUEST_TIME`.
- Envia seu horário local.
- Recebe o novo horário sincronizado e o imprime no terminal.

---

## ▶️ Como Executar

### ✅ Pré-requisitos
- Python 3.x instalado
- Bibliotecas necessárias:
  ```bash
  pip install python-dateutil colorama
  ```

## 🚀 Passos

### 1. Inicie o mestre:
```bash
python master.py
```
O mestre aguardará conexões na porta `8080`.

### 2. Em outros terminais, inicie os slaves (um por vez):
```bash
python slave.py
```

### 3. Observe os logs coloridos mostrando:
- Desvio inicial de cada slave
- Comunicação com o mestre
- Novo horário sincronizado recebido

---

## 🧪 Exemplo de Execução

### Terminal do Mestre:
```
[MESTRE] Esperando conexões...
[MESTRE] Conexão de 127.0.0.1
[MESTRE] Horário do cliente: 14:25:10.000123
...
[MESTRE] Média ajustada: 14:25:07.456789
[MESTRE] Horário sincronizado enviado.
```

### Terminal do Slave:
```
[SLAVE abcd] Relógio local com desvio de +5 segundos: 14:25:15.000456
[SLAVE abcd] Conectado ao mestre.
[SLAVE abcd] Pedido de hora recebido do mestre.
[SLAVE abcd] Horário enviado: 14:25:15.000456
[SLAVE abcd] Novo horário recebido: 14:25:07.456789
```

---

## 📚 Conceitos Aplicados
- Comunicação via **sockets TCP**
- **Algoritmos de sincronização de tempo** (Berkeley)
- Tratamento de **desvios de relógio**
- Uso de **multiplos processos simulando nós distribuídos**
- Uso de cores no terminal com `colorama` para melhor visualização

---

## 🏁 Considerações Finais

Este projeto simula de forma prática os conceitos de **relógios lógicos e físicos**, além da **coordenação centralizada** em sistemas distribuídos, com foco no algoritmo de Berkeley
