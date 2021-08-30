# Login com Flask

## JWT
A ideia com JWT seria gerar um token de autenticação que é válido por um período de tempo, esse token seria feito a partir do identificador único e estaria na Header Authorization. Com isso as rotas serão verificadas se contem o token e se ele é válido.


### Pseudo método de login

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.get_by_email(email)

    if not user or not user.verify_password():
        return jsonify({
            'error': 'suas credenciais estão erradas.'
        }), 403


    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow + datetime.timedelta(minutes=10)
    }

    token = "Bearer" + jwt.encode(payload, app.config['SECRET_KEY'])

    return jsonify('token': token)
```

### Pseudo código do jwt_required

Aqui é o método que vai verificar o token. Vai procurar por Authorization na header da requisição. irá verificar se token foi em formado e se ainda é válido, se for será retornado o usuário logado.

```python
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        
        if not token:
            return jsonify({'error': "você não tem permissão para acessar essa rota."}), 403

        if not 'Bearer' in token:
            return jsonify({"error": "token inválido."}), 401

        try:
            token_pure = token.replace("Bearer", "")
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'])
            current_user = User.get_by_id(decoded)
        except:
            return jsonify({"error": "token é inválido."}), 403

        return f(current_user=current_user, *args, **kwargs)

    return wrapper
```

### Pseudo código de rota protegita

O método de verificação do token ira verificar a header da requisição da rota protected.
Irá receber o usuário logado e assim, prosseguir com sua execução.

```python
@app.route('/auth/protected')
@jwt_required
def protected(current_user):
    result = current_user.get_nome()

    return jsonify(result)
```

### Observações

Temos que armazenas a senha no BD e a senha não pode ser amazenada crua, tem que ser armazenada com algum codificador.

Sempre que uma requisição que precisa do token for chamada, no cliente (Insomnia, Postman da vida) precisamos adicionar na Header o Authorization e o token gerado.
