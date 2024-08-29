<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login de Usuarios</title>
</head>
<body>

    <h1>Minha página com interação de modelos</h1>
        <div>
            <h2>Dados do Usuário:</h2>
            <p>Username: {{ current_user.username }} </p>
        </div>
    <form action="/logout" method="post">
        <button type="submit">Logout</button>
    </form>
</body>
</html>