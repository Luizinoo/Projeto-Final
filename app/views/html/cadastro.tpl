<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro</title>
</head>
<body>

    <h1>Insira seus dadas abaixo</h1>
    
    <body>
    <h1>Login</h1>
    <form action="/cadastro" method="post">
        <label for="username">Username:</label>
        <input id="username" name="username" type="text" required /><br>

        <label for="nome">Nome:</label>
        <input id="nome" name="nome" type="text" required /><br>

        <label for="password">Senha:</label>
        <input id="password" name="password" type="password" required /><br>

        <input value="Login" type="submit" />
    </form>
</body>
</html>