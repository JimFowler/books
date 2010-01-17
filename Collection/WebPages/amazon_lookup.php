<?php

// Build your request string, e.g.
$request = 'Service=AWSECommerceService&'.'AWSAccessKeyId=[YOUR AWS ACCESS KEY]&'.'Timestamp='.gmdate("Y-m-d\TH:i:s\Z").'&Operation=ItemSearch&Title='.$title.'&SearchIndex=Books';

// Encode and sort the request string
$request = str_replace(',','%2C', $request);
$request = str_replace(':','%3A', $request);
$reqarr = explode('&',$request);
sort($reqarr);
$string_to_sign = implode("&", $reqarr);

// Append endpoint
$string_to_sign = "GET\necs.amazonaws.co.uk\n/onca/xml\n".$string_to_sign;

// Create signature hash
$signature = urlencode(base64_encode(hash_hmac("sha256", $string_to_sign, '[YOUR AWS PRIVATE KEY]', True)));

// Append signature to original request
$request .= '&Signature='.$signature;

// Append endpoint to original request
$request = 'http://ecs.amazonaws.co.uk/onca/xml?'.$request;

// Make request
Append signature to original request
$curl_handle = curl_init();
curl_setopt($curl_handle, CURLOPT_URL, $request);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
$book_data = curl_exec($curl_handle);
curl_close($curl_handle);
return $book_data;
?>
