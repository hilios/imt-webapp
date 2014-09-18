IMT - Backends HTTP
===================

Código do curso de Backend HTTP com python ministrado no Instituto Mauá de Tecnologia.

### Instalação

*Requer Python 2.7*

```sh
$ pip install paste
$ pip install webob
$ pip install webapp2
$ pip install jinja2
```

### Iniciando o Banco de dados

*Requer SQLite3*

```sh
$ python migrate.py
```

### Iniciando o servidor web

```sh
$ python servidor.py
serving on http://127.0.0.1:8080
```

Abra o seu navegador no endereço: [http://127.0.0.1:8080](serving on http://127.0.0.1:8080).

*URLs*

- Dispositivos: [/api/devices](http://127.0.0.1:8080/api/devices)
- Medidas: [/api/devices/N](http://127.0.0.1:8080/api/devices/1)

