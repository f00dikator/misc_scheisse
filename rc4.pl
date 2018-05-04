#!/usr/bin/perl


$MAX = 256;

    foreach $i (0..255) {
        $tmp = sprintf ("%c", $i);
        $atoi{$tmp} = $i;
    }

    $infile = shift;
    $tocrypt = shift;

    if ( ($infile eq '') || ($tocrypt eq '') ) {
        shit_for_brains();
    }

    open (IN, $infile);

    for ($i=0; $i<$MAX; $i++) {$S[$i] = $i;}

    $p=0;
    printf ("Enter a password\n");
    chop ($pword=<STDIN>);
    printf ("Enter the public portion of your password \(IV\)\n");
    chop ($pword2=<STDIN>);
    $pword = $pword . $pword2;
    @TEMP = split(//,$pword);
    $p = $#TEMP + 1;
    if ($tocrypt eq 'crypt') {
        open (OUT, ">$infile.crypt.$pword2");
        $finalfile = $infile . ".crypt" . ".$pword2";
    }
    if ($tocrypt eq 'decrypt') {open (OUT, ">$infile.decrypt"); $finalfile = $infile . ".decrypt";}

    for ($i=0; $i < $MAX; $i++) {$K[$i] = $TEMP[$i % $p];}

    $j=0;
    for ($i=0; $i<$MAX; $i++) {
        $j = ($j + $S[$i] + $K[$i]) % $MAX;
        $swap = $S[$i];
        $S[$i] = $S[$j];
        $S[$j] = $swap;
    }

    $i=$j=$q=0;
    while (<IN>) {
        if ($tocrypt eq 'crypt') {@mytmp = split(// ,$_);}
        if ($tocrypt eq 'decrypt') {@mytmp = split (/ /,$_);}
        foreach $val (@mytmp) {
            if ($tocrypt eq 'crypt') {
                $value = $atoi{$val};
            }
            if ($tocrypt eq 'decrypt') {$value = $val + 0;}
            $i = ($i + 1) % $MAX;
            $j = ($j + $S[$i]) % $MAX;
            $swap = $S[$i];
            $S[$i] = $S[$j];
            $S[$j] = $swap;
            $t = ($S[$i] + $S[$j]) % $MAX;
            $Q[$q] = $S[$t];
            $c = $value ^ $Q[$q];

            select (OUT); $|=1;
            if ($tocrypt eq 'crypt') {
                printf ("%d ", $c);
            }
            if ($tocrypt eq 'decrypt') {
                printf ("%c", $c);
            }
            select (STDOUT); $|=1;

            $q++;
        }

    }

    close (IN);
    close (OUT);
    print "Results are in $finalfile\n";
    exit(0);





sub shit_for_brains {
        printf ("Yo Brainchild!  Usage: ./rc4.pl <file name> <crypt/decrypt>\n");
        exit(0);
}



