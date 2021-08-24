<p align=center>
  <img
 src="https://user-images.githubusercontent.com/50140771/128561548-3a8d25e1-c2a3-46ef-94f7-4447fcdc0a97.png"/> 
</p>

# 🛠️ API SoLanches

O SoLanches é um sistema web, criado e desenvolvido durante a disciplina de Engenharia de Software do curso de Ciência da Computação na Universidade Federal de Campina Grande, que tem como objetivo exibir todos os comércios do ramo alimentício de cidades pequenas. Neste repositório está presente a API criada para o sistema. O Frontend do sistema e mais detalhes sobre sua documentação podem ser acessados [aqui](https://github.com/SoLanches/Frontend-SoLanches).

## 🗒️ Documentação da API

A documentação com instruções de uso para requisições à API pode ser encontrada [aqui](api.md).

## ⚙️ Tecnologias utilizadas

- [Python](https://python.org/) - Linguagem de programação
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Framework
- [MongoDB](https://docs.mongodb.com/) - DataBase
- [PyMongo](https://pymongo.readthedocs.io/en/stable/) - Distribuição Python para trabalhar com o MongoDB

## Como executar localmente

Para executar o sistema de forma automática, basta utilizar o seguinte comando

```
$ make run
```

Se optar por executar a API de forma manual, siga os seguintes passos

1. Crie o ambiente virtual
```
$ python3 -m venv venv
```

2. Ative o ambiente virtual
```
$ source venv/bin/activate
```

3. Instale as dependências 
```
$ pip install -r requirements.txt
```

4. Rode a aplicação
``` 
$ python3 -m solanches
```

## Como executar os testes

Para executar os testes, basta rodar o comando

```
$ make test
```

Se optar por executar manualmente, instale as dependências presentes no arquivo `tests-requirements.txt` e digite o seguinte comando:

```
$ python3 -m pytest
```

## 📌 Equipe do SoLanches

- [Ana Carolina](https://github.com/anacarolinacv)
- [Daniel Gomes](https://github.com/dnlgomesl)
- [Eduardo Afonso](https://github.com/EduardoNunes5)
- [Emilly Albuquerque](https://github.com/emys-alb)
- [Erick Sena](https://github.com/erickems)
- [Francicláudio Dantas](https://github.com/claudiodantas)
- [Gustavo Farias](https://github.com/GusttaFS)
- [Leandra Oliveira](https://github.com/LeandraOS)
- [Luciano Erick](https://github.com/LucianErick)
- [Marta Laís](https://github.com/martalais)
- [Mariana Nascimento](https://github.com/marianasn)
- [Rodrigo Eloy](https://github.com/RodrigoEC)

