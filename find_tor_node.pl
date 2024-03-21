#!/usr/bin/perl

$file = shift || die "Need file name";
open (IN, $file);
while (<IN>)
{
    if ($_ =~ /([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)/)
    {
        chop($_);
        $ip = $4 . "." . $3 . "." . $2 . "." . $1 . ".dnsel.torproject.org";
        $cmd = `nslookup $ip`;
        @rray = split(/\n/, $cmd);
        foreach $t (@rray)
        {
                if ($t =~ /Address: 127.0.0.2/)
                {
                        print "$_ is a tor exit node\n";
                }
        }
    }
}
