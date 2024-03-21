<?php
include "../../app/controllers/answers.php";
?>


<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Maritime English</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
          integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>


<!-- connection header -->
<?php include("../../app/include/header-admin.php"); ?>


<div class="container">
    <?php include "../../app/include/sidebar.php"; ?>


    <div class="styles col-9">
        <div class="button row">
            <a href="<?php echo BASE_URL . "admin/answers/create.php";?>" class="col-2 btn btn-success">Создать</a>
        </div>
        <div class="row title-table">
            <h2>Управление записями</h2>
            <div class="id col-1">ID</div>
            <div class="question_code col-1">Код вопроса</div>
            <div class="a col-2">1 вариант</div>
            <div class="b col-2">2 вариант</div>
            <div class="c col-2">3 вариант</div>
            <div class="d col-2">4 вариант</div>
            <div class="red col-2">Управление</div>
        </div>
        <?php foreach ($answers as $key => $answer): ?>
            <div class="row style">
                <div class="id col-1"><?=$answer['id']; ?></div>
                <div class="question_code col-1"><?=$answer['question_code'];  ?></div>
                <div class="a col-2"><?=$answer['a'];  ?></div>
                <div class="b col-2"><?=$answer['b'];  ?></div>
                <div class="c col-2"><?=$answer['c'];  ?></div>
                <div class="d col-2"><?=$answer['d'];  ?></div>
                <div class="red col-1"><a href="edit.php?word_code=<?=$answer['id']; ?>">edit</a></div>
            </div>
        <?php endforeach; ?>
    </div>
</div>
</div>



<!-- connection footer -->
<?php include("../../app/include/footer.php"); ?>



<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
</body>
</html>


