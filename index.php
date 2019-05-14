<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700">
    <title>SWAP - Simple Web Application Pentest</title>
</head>
<body>
    <header>
        <img src="scorpion_logo-01.png" alt="SWAP">
        <h1>Simple Web Application Pentest</h1>
    </header>

    <main>
        <section id="inputForm">
            <fieldset>
                <label>Digite o domínio a ser testado:</label>
                <form name="domainTest" action="callSwap.php" method="GET">
                    <input type="text" id="txtDomain" name="txtDomain" placeholder="http://">
                    <input type="submit" id="btnSubmit" value="Testar"> 
                </form>
            </fieldset>
        </section>
    </main>
</body>
</html>
