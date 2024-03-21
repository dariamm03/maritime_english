<?php

include "../../app/database/db.php";

$errMsg = '';
$question_code = '';
$text = '';
$correct = '';
$category_code = '';
$picture = '';
$audio = '';
$questions = selectAll('questions');
$categories = selectAll('categories_for_test');




// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['question-create'])) {
    if (!empty($_FILES['picture']['name'])) {

        $imgName = $_FILES['picture']['name'];
        $fileTmpName = $_FILES['picture']['tmp_name'];


        move_uploaded_file($fileTmpName, "../../assets/img/$imgName");

        $text = trim($_POST['text']);
        $correct = trim($_POST['correct']);
        $category_code = trim($_POST['category_code']);
        $audio = trim($_POST['audio']);
        if ($text === '' || $correct === '') {
            $errMsg = "Не все поля заполнены!";
        } else {
            $question = [
                'text' => $text,
                'correct' => $correct,
                'category_code' => $category_code,
                'picture' => $imgName,
                'audio' => $audio
            ];

            insert('questions', $question);
            $errMsg = "Вопрос добавлен";
            header('location: ' . 'http://localhost/dynamic-site/admin/questions/index.php');
        }
    } else {
        $text = '';
        $correct = '';
        $category_code = '';
    }
}

// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['question_code'])) {
    $question_code = $_GET['question_code'];
    $question = selectOne('questions', ['question_code' => $question_code]);
    $question_code = $question['question_code'];
    $text = $question['text'];
    $correct = $question['correct'];
    $category_code = $question['category_code'];
    $picture = $question['picture'];
    $audio = $question['audio'];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['question-edit'])){
    $imgName = $_FILES['picture']['name'];
    $fileTmpName = $_FILES['picture']['tmp_name'];


    move_uploaded_file($fileTmpName, "../../assets/img/$imgName");


    $text = trim($_POST['text']);
    $correct = trim($_POST['correct']);
    $category_code = trim($_POST['category_code']);


    if($text === '' || $correct === '' || $category_code === ''){
        $errMsg = "Не все поля заполнены!";
    }
    else{
        $question = [
            'text' => $text,
            'correct' => $correct,
            'category_code' => $category_code,
            'picture' => $imgName,
            'audio' => $audio
        ];
        $question_code = $_POST['question_code'];
        var_dump($question_code);
        $question_id = update('questions', $question_code,$question, 'question_code');
        header('location: ' . 'index.php');
    }
}
