<?php

	
header('Content-Type:text/json;charset=utf-8');
 
$hero_string = $_POST['hero_string'];
$get_hero= explode(",",$hero_string);

set_time_limit(0);


Function get_total_ratio($r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5)
{
$ratios1 = get_time_ratio(1, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5);
$ratios2 = get_time_ratio(2, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5);
$ratios3 = get_time_ratio(3, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5);
$ratios4 = get_time_ratio(4, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5);
$ratios5 = get_time_ratio(5, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5);
$ratios6 = get_time_ratio(6, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5);

$ratios = array($ratios1, $ratios2, $ratios3, $ratios4, $ratios5, $ratios6);
return $ratios;
}


Function get_time_ratio($time, $r1, $r2, $r3, $r4, $r5, $h1, $h2, $h3, $h4, $h5)
{
$ratio11 = get_ratio($time, $r1, $h1);
$ratio12 = get_ratio($time, $r1, $h2);
$ratio13 = get_ratio($time, $r1, $h3);
$ratio14 = get_ratio($time, $r1, $h4);
$ratio15 = get_ratio($time, $r1, $h5);

$ratio21 = get_ratio($time, $r2, $h1);
$ratio22 = get_ratio($time, $r2, $h2);
$ratio23 = get_ratio($time, $r2, $h3);
$ratio24 = get_ratio($time, $r2, $h4);
$ratio25 = get_ratio($time, $r2, $h5);

$ratio31 = get_ratio($time, $r3, $h1);
$ratio32 = get_ratio($time, $r3, $h2);
$ratio33 = get_ratio($time, $r3, $h3);
$ratio34 = get_ratio($time, $r3, $h4);
$ratio35 = get_ratio($time, $r3, $h5);

$ratio41 = get_ratio($time, $r4, $h1);
$ratio42 = get_ratio($time, $r4, $h2);
$ratio43 = get_ratio($time, $r4, $h3);
$ratio44 = get_ratio($time, $r4, $h4);
$ratio45 = get_ratio($time, $r4, $h5);

$ratio51 = get_ratio($time, $r5, $h1);
$ratio52 = get_ratio($time, $r5, $h2);
$ratio53 = get_ratio($time, $r5, $h3);
$ratio54 = get_ratio($time, $r5, $h4);
$ratio55 = get_ratio($time, $r5, $h5);

$ratio1 = ($ratio11+$ratio12+$ratio13+$ratio14+$ratio15)/5;
$ratio2 = ($ratio21+$ratio22+$ratio23+$ratio24+$ratio25)/5;
$ratio3 = ($ratio31+$ratio32+$ratio33+$ratio34+$ratio35)/5;
$ratio4 = ($ratio41+$ratio42+$ratio43+$ratio44+$ratio45)/5;
$ratio5 = ($ratio51+$ratio52+$ratio53+$ratio54+$ratio55)/5;
return (($ratio1+$ratio2+$ratio3+$ratio4+$ratio5)/5);
}


Function get_ratio($the_time, $hero1, $hero2)
{
$total_win = 0;
$total_match = 0;
$the_time1 = 600*($the_time - 1);
$the_time2 = 600*($the_time);

$servername = "localhost";
$username = "root";
$password = "CUHKSZ";
$dbname = "win";

// Create connection
$conn = mysqli_connect($servername, $username, $password);
// Check connection
if (!$conn) {
    die("connection fail: " . mysql_error());
} 
// Connect to database

mysqli_select_db($conn, $dbname);

$sql0 = 
"create view temp_matches{$the_time} as
select M.match_id as match_id, ((PM.slot <128) = M.radiant_win) as is_win, PM.hero_id 
from matches as M, player_match as PM 
where (M.match_id = PM.match_id) and (M.duration > {$the_time1} ) and (M.duration < {$the_time2} )";

$sql1 = "
select count(*) as counts
from temp_matches{$the_time} as A, temp_matches{$the_time} as B 
where (A.match_id = B.match_id) and (A.hero_id = {$hero1}) and (B.hero_id = {$hero2}) and (A.is_win <> B.is_win) and (A.is_win = 1)";

$sql2 = "
select count(*) as counts
from temp_matches{$the_time} as A, temp_matches{$the_time} as B 
where (A.match_id = B.match_id) and (A.hero_id = {$hero1}) and (B.hero_id = {$hero2}) and (A.is_win <> B.is_win)";

$sql3 = "drop view temp_matches";

// Create view table;
//mysqli_query($conn, $sql0);

// Use sql1 and sql2 to get data;
$result1 = mysqli_query($conn, $sql1);
if (!$result1){
echo" result1 wrong for" . $the_time . $hero1 . $hero2;};
$row1 = mysqli_fetch_assoc($result1);  
$total_win = $row1["counts"];

$result2 = mysqli_query($conn, $sql2);
if (!$result2){
echo" result2 wrong for" . $the_time . $hero1 . $hero2;};
$row2 = mysqli_fetch_assoc($result2);  
$total_match = $row2["counts"];

// Delete view table, reuslts and connection;
mysqli_free_result($result1);
mysqli_free_result($result2);
//mysqli_query($conn, $sql3); 
mysqli_close($conn);

// Return result;
if ($total_match <> 0){ 
	return ($total_win/$total_match);}

return 0.5;
}



$asd = get_total_ratio($get_hero[0], $get_hero[1], $get_hero[2], $get_hero[3], $get_hero[4], $get_hero[5], $get_hero[6], $get_hero[7], $get_hero[8], $get_hero[9]);

$f_result = json_encode($asd);
echo $f_result;



?>