<header class="container-fluid">
    <div class="container">
        <div class="row">
            <div class="col-2">
                <h1>
                    <a href="<?php echo BASE_URL ?>"><img src="../../assets/img/log.png" class="d-block" alt="..." width="128" height="73"></a>
                </h1>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </div>
            <nav class="menu col-10" id="main-menu">
                <button class="menu-toggle" id="toggle-menu">close</button>
                <div class="menu-dropdown">
                    <ul class="nav-menu">
                        <li>
                            <?php if (isset($_SESSION['user_code'])): ?>
                                <a href="#">
                                    <i class="fas fa-user"></i>
                                    <?php echo $_SESSION['login']; ?>
                                </a>
                                <ul>
                                    <?php if ($_SESSION['admin']): ?>
                                        <li><a href="https://localhost/maritime/admin/questions/index.php">Админ панель</a></li>
                                    <?php endif; ?>
                                    <li><a href="<?php echo BASE_URL . 'logout.php'; ?>">Выход</a></li>
                                </ul>
                            <?php else: ?>
                                <a href="<?php echo BASE_URL . 'log.php'; ?>">
                                    <i class="fas fa-user"></i>
                                    Кабинет
                                </a>
                            <?php endif; ?>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    </div>
</header>
