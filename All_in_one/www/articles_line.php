<?php
$params = $_POST['hero_string'];
exec("\"C:/Anaconda3/python.exe\" chart3.py {$params}", $output, $return_val); 
sleep(8); 
echo $output[0];
//exec("\"C:/Anaconda3/python.exe\" chart3.py {$params} 2>&1", $output, $return_val);  
//var_dump($output);
?>