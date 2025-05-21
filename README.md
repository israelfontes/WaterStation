# Water Station Management System

## Overview

Water Station é um sistema de gerenciamento completo para monitoramento de estações de extração e distribuição de água, desenvolvido com Django e arquitetura MVC. O sistema permite o controle e monitoramento em tempo real de reservatórios, dessalinizadores e poços de água, utilizando sensores IoT para coleta de dados.

![Sistema Water Station](WaterStation_1.png)

## Funcionalidades

### Gerenciamento de Usuários e Permissões
- Sistema de autenticação e autorização
- Níveis de permissão personalizáveis
- Perfis de usuário com informações de contato e endereço

### Cenários e Plantas
- Criação e gerenciamento de múltiplos cenários de operação
- Configuração de plantas com localização geográfica
- Compartilhamento de cenários entre usuários

### Componentes Hídricos
- Gerenciamento de reservatórios com tipo e capacidade
- Monitoramento de dessalinizadores com controle de alcalinidade
- Rastreamento de poços de água com medição de fluxo

### Sensores e Leituras
- Suporte a múltiplos tipos de sensores (temperatura, pressão, pH, fluxo)
- Rastreamento em tempo real de leituras
- Histórico de medições com timestamp

### Dashboard e Análises
- Painel de controle com visão geral do sistema
- Gráficos e visualizações de dados
- Relatórios personalizáveis

### API RESTful
- API completa para integração com outros sistemas
- Documentação de endpoints
- Autenticação segura

## Tecnologias

- **Backend**: Django 5.0+
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Banco de Dados**: PostgreSQL (recomendado), SQLite (desenvolvimento), MariaDB (prévia)
- **Autenticação**: Django Authentication System
- **API**: Django REST Framework

## Cardinalidades

- **User → Address (1:1)** → Cada usuário tem um endereço, e cada endereço pertence a um usuário.
- **User → Authorization Level (N:1)** → Muitos usuários podem ter o mesmo nível de autorização.
- **User → User Region (N:M)** → Um usuário pode estar associado a várias regiões, e uma região pode ter vários usuários.
- **Reservoir → Sensor (1:N)** → Um reservatório pode ter vários sensores, mas um sensor pertence a apenas um reservatório.
- **Sensor → Read (1:N)** → Um sensor gera múltiplas leituras, mas cada leitura pertence a um sensor.
- **Dissalinizier → Sensor (1:N)** → Um sistema de dessalinização pode conter vários sensores, mas um sensor está associado a um sistema de dessalinização.
- **Water Well → Sensor (1:N)** → Um poço de água pode ser monitorado por vários sensores, mas cada sensor pertence a um único poço de água.
- **Plant → Address (1:1)** → Cada estação de tratamento tem um endereço.
- **Plant → Region (N:1)** → Muitas estações podem estar dentro da mesma região.
- **Plant → Reservoir (1:N)** → Uma estação pode conter vários reservatórios, mas um reservatório pertence a apenas uma estação.
- **Plant → Dissalinizier (1:N)** → Uma estação pode ter múltiplos sistemas de dessalinização.
- **Plant → Water Well (1:N)** → Uma estação pode gerenciar vários poços de água.


## Requisitos

- Python 3.10+
- Django 5.0+
- PostgreSQL ou SQLite
- Outras dependências listadas em `requirements.txt`

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request para branch develop

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
