<?php
header('Content-Type: application/json');
// create curl resource 
$curl = curl_init();
// set url 
curl_setopt ($curl, CURLOPT_URL, "http://localhost:8080/relationships/*?columns=agent:b,agent:a");

curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl, CURLOPT_HTTPGET, 1);
curl_setopt( $curl, CURLOPT_HTTPHEADER, array(
                                            'Accept: application/json',
                                            'Content-Type: application/json',
                                            'Connection: Keep-Alive'
                                            ));
$result = curl_exec ($curl);
curl_close ($curl);
//print_r($result);
$decode = json_decode($result, true);

$arr=array();
foreach ($decode['Row'] as $key => $va) {
    $col_r=array();
    foreach ($va['Cell'] as &$dt) {
        $col = [base64_decode($dt['column']) => base64_decode($dt['$']) ];
        array_push($col_r,$col);
    }
    $row = [ $key.'' => $col_r ];
    array_push($arr,$col_r);
}
//$data->
$json = json_encode($arr);
print_r($json);
?>
