<?php
include "../../app/controllers/questions.php";
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


<<!-- connection header -->
<?php include("../../app/include/header-admin.php"); ?>


<div class="container">
    <?php include "../../app/include/sidebar.php"; ?>


    <div class="styles col-9">
        <div class="button row">
            <a href="<?php echo BASE_URL . "admin/questions/create.php";?>" class="col-2 btn btn-success">Создать</a>
            <span class="col-1"></span>
            <a href="<?php echo BASE_URL . "admin/questions/admin.php";?>" class="col-3 btn btn-warning">Редактировать</a>
        </div>
        <div class="row title-table">
            <h2>Добавление записи</h2>
        </div>
        <div class="row add-style">
            <div class="mb-12 col-12 col-md-12 err">
                <p><?=$errMsg?></p>
            </div>
            <form action="create.php" method="post" enctype="multipart/form-data">
                <div class="col">
                    <input name="text" value="<?=$text;?>" type="text" class="form-control" placeholder="Текст вопрроса" aria-label="Текст вопрроса">
                </div>
                <div class="col">
                    <input name="correct" value="<?=$correct;?>" type="text" class="form-control" placeholder="Правиьный ответ" aria-label="Правиьный ответ">
                </div>
                <div class="col">
                    <label for="description" class="form-label">Код категории вопроса</label>
                    <option selected>Категория</option>
                    <select name="type_code" class="form-select mb-2">
                        <?php foreach ($categories as $key => $category): ?>
                            <option value="<?=$category['category_code']; ?>"><?=$category['category_name'];?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="input-group col mb-4 mt-4">
                    <input name="picture" type="file" class="form-control" id="inputGroupFile02">
                    <label class="input-group-text" for="inputGroupFile02">Upload</label>
                </div>
                <div class="input-group col mb-4 mt-4">
                    <input name="audio" type="file" class="form-control" id="inputGroupFile02">
                    <label class="input-group-text" for="inputGroupFile02">Upload</label>
                </div>
                <div class="col">
                    <button name="question-create" class="btn btn-primary" type="submit">Сохранить запись</button>
                </div>
            </form>
        </div>
    </div>
</div>
</div>
</div>
</div>

<!-- connection footer -->
<?php include("../../app/include/footer.php"); ?>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
</body>
</html>



