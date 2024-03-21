<?php
include "app/database/db.php";

$errMsg = '';


//Код для авторизации
if( $_SERVER['REQUEST_METHOD'] === 'POST'&& isset($_POST['button-log'])) {
    $login = trim($_POST['login']);
    $password = trim($_POST['password']);

    if ($login === '' || $password === ''){
        $errMsg = "Не все поля заполнены!";
    }
    else {
        $existen1 = selectOne('users', ['login' => $login]);
        var_dump($password);
        var_dump( $existen1['password']);
        if ($existen1 && password_verify($password, $existen1['password'])) {

            $_SESSION['admin'] = $existen1['admin'];

            $secret = callSecret($login);

            if ($_SESSION['admin']) {
                header('location: ' . BASE_URL . '2fa.php');
            } else {
                $_SESSION['user_code'] = $existen1['user_code'];
                $_SESSION['login'] = $existen1['login'];
                header('location: ' . BASE_URL);
                $color = "green";
                $errMsg = "<font color='$color'>" . "Вы успешно авторизовались" . "</font>";
            }
        } else{
            $errMsg = "Ошибка авторизации!";
        }
    }
}
else{
    $login = '';
    $password = '';
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['button-admin'])) {
    $login = 'dariam03';
    $existen1 = selectOne('users', ['login' => $login]);
    $secret = callSecret($login);
    $code = trim($_POST['code']);
    require_once 'GoogleAuthenticator.php';
    $ga = new PHPGangsta_GoogleAuthenticator();
    $checkResult = $ga->verifyCode($secret, $code, 2);
    if ($checkResult) {
        $_SESSION['user_code'] = $existen1['user_code'];
        $_SESSION['login'] = $existen1['login'];
        header('location: ' . BASE_URL . 'admin/questions/index.php');
        $color = "green";
        $errMsg = "<font color='$color'>" . "Вы успешно авторизовались" . "</font>";
    } else {
        $errMsg = 'Неверный код';
    }
}