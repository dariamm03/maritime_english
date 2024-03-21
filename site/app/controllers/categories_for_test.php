<?php

include "../../app/database/db.php";

$errMsg = '';
$category_id = '';
$category_name = '';
$categories = selectAll('categories_for_test');


if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['category-create'])){

    $category_name = trim($_POST['category_name']);
    if($category_name === ''){
        $errMsg = "Не все поля заполнены!";
    }
    else{
        $category = [
            'category_name' => $category_name
        ];

        insert('categories_for_test', $category);
        $errMsg = "Категория добавлена";
        header('location: ' . 'http://localhost/maritime/admin/categories_for_test/admin.php');
    }
}
else{
    $category_name = '';
}

// Редактирование категории
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['category_id'])) {
    $category_id = $_GET['category_id'];
    $category = selectOne('categories_for_test', ['category_id' => $category_id]);
    $category_id = $category['category_id'];
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
        $category_id = $_POST['category_id'];
        $category_code = update('categories_for_test', $category_id,$category, category_id);
        header('location: ' . 'admin.php');
    }
}