<?php
include "../../app/controllers/categories_of_words.php";
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


    <div class="styles col-10">
        <div class="button row">
            <a href="<?php echo BASE_URL . "admin/categories_of_words/create.php";?>" class="col-2 btn btn-success">Создать</a>
        </div>
        <div class="section search col-md-3 col-9">
            <h3>Поиск</h3>
            <form action="/" method="post">
                <input type="text" name="search-term" class="text-input" placeholder="Введите искомое слово">
            </form>
        </div>
        <div class="row title-table">
            <h2>Управление записями</h2>
            <div class="category_code col-1">ID</div>
            <div class="category_name col-3">Название категории</div>
            <div class="red col-2">Управление</div>
        </div>
        <?php foreach ($categories as $key => $category): ?>
            <div class="row style">
                <div class="category_code col-1"><?=$category['category_code']; ?></div>
                <div class="category_name col-3"><?=$category['category_name'];  ?></div>
                <div class="red col-1"><a href="edit.php?category_code=<?=$category['category_code']; ?>">edit</a></div>
                <div class="del col-1"><a href="#">delete</a></div>
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
