#!/usr/bin/perl

# encode text to base64. 

use MIME::Base64;# qw( encode_base64 );

print "Enter passwd :";
$pass = <STDIN>;
chop($pass);

$b64 = encode_base64($pass);

print "$b64\n";
