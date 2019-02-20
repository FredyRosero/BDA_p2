<?php
// create curl resource 
$curl = curl_init();
// set url 
curl_setopt ($curl, CURLOPT_URL, "http://localhost:8080/relationships/*/agent:a");

curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl, CURLOPT_HTTPGET, 1);
    $header[] = "Accept: application/json";
curl_setopt( $curl, CURLOPT_HTTPHEADER,     $header  );
$result = curl_exec ($curl);
curl_close ($curl);

print_r ($result);
?>
