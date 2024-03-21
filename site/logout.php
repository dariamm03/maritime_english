<?php
session_start();
include "path.php";

unset($_SESSION['user_code']);
unset($_SESSION['login']);
unset($_SESSION['admin']);

header('location: ' . BASE_URL . 'log.php');