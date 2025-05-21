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
- **Banco de Dados**: PostgreSQL (recomendado), SQLite (desenvolvimento)
- **Autenticação**: Django Authentication System
- **API**: Django REST Framework

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