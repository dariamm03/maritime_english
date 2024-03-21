<?php

include "../../app/database/db.php";

$errMsg = '';
$word_code = '';
$word = '';
$translation = '';
$category = '';
$example_in_text = '';
$words = selectAll('study_words_in_text');
$categories = selectAll('categories_of_words');


// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['word-create'])) {

    $word = trim($_POST['word']);
    $translation = trim($_POST['translation']);
    $category = trim($_POST['category']);
    $example_in_text = trim($_POST['example_in_text']);
    if ($word === '' || $translation === '' || $category === '' ) {
        $errMsg = "Не все поля заполнены!";
    } else {
        $word = [
            'word' => $word,
            'translation' => $translation,
            'category' => $category,
            'example_in_text' => $example_in_text
        ];

        insert('study_words_in_text', $word);
        $errMsg = "Слово добавлено";
        header('location: ' . 'http://localhost/maritime/admin/study_words_in_text/index.php');
    }
} else {
    $word = '';
    $translation = '';
    $example_in_text = '';

}

// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['word_code'])) {
    $word_code = $_GET['word_code'];
    $wordd = selectOne('study_words_in_text', ['word_code' => $word_code]);
    $word_code = $wordd['word_code'];
    $word = $wordd['word'];
    $translation = $wordd['translation'];
    $category = $wordd['category'];
    $example_in_text = $wordd['example_in_text'];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['word-edit'])){
    $word = trim($_POST['word']);
    $translation = trim($_POST['translation']);
    $category = trim($_POST['category_code']);
    $example_in_text = trim($_POST['example_in_text']);


    if($word === '' || $translation === '' || $category === '' ){
        $errMsg = "Не все поля заполнены!";
    }
    else{
        $wordd = [
            'word' => $word,
            'translation' => $translation,
            'category' => $category,
            'example_in_text' => $example_in_text
        ];
        $word_code = $_POST['word_code'];
        $word_id = update('study_words_in_text', $word_code,$wordd, word_code);
        header('location: ' . 'index.php');
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['word_del'])){


    $word_code = $_GET['word_del'];
    delete('study_words_in_text', $word_code, 'word_code');
    header('location: ' .  'http://localhost/maritime/admin/study_words_in_text/index.php');
}
