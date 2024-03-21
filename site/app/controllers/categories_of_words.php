<?php

include "../../app/database/db.php";

$errMsg = '';
$category_code = '';
$category_name = '';
$categories = selectAll('categories_of_words');


if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['category-create'])){

    $category_name = trim($_POST['category_name']);
    if($category_name === ''){
        $errMsg = "Не все поля заполнены!";
    }
    else{
        $category = [
            'category_name' => $category_name
        ];

        insert('categories_of_words', $category);
        $errMsg = "Категория добавлена";
        header('location: ' . 'http://localhost/maritime/admin/categories_of_words/admin.php');
    }
}
else{
    $category_name = '';
}

// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['category_code'])) {
    $category_code = $_GET['category_code'];
    $category = selectOne('categories_of_words', ['category_code' => $category_code]);
    $category_code = $category['category_code'];
    $category_name = $category['category_name'];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['category-edit'])){
    $category_name = trim($_POST['category_name']);

    if($category_name === ''){
        $errMsg = "Не все поля заполнены!";
    }
    else{
        $category = [
            'category_name' => $category_name
        ];
        $category_code = $_POST['category_code'];
        $category_id = update('categories_of_words', $category_code,$category, category_code);
        header('location: ' . 'admin.php');
    }
}