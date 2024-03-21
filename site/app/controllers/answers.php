<?php

include "../../app/database/db.php";

$errMsg = '';
$id = '';
$question_code = '';
$a = '';
$b = '';
$c = '';
$d = '';
$answers = selectAll('answers');
$questions = selectAll('questions');


// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['answer-create'])) {

    $question_code = trim($_POST['question_code']);
    $a = trim($_POST['a']);
    $b = trim($_POST['b']);
    $c = trim($_POST['c']);
    $d = trim($_POST['d']);
    if ($question_code === '' || $a === '' || $b === '' || $c === '' || $d === '') {
        $errMsg = "Не все поля заполнены!";
    } else {
        $answer = [
            'question_code' => $question_code,
            'a' => $a,
            'b' => $b,
            'c' => $c,
            'd' => $d
        ];

        insert('answers', $answer);
        $errMsg = "Ответ добавлен";
        header('location: ' . 'http://localhost/maritime/admin/answers/index.php');
    }
} else {
    $a = '';
    $b = '';
    $c = '';
    $d = '';

}

// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['answer_code'])) {
    $id = $_GET['id'];
    $answer = selectOne('answers', ['id' => $id]);
    $id = $answer['id'];
    $question_code = $answer['question_code'];
    $a = $answer['a'];
    $b = $answer['b'];
    $c = $answer['c'];
    $d = $answer['d'];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['answer-edit'])){

    $question_code = trim($_POST['question_code']);
    $a = trim($_POST['a']);
    $b = trim($_POST['b']);
    $c = trim($_POST['c']);
    $d = trim($_POST['d']);


    if($question_code === '' || $a === '' || $b === '' || $c === '' || $d === ''){
        $errMsg = "Не все поля заполнены!";
    }
    else{
        $answer = [
            'question_code' => $question_code,
            'a' => $a,
            'b' => $b,
            'c' => $c,
            'd' => $d
        ];
        $id = $_POST['id'];
        $answer_id = update('answers', $id,$answer, id);
        header('location: ' . 'index.php');
    }
}
