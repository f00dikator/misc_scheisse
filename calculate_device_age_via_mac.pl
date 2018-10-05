#!/usr/bin/perl

@masks = ();
@tmp = split(/\n/, `/usr/local/bin/python3 Navi.py get assets`);
foreach $i (@tmp)
{
    if ($i =~ /^(([0-9]+\.){3}[0-9]+)$/)
    {
        push (@IPS, $i);    
    }
}


open (IN, "mac-ages.csv") || die "Need mac-ages.csv file.\n";
while (<IN>)
{
    if ($_ =~ /^([0-9a-fA-F]{12})\/([0-9]+),([0-9]{4}-[0-9]+-[0-9]+),(.*)$/)
    {
        $mac = eval("0x" . "1" . $1);
        $mask = eval($2);
        $date = $3;
        $shifty = $mac >> (48 - $mask);
        if (defined($MASTER{$shifty}))
        {
            if ($MASTER{$shifty} !~ /$date/)
            {
                $MASTER{$shifty} = $MASTER{$shifty} . $date . " , ";
            }
        }
        else
        {
            $MASTER{$shifty} = $date;
        }
        push (@masks, $mask) unless (grep(/$mask/,@masks));
    }
}
@masks = sort { $a <=> $b } @masks;
close(IN);

foreach $ip (@IPS)
{
    @tmp = split(/\n/,`/usr/local/bin/python3 Navi.py $ip U`);
    @MACS = ();
    foreach $tmp_val (@tmp)
    {
        if ($tmp_val =~ /^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$/)
        {
            $tmp_mac_formatted = $tmp_val;
            $tmp_val =~ s/://g;
            $mac = eval("0x" . "1" . $tmp_val);
            $done = 0;
            for ($i=$#masks - 1; $done == 0 && defined($masks[$i]); $i--)
            {
                $tmp_mac = $mac >> (48 - $masks[$i]);
                if (defined($MASTER{$tmp_mac}))
                {
                    if ($MASTER{$tmp_mac} =~ /.*,.*/)
                    {
                        print "$ip -> $tmp_mac_formatted (mask $masks[$i]) -> possible device ages:\n";
                        @tmp_dates = split(/,/, $MASTER{$tmp_mac});
                        foreach $t_date (@tmp_dates)
                        {
                            print "\t$t_date\n";
                        }
                    }
                    else
                    {
                        print "$ip -> $tmp_mac_formatted (mask $masks[$i]) -> $MASTER{$tmp_mac}\n"; 
                    }
                    print "\n";
                    $done = 1;
                }
            }
            if ($done == 0)
            {
                print "$ip -> $tmp_mac_formatted (mask $masks[$i]) -> No device age could be gleaned\n";
            }
        }
    }
}


