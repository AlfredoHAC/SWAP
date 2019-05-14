<?php 

    $command = escapeshellcmd("./Modules/swap.py");
    $output  = shell_exec($command);

    if(file_exists("./Log/swapLog.html")){
        header("location:./Log/swapLog.html");
    }else{
        header("location:index.php?error=1");
    }
?>