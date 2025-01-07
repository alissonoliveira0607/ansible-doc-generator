# Gerador de Documentação de Roles Ansible

## Descrição

O Gerador de Documentação de Roles Ansible é uma ferramenta desenvolvida em Python que automatiza a criação de documentação para roles do Ansible. A ferramenta analisa a estrutura da role e gera um arquivo Markdown contendo informações abrangentes sobre a configuração, variáveis, tarefas e outros elementos importantes.

## Funcionalidades

- Geração automática de documentação em formato Markdown
- Validação da estrutura de diretórios da role
- Extração de metadados e informações da role
- Análise de variáveis (defaults e vars)
- Listagem de tarefas e handlers
- Documentação de dependências e plataformas suportadas
- Sistema de logging detalhado
- Suporte a múltiplos formatos YAML

## Requisitos

- Python 3.6 ou superior
- PyYAML
- Sistema operacional compatível (Linux, macOS, Windows)

## Instalação

1. Clone o repositório:
```bash
git clone https://seu-repositorio/ansible-doc-generator.git
cd ansible-doc-generator
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Comando Básico

```bash
python ansible_doc_generator.py /caminho/para/role
```

### Opções Disponíveis

```bash
python ansible_doc_generator.py --help
```

Saída:
```
usage: ansible_doc_generator.py [-h] [--output PATH] [--logs DIR] [--verbose]
                              [--version]
                              role_directory

Gerador de Documentação de Roles Ansible

Esta ferramenta gera automaticamente documentação abrangente para roles do Ansible.
Ela analisa a estrutura da role e cria um documento Markdown detalhado incluindo:
- Metadados e descrição da role
- Validação da estrutura de diretórios
- Variáveis de defaults e vars
- Informações sobre tarefas e handlers
- Suporte a plataformas e dependências
- Exemplo de uso em playbook

argumentos posicionais:
  role_directory         Caminho para o diretório da role do Ansible a ser analisada

argumentos opcionais:
  -h, --help            mostra esta mensagem de ajuda e sai
  --output PATH, -o PATH
                        Caminho para o arquivo de documentação gerado
                        (padrão: DOCUMENTATION.md no diretório da role)
  --logs DIR, -l DIR    Diretório para armazenar arquivos de log
                        (padrão: ./logs)
  --verbose, -v         Aumenta o nível de verbosidade (pode ser usado múltiplas vezes)
  --version             Mostra o número da versão do programa e sai
```

### Exemplos de Uso

1. Gerar documentação básica:
```bash
python ansible_doc_generator.py /path/to/my-role
```

2. Especificar arquivo de saída personalizado:
```bash
python ansible_doc_generator.py /path/to/my-role -o custom_docs.md
```

3. Definir diretório de logs personalizado:
```bash
python ansible_doc_generator.py /path/to/my-role -l /path/to/logs
```

4. Aumentar verbosidade:
```bash
python ansible_doc_generator.py /path/to/my-role -v
```

## Estrutura do Arquivo de Saída

O arquivo de documentação gerado inclui:

1. **Cabeçalho**
   - Nome da role
   - Descrição
   - Informações do autor
   - Licença
   - Versão mínima do Ansible

2. **Estrutura de Diretórios**
   - Lista de diretórios requeridos
   - Indicadores de presença/ausência (✓/✗)

3. **Informações da Role**
   - Plataformas suportadas
   - Dependências
   - Variáveis (defaults e vars)
   - Lista de tarefas
   - Handlers
   - Exemplo de playbook

## Logs e Depuração

O sistema de logging armazena informações detalhadas sobre:
- Início e fim do processo de geração
- Arquivos YAML não encontrados
- Erros de parsing YAML
- Diretórios ausentes na estrutura da role
- Erros durante a geração da documentação

Os logs são armazenados em:
```
./logs/docgen_YYYYMMDD_HHMMSS.log
```

[Todo o conteúdo anterior permanece igual até a seção de Estrutura do Código]

## Uso com Docker



1. Baixar a imagem do Docker Hub:
[Docker Hub](https://hub.docker.com/repository/docker/aoliveirasilva/ansible-doc-generator/general)
```bash
docker pull aoliveirasilva/ansible-doc-generator:v1.0
```

1. Gerar documentação para uma role:
```bash
docker run -v /caminho/para/role:/role -v $(pwd)/output:/output \
    aoliveirasilva/ansible-doc-generator:v1.0 \
    /role -o /output/DOCUMENTATION.md
```

1. Ver as opções disponíveis:
```bash
docker run seu-usuario/ansible-doc-generator:latest --help
```


## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Estrutura do Código

```
ansible-doc-generator/
├── docgen.py   
├── requirements.txt           
├── README.md             
```

## Licença

Este projeto está licenciado sob a GPLv3.

## Autor

[@Alisson Oliveira](https://github.com/alissonoliveira0607) - alissonoliveira0607@gmail.com


---

*Última atualização: [06/01/2025]*