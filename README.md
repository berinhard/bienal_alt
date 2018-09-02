Projeto para o site da Outra 33 Bienal de São Paulo

## Setup da aplicação

Esse é um projeto Django clásscio, então o processo é o tradicional:

```bash
# Clonar o repositório:
git clone git@github.com:outra-bienal/bienal_alt.git

# Criar um virtualenv:
mkvirtualenv bienal_alt -p /usr/bin/python3.6.5

# Ativar o virtualenv
cd bienal_alt
cp env.example .env  # talvez você precisará editar o .env de acordo com suas configurações

# Instalar dependências
pip install -r requirements.txt
```

## Executando a aplicação

Para acessar a aplicação, será necessário criar um usuário administrativo com o comando:

```bash
python project/manage.py migrate
python project/manage.py createsuperuser
python project/manage.py runserver
```
