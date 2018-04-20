#!/usr/bin/perl

# encode text to base64. 

use MIME::Base64 qw( encode_base64 );

$pass = shift || die "Need the password. $!\n";
$b64 = encode_base64($pass);

print "$b64\n";
