<?php
include "../../app/controllers/study_words_in_text.php";
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
            <a href="<?php echo BASE_URL . "admin/study_words_in_text/create.php";?>" class="col-2 btn btn-success">Создать</a>
        </div>
        <div class="row title-table">
            <h2>Обновление записи</h2>
        </div>
        <div class="row add-style">
            <div class="mb-12 col-12 col-md-12 err">
                <p><?=$errMsg?></p>
            </div>
            <form action="edit.php" method="post" enctype="multipart/form-data">
                <input name="word_code" value="<?=$word_code;?>" type="hidden">
                <div class="col">
                    <input name="word" value="<?=$word;?>" type="text" class="form-control" placeholder="Слово" aria-label="Слово">
                </div>
                <div class="col">
                    <input name="translation" value="<?=$translation;?>" type="text" class="form-control" placeholder="Перевод" aria-label="Перевод">
                </div>
                <div class="col">
                    <option selected>Код категории</option>
                    <select name="category" class="form-select mb-2">
                        <?php foreach ($categories as $key => $category): ?>
                            <option value="<?=$category['category_code']; ?>"><?=$category['category_name'];?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="col">
                    <input name="example_in_text" value="<?=$example_in_text;?>" type="text" class="form-control" placeholder="Пример использования" aria-label="Пример использования">
                </div>
                <div class="col">
                    <button name="word-edit" class="btn btn-primary" type="submit">Обновить запись</button>
                </div>
            </form>
        </div>
    </div>
</div>
</div>


<!-- connection footer -->
<?php include("../../app/include/footer.php"); ?>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
</body>
</html>

