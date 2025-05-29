# WaterStation - Sistema de Monitoramento de Dessalinização

Sistema web para monitoramento e gerenciamento de plantas de dessalinização de água, desenvolvido em Django com API REST para integração com sensores IoT.

## 📋 Funcionalidades

- **Gerenciamento de Usuários**: Admin, Operador e Visualizador
- **Monitoramento de Plantas**: Poços, dessalinizadores e reservatórios
- **Sensores IoT**: Temperatura, pH, salinidade, fluxo, pressão e nível
- **Dashboard em Tempo Real**: Alertas e estatísticas
- **API REST**: Para integração com dispositivos IoT

## 🚀 Como Executar

### 1. Preparar o Ambiente

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd WaterStation

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar o Banco de Dados

```bash
# Executar migrações
python manage.py migrate

# Criar dados iniciais (níveis de autorização, regiões, etc)
python manage.py setup_initial_data

# (Opcional) Criar dados de teste
python manage.py populate_test_data
```

### 3. Executar o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em: http://127.0.0.1:8000

## 👤 Usuários Padrão

Após executar `setup_initial_data`, será criado:

- **Admin**: admin@waterstation.com / admin123
- **Operador**: operador1@waterstation.com / op123456  
- **Visualizador**: visualizador1@waterstation.com / vis123456

## 📡 Simulador de Sensores

O sistema inclui um simulador Python para testar o envio de dados de sensores.

### Como Usar o Simulador

```bash
# Executar o simulador
python sample_sensor.py
```

### Opções do Simulador

1. **Simular sensor de temperatura** - Envia dados de temperatura por 2 minutos
2. **Simular sensor de pH** - Envia dados de pH por 2 minutos  
3. **Simular sensor de salinidade** - Envia dados de salinidade por 2 minutos
4. **Enviar leitura única** - Envia um valor específico para um sensor
5. **Teste múltiplos sensores** - Testa vários sensores simultaneamente

### Exemplo de Uso da API

```python
import requests

# Login na API
response = requests.post('http://127.0.0.1:8000/api/users/token/', {
    'email': 'admin@waterstation.com',
    'password': 'admin123'
})
token = response.json()['access']

# Enviar dados do sensor
headers = {'Authorization': f'Bearer {token}'}
data = {
    'sensor_id': 1,
    'value': 25.5
}
requests.post('http://127.0.0.1:8000/api/monitoring/sensor-data/', 
              json=data, headers=headers)
```

## 🔧 Estrutura do Sistema

### Níveis de Usuário

- **Admin**: Gerencia usuários e plantas
- **Operador**: Gerencia apenas plantas  
- **Visualizador**: Apenas visualização

### Componentes de uma Planta

- **Poço de Água**: Com sensores de temperatura, pH, salinidade
- **Dessalinizador**: Com sensores de fluxo e pressão
- **Reservatório**: Com sensores de nível e temperatura

## 📚 URLs Principais

- **Dashboard**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Plantas**: http://127.0.0.1:8000/monitoring/plants/
- **API Docs**: http://127.0.0.1:8000/api/docs/
- **Admin**: http://127.0.0.1:8000/admin/

## 🛠️ Tecnologias

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: Bootstrap 5 + JavaScript
- **Banco de Dados**: SQLite (desenvolvimento)
- **API**: JWT Authentication

## 📖 Comandos Úteis

```bash
# Resetar banco de dados
python manage.py flush

# Criar dados iniciais novamente
python manage.py setup_initial_data

# Ver logs do servidor
python manage.py runserver --verbosity=2
```

---

**Desenvolvido para monitoramento de plantas de dessalinização com foco em simplicidade e eficiência.**