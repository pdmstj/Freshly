<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Styled Table and Login</title>
    <link rel="stylesheet" href="css/style.css">
</head>

<body>

    <div class="container">

        <table border>
            <thead>
                <tr>
                    <td>ID</td>
                    <td>아이디</td>
                    <td>비밀번호</td>
                    <td>email</td>
                </tr>
            </thead>
            <hbody>
                <?php
                //1. mysql 접속
                $conn = mysqli_connect('localhost', 'root', '111111', 'freshlydb');

                //연결 실패 시, 오류 문자 출력하기
                if (!$conn) {
                    die("연결 실패!" . mysqli_connect_error());
                }

                //2. 쿼리 날리기(내림차순)
                $sql = "select * from users order by id desc";
                $result = mysqli_query($conn, $sql);
                //쿼리 날리기 실패 시, 오류 문자 출력하기
                if (!$result) {
                    die("쿼리 날리기 실패!" . mysqli_error($conn));
                }
                $cnt = mysqli_num_rows($result);
                echo "cnt: " . $cnt;

                //한 줄씩 가져오기
                for ($i = 0; $i < $cnt; $i++) {
                    $a = mysqli_fetch_row($result);
                    echo "<tr><td>$a[0]</td><td>$a[1]</td><td>$a[2]</td><td><a href='update_from.php?idx=$a[0]'>수정 </a>
                    <a href='delete.php?idx=$a[0]'>삭제</a></td></tr>";
                }
                /*mysqli_fetch_row($result);
                $a = mysqli_fetch_row($result);
                echo $a[0]."<br/>"; 번호
                echo $a[1]."<br/>"; 아이디
                echo $a[2]."<br/>"; 비밀번호
                */
                mysqli_close($conn);
                ?>
            </hbody>
        </table>
        <div class="center-login">
            <a href="login_form.html" class="login-btn">Login</a>
        </div>
    </div>

</body>

</html>