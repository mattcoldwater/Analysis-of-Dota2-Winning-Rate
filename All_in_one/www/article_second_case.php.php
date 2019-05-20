<?php

header('Content-Type:text/json;charset=utf-8');
 
$hero_string = $_POST['hero_string'];
$get_hero= explode(",",$hero_string);	


Function get_the_fail_ratio ($hero){


$sql0 = "
select *
from total_heroes_ratio
where h0 = {$hero}
";


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


// Use sql0 to get data;
$result = mysqli_query($conn, $sql0);
if (!$result){
echo" result wrong";};
$row = mysqli_fetch_assoc($result);  

// Get the top three highest win-ratio heroes
$i = 0;
$hero_ratios = array();
for ($i = 0; $i<130; $i++){
	$hero_column = "h" . $i;
	$hero_ratios[$i] = $row[$hero_column];
};
mysqli_free_result($result);
mysqli_close($conn);


$final_heroes = get_top_three ($hero_ratios);
print_r($final_heroes);
return $final_heroes;
}

Function get_top_three($hero_ratios){

$i = 1;
$final_heroes = array();
$final_heroes[0] = 0;
$final_heroes[1] = 0;
$final_heroes[2] = 0;
$final_heroes_ratio = array();
$final_heroes_ratio[0] = 0;
$final_heroes_ratio[1] = 0;
$final_heroes_ratio[2] = 0;

for ($i = 1; $i<130; $i++){
	if ($hero_ratios[$i] == 0.01){continue;};
	if ($hero_ratios[$i] > $final_heroes_ratio[0]){
		$final_heroes_ratio = array($hero_ratios[$i], $final_heroes_ratio[0], $final_heroes_ratio[1]);
		$final_heroes = array($i, $final_heroes[0], $final_heroes[1]);
	}
	elseif ($hero_ratios[$i] > $final_heroes_ratio[1]){
		$final_heroes_ratio = array($final_heroes_ratio[0], $hero_ratios[$i], $final_heroes_ratio[1]);
		$final_heroes = array($final_heroes[0], $i, $final_heroes[1]);
	}
	elseif ($hero_ratios[$i] > $final_heroes_ratio[2]){
		$final_heroes_ratio[2] = $hero_ratios[$i];
		$final_heroes[2] = $i;
	}
}

return $final_heroes;
}




Function test_team($temp, $team, $the_num){

$the_num = $the_num - 1;
while ($the_num > -1){
	if ($temp == $team[$the_num])
		return 1;
	$the_num = $the_num - 1;
}
return 0;
}




Function get_whole_team($h1, $h2, $h3, $h4, $h5){

$the_team = array();
$temp_one = array();
//For hero 1;
$temp_one = get_the_fail_ratio ($h1);
$the_team[0] = $temp_one[0];

//For hero 2;
$temp_one = get_the_fail_ratio ($h2);
if($temp_one[0] == $the_team[0]){
	$the_team[1] = $temp_one[1];	
}
else {
	$the_team[1] = $temp_one[0];
} 

// For hero 3;
$temp_one = get_the_fail_ratio ($h3);
if(!test_team($temp_one[0], $the_team, 2)){
	$the_team[2] = $temp_one[0];}
elseif(!test_team($temp_one[1], $the_team, 2)){
	$the_team[2] = $temp_one[1];}
else {
	$the_team[2] = $temp_one[2];
}

//For hero 4;
$temp_one = get_the_fail_ratio ($h4);
if(!test_team($temp_one[0], $the_team, 3)){
	$the_team[3] = $temp_one[0];
}
elseif(!test_team($temp_one[1], $the_team, 3)){
	$the_team[3] = $temp_one[1];
}
else {
	$the_team[3] = $temp_one[2];
}

//For hero 5;
$temp_one = get_the_fail_ratio ($h5);
if(!test_team($temp_one[0], $the_team, 4)){
	$the_team[4] = $temp_one[0];
}
elseif(!test_team($temp_one[1], $the_team, 3)){
	$the_team[4] = $temp_one[1];
}
else {
	$the_team[4] = $temp_one[2];
}

return $the_team;

}

$asd = get_whole_team($get_hero[1],$get_hero[2],$get_hero[3],$get_hero[4],$get_hero[5]);
$f_result = json_encode($asd);
echo $f_result;



?>