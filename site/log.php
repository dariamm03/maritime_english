<?php
include "path.php";
include "app/controllers/reg_clients.php";
?>

<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Maritime English</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link rel="stylesheet" href="assets/css/log.css">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
          integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>


<!-- connection header -->
<?php include("app/include/header.php"); ?>

<!-- FORM -->
<div class="container reg_form">
    <form class="row justify-content-center" method="post" action="log.php">
        <h3>Авторизация</h3>
        <div class="record-section col-md-6 col-16">
            <img src="assets/img/ship2.png" class="d-block" alt="..." width="500" height="600">
        </div>
        <div class="record-section2 col-md-6 col-14 d">
            <br/><br><br>
            <div class="mb-3 col-12 col-md-6 err">
                <p><?=$errMsg?></p>
            </div>
            <div class="mb-3 col-12 col-md-7">
                <h6>Введите логин</h6>
                <input name="login" value="<?=$login?>" type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
            </div>
            <br/>
            <div class="w-100"></div>
            <div class="mb-3 col-12 col-md-7">
                <h6>Введите пароль</h6>
                <input name="password" type="password" class="form-control" id="exampleInputPassword1">
            </div>
            <br/>
            <div class="w-100"></div>
            <div class="mb-3 col-12 ">
                <button type="submit" class="btn btn-success" name="button-log">Войти</button>
            </div>
        </div>
    </form>
</div>

<!-- connection footer -->
<?php include("app/include/footer.php"); ?>

