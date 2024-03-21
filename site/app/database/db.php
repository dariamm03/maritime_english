<?php

session_start();
require('connect.php');

function tt($value){
    echo '<pre>';
    print_r($value);
    echo '</pre>';
    exit();
}


//Проверка выполнения запроса к БД
function dbCheckError($query){
    $errInfo = $query->errorInfo();
    if ($errInfo[0] !== PDO::ERR_NONE){
        echo $errInfo[2];
        exit();
    }
    return true;
}

//Запрос на получение данных одной таблицы
function selectAllWithParams($table, $params = []){
    global $pdo;
    $sql = "SELECT * FROM $table";
    if(!empty($params)){
        $i=0;
        foreach ($params as $key => $value){
            if(!is_numeric($value)){
                $value = "'".$value."'";
            }
            if($i === 0){
                $sql = $sql . " WHERE $key=$value";
            }
            else{
                $sql = $sql . " AND $key=$value";
            }
            $i++;
        }
    }
    $query = $pdo->prepare($sql);
    $query->execute();
    dbCheckError($query);

    return $query->fetchAll();
}

function selectAll($table, $params = []){
    global $pdo;
    $sql = "SELECT * FROM $table";
    $query = $pdo->prepare($sql);
    $query->execute();


    return $query->fetchAll();

}



function selectOne($table, $params = []){
    global $pdo;
    $sql = "SELECT * FROM $table";
    if(!empty($params)){
        $i = 0;
        foreach ($params as $key => $value){
            if (!is_numeric($value)){
                $value = "'".$value."'";
            }
            if ($i === 0){
                $sql = $sql . " WHERE $key=$value";
            }else{
                $sql = $sql . " AND $key=$value";
            }
            $i++;
        }
    }
    $query = $pdo->prepare($sql);
    $query->execute();
    dbCheckError($query);
    return $query->fetch();
}


function Results(){
    ?>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Результаты пользователей</title>
        <style type="text/css">
            table{
                width: 500px;
                margin: 0 auto;
                border: 1px solid black;
                padding: 10px;
                text-align: center;
                border-collapse: collapse;
                color: black;
            }
            th, td{
                border: 1px solid black;
                padding: 8px;
            }
            th{
                background: #6495ED;
                color: black;
            }
            h3{
                color: black;
                text-align: center;
            }
            h6{
                color: black;
                margin-left: 200px;
            }
        </style>
    </head>
    <body>
    <br/>
    <table>
        <tr>
            <th>Код пользователя</th>
            <th>Телеграм код</th>
            <th>Результат раздела "Пропуски"</th>
            <th>Результат раздел "Варианты ответов"</th>
            <th>Результат раздела "Произношение"</th>
            <th>Дата прохождения</th>
        </tr>

        <?php

        global $pdo;
        $sql = "SELECT tests.user_code, telegram_code, gaps, answer_choice, pronunciation, date from users, tests where tests.user_code = users.user_code";
        $query = $pdo->prepare($sql);
        $query->execute();
        $result_array = $query->fetchAll();
        $result = '';
        foreach ($result_array as $row) {
            $result .= '<tr>';

            $result .= "<td>" . $row["user_code"] . "</td>";
            $result .= "<td>" . $row["telegram_code"] . "</td>";
            $result .= "<td>" . $row["gaps"] . "</td>";
            $result .= "<td>" . $row["answer_choice"] . "</td>";
            $result .= "<td>" . $row["pronunciation"] . "</td>";
            $result .= "<td>" . $row["date"] . "</td>";
            $result .= "</tr>";
        }
        echo $result;

        ?>
    </table>
    </body>
    </html>
    <?php
}



//tt(selectAll('dancing_group'));

function update($table, $id, $params, $perem)
{
    global $pdo;
    $i = 0;
    $str = '';
    foreach ($params as $key => $value) {
        if ($i === 0) {
            $str = $str . $key . " = '" . $value . "'";
        } else {
            $str = $str . ", " . $key . " = '" . $value . "'";
        }
        $i++;
    }

    $sql = "UPDATE $table SET $str WHERE $perem = $id";
    $query = $pdo->prepare($sql);
    $query->execute($params);
    dbCheckError($query);
}

function delete($table, $id, $code){
    global $pdo;
    $sql = "DELETE FROM $table WHERE $code = $id";
    $query = $pdo->prepare($sql);
    $query->execute();
    dbCheckError($query);
}

// Запись в таблицу БД
function insert($table, $params){
    global  $pdo;
    $i = 0;
    $coll = '';
    $mask = '';
    foreach ($params as $key => $value){
        if ($i === 0){
            $coll = $coll . "$key";
            $mask = $mask . "'" ."$value" . "'";
        }
        else {
            $coll = $coll . ", $key";
            $mask = $mask . ", '" . "$value" . "'";
        }
        $i++;
    }
    $sql = "INSERT INTO $table ($coll) VALUES ($mask)";
    $query = $pdo->prepare($sql);
    $query->execute($params);
    dbCheckError($query);
    return $pdo->lastInsertId();
}

function callSecret($login){
    ob_start();
    global  $pdo;
    $sql = "SELECT users.secret FROM users WHERE users.login = '$login'";
    $query = $pdo->prepare($sql);
    $query->execute();
    return array_values($query->fetch())[0];
}


//Поиск в админ панели
function searchAdminQuestions($text, $table1){
    $text = trim(strip_tags(stripcslashes(htmlspecialchars($text))));
    global $pdo;
    $sql = "SELECT
        s.*
        FROM $table1 AS s
        WHERE s.text LIKE '%$text%' OR s.correct LIKE '%$text%'";
    $query = $pdo->prepare($sql);
    $query->execute();
    dbCheckError($query);
    return $query->fetchAll();
}