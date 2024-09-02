<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portal</title>
    </head>
        <body>
            <header>
            <nav>
                <a class="logo" href="/home">Tiger Codes</a>
                <div class="mobile-menu">
                <div class="line1"></div>
                <div class="line2"></div>
                <div class="line3"></div>
                </div>
                <ul class="nav-list">
                <li><a href="/home">Início</a></li>
                <li><a href="/login">Login</a></li>
                <li><a href="/administracao">Admin</a></li>
                <li><a href="/">Contato</a></li>
                </ul>
            </nav>
            </header>
            <main></main>
            <script src="/app/static/js/mobile-navbar.js"></script>
        <h1>Login</h1>
        <form action="/login" method="post">
            <label for="username">Nome:</label>
            <input id="username" name="username" type="text" required /><br>

            <label for="password">Senha:</label>
            <input id="password" name="password" type="password" required /><br>

            <input value="Login" type="submit" />
        </form>
    </body>
</html>