#
#    SquidGuard Configuration Webmin Module Library
#    Copyright (C) 2001 by Tim Niemueller <tim@niemueller.de>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    Created  : 26.03.2001

do '../web-lib.pl';
$|=1;
$_DEBUG=0;
$version="0.91.2";
$needperl="5.6.0";

&init_config();

eval "use $needperl";
&terror('global_needmodernperl', $version, $needperl, $@) if ($@);

if ($config{'userdb'}) {
  eval "use DBI";
  &terror('global_needdbi', $@) if ($@);
}

%access=&get_module_acl();
$cl=$text{'config_link'};
&ReadParse();


sub parse_config {

  # Do NOT use read_file_lines here, otherwise a
  # flush_file_lines in save_*.cgi would have
  # Very Bad Side-Effects (TM)

  open(CONF, $config{'conf'});
    my @c=<CONF>;
  close(CONF);
  my @config=();

  for (my $i=0; $i < @c; $i++) {
    $c[$i] = unify($c[$i]);

    next if (!$c[$i] || ($c[$i] =~ /^#/));
    print "$i: $c[$i]<BR>\n" if $_DEBUG;

    if ($c[$i] =~ /^dbhome\s+(\S+)/) {

      ###### DB Home

      my %section;
         $section{'sectype'}='dbhome';
         $section{'dbhome'}=$1;
         $section{'line'}=$i;

      print "<B>dbhome token found (i: $i, dbhome: $section{'dbhome'})</B><BR>\n" if $_DEBUG;

      push(@config, \%section);

    } elsif ($c[$i] =~ /^logdir\s+(\S+)/) {

      ###### Log Dir

      my %section;
         $section{'sectype'}='logdir';
         $section{'logdir'}=$1;
         $section{'line'}=$i;

      print "<B>logdir token found (i: $i, logdir: $section{'logdir'})</B><BR>\n" if $_DEBUG;

      push(@config, \%section);

    } elsif ($c[$i] =~ /^time\s+([-_.a-zA-Z0-9]+)\s+\{\s*$/) {

      ###### Timespace

      my %section;
         $section{'sectype'}='time';
         $section{'secname'}=$1;
         $section{'line'}=$i;

      my @members=();
      $c[$i] = unify($c[++$i]);
      while(($i < scalar(@c)) && ($c[$i] !~ /^\s*\}/)) {
        $c[$i] = unify($c[$i]);
        if ( ($c[$i] =~ /^weekly\s(.*)\s(\d\d:\d\d\s?-\s?\d\d:\d\d)/) ||
             ($c[$i] =~ /^weekly\s(.*)/) ) {
          print "<B>weekly token found</B><BR>\n" if $_DEBUG;
          my %st;
             $st{'stype'} = 'weekly';
             $st{'time'} = $2;
             $st{'line'} = $i;
             $st{'rawdays'} = $1;

          $st{'time'} =~ s/\s//g;
          my ($from, $to) = split(/-/, $st{'time'}, 2);
          ($st{'shour'}, $st{'smin'}) = split(/:/, $from);
          ($st{'ehour'}, $st{'emin'}) = split(/:/, $to);

          my @r=split(/\s?/, $st{'rawdays'});
          my $d='';
          foreach $s (@r) {
            print "S: $s<BR>\n" if $_DEBUG;
            if ($s eq '*') {
              $d='*';        # 128
              last;
            } elsif ($s =~ /m(ondays?)?/) {
              $d.='m';       # ++
            } elsif ($s =~ /t(uesdays?)?/) {
              $d.='t';       ## +=2;
            } elsif ($s =~ /w(ednesdays?)?/) {
              $d.='w';       ## +=4;
            } elsif ($s =~ /t?h(ursdays?)?/) {
              $d.='h';       ## +=8;
            } elsif ($s =~ /f(ridays?)?/) {
              $d.='f';       ## +=16;
            } elsif ($s =~ /s?a(turdays?)?/) {
              $d.='a';       ## +=32;
            } elsif ($s =~ /s(undays?)?/) {
              $d.='s';       ## +=64;
            }
          }
          $st{'days'}=$d;
          push(@members, \%st);
        } elsif ( ($c[$i] =~ /^date\s+(\d\d\d\d|\*)[.-](\d\d|\*)[.-](\d\d|\*)\s*(\d\d:\d\d\s?-\s?\d\d:\d\d)/) ) {
          #        ($c[$i] =~ /^date\s (\d\d|\*)[.-](\d\d|\*)[.-](\d\d|\*)/) ) {
          # 
          print "<B>date token found - 1</B><BR>\n" if $_DEBUG;
          my %st;
          $st{'stype'}='date';
          $st{'line'} = $i;
          $st{'syear'}=$1;
          $st{'syear'}+=2000 if (length($st{'syear'}==2));
          $st{'smonth'}=$2;
          $st{'sday'}=$3;
          $st{'time'}=$4;

          $st{'time'} =~ s/\s//g;
          my ($from, $to) = split(/-/, $st{'time'}, 2);
          ($st{'shour'}, $st{'smin'}) = split(/:/, $from);
          ($st{'ehour'}, $st{'emin'}) = split(/:/, $to);

          push(@members, \%st);

       } elsif (($c[$i] =~ /^date\s+(\d\d\d\d|\*)[.-](\d\d|\*)[.-](\d\d|\*)-(\d\d\d\d|\*)[.-](\d\d|\*)[.-](\d\d|\*)\s*(\d\d:\d\d\s?-\s?\d\d:\d\d)/) ||
                ($c[$i] =~ /^date\s+(\d\d\d\d|\*)[.-](\d\d|\*)[.-](\d\d|\*)-(\d\d\d\d|\*)[.-](\d\d|\*)[.-](\d\d|\*)/) ) {
          print "<B>date range token found (l: $i, i: ", scalar(@members), ")</B><BR>\n" if $_DEBUG;
          my %st;
          $st{'stype'}='date_range';
          $st{'line'} = $i;
          $st{'syear'}=$1;
          $st{'smonth'}=$2;
          $st{'sday'}=$3;
          $st{'eyear'}=$4;
          $st{'emonth'}=$5;
          $st{'eday'}=$6;
          $st{'time'}=$7;

          $st{'time'} =~ s/\s//g;
          my ($from, $to) = split(/-/, $st{'time'}, 2);
          ($st{'shour'}, $st{'smin'}) = split(/:/, $from);
          ($st{'ehour'}, $st{'emin'}) = split(/:/, $to);

          push(@members, \%st);

        }
        $i++;
      } # End of while

      # All empty lines after the section
      # are counted to the section
      while (($i+1 < scalar(@c)) && (unify($c[$i+1]) eq "")) {
        $i++;
        $c[$i] = unify($c[$i]);
      }
      $section{'end_line'} = $i;

      $section{'members'}=\@members;
      push(@config, \%section);
    } elsif ($c[$i] =~ /^(src|source)\s+([-_.a-zA-Z0-9]+)\s+((within|outside)\s+([-_.a-zA-Z0-9]+)\s+)?\{\s*$/) {

      ###### Source Group

      print "<B>source token found ($i)</B><BR>\n" if $_DEBUG;
      my %section;
         $section{'sectype'}='source';
         $section{'secname'}=$2;
         $section{'line'}=$i;
         $section{'tstype'} = $4;
         $section{'timespace'} = $5;
      my @members=();

      $c[$i] = unify($c[++$i]);
      while(($i < scalar(@c)) && ($c[$i] !~ /^\s*\}/)) {
        $c[$i] = unify($c[$i]);

        if ($c[$i] =~ /^ip\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/) {
          my %st;
             $st{'stype'}='subnet_long';
             $st{'line'}=$i;
             $st{'ip'}=$1;
             $st{'mask'}=$2;
          push(@members, \%st);
        } elsif ($c[$i] =~ /^ip\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/) {
          my %st;
             $st{'stype'}='iprange';
             $st{'line'}=$i;
             $st{'ip'}=$1;
             $st{'end'}=$2;
          push(@members, \%st);
        } elsif ($c[$i] =~ /^ip\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d\d?)/) {
          my %st;
             $st{'stype'}='subnet';
             $st{'line'}=$i;
             $st{'ip'}=$1;
             $st{'prefix'}=$2;
          push(@members, \%st);
        } elsif ($c[$i] =~ /^ip\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/) {
          my %st;
             $st{'stype'}='ip';
             $st{'line'}=$i;
             $st{'ip'}=$1;
          push(@members, \%st);


        } elsif ($c[$i] =~ /^domain\s+(\S+)/) {
          my %st;
             $st{'stype'}='domain';
             $st{'line'}=$i;
             $st{'domain'}=$1;
          push(@members, \%st);

        } elsif ($c[$i] =~ /^user\s+(\S+)/) {
          my %st;
             $st{'stype'}='user';
             $st{'line'}=$i;
             $st{'user'}=$1;
          push(@members, \%st);
        } elsif ($c[$i] =~ /^userlist\s+(\S+)/) {
          my %st;
             $st{'stype'}='userlist';
             $st{'line'}=$i;
             $st{'userlist'}=$1;
             $st{'userlist'} =~ /\/?([^\/]+)$/;
             $st{'name'}=$1;
          push(@members, \%st);
        }

        $i++;
      }

      # All empty lines after the section
      # are counted to the section
      while (($i+1 < scalar(@c)) && (unify($c[$i+1]) eq "")) {
        $i++;
        $c[$i] = unify($c[$i]);
      }
      $section{'end_line'} = $i;

      $section{'members'}=\@members;
      push(@config, \%section);
    } elsif ($c[$i] =~ /^(dest|destination)\s+([-_.a-zA-Z0-9]+)(\s+(within|outside)\s+([-_.a-zA-Z0-9]+))?\s+\{\s*$/) {

      ###### destination group

      print "<B>destination token found ($i)</B><BR>\n" if $_DEBUG;
      my %section;
         $section{'sectype'}='dest';
         $section{'secname'}=$2;
         $section{'line'}=$i;
         $section{'tstype'}=$4;
         $section{'timespace'}=$5;

      $c[$i] = unify($c[++$i]);
      while(($i < scalar(@c)) && ($c[$i] !~ /^\s*\}/)) {
        $c[$i] = unify($c[$i]);

        if ($c[$i] =~ /^domainlist\s+(\S+)/) {
          $section{'domainlist'}=$1;
          $section{'domainlist_line'} = $i;
        } elsif ($c[$i] =~ /^urllist\s+(\S+)/) {
          $section{'urllist'}=$1;
          $section{'urllist_line'} = $i;
        } elsif ($c[$i] =~ /^expressionlist\s+(\S+)/) {
          $section{'exprlist'}=$1;
          $section{'exprlist_line'} = $i;
        }
        $i++;
      }

      # All empty lines after the section
      # are counted to the section
      while (($i+1 < scalar(@c)) && (unify($c[$i+1]) eq "")) {
        $i++;
        $c[$i] = unify($c[$i]);
      }
      $section{'end_line'} = $i;

      push(@config, \%section);


    } elsif ($c[$i] =~ /^(rew|rewrite)\s+([-_.a-zA-Z0-9]+)\s+((within|outside)\s+([-_.a-zA-Z0-9]+)\s+)?\{\s*$/) {

      ###### Rewrite group

      print "<B>rewrite token found ($i)</B><BR>\n" if $_DEBUG;
      my %section;
         $section{'sectype'}='rewrite';
         $section{'secname'}=$2;
         $section{'line'}=$i;
         $section{'tstype'} = $4;
         $section{'timespace'} = $5;

      my @members=();
      $c[$i] = unify($c[++$i]);
      while(($i < scalar(@c)) && ($c[$i] !~ /^\s*\}/)) {
        $c[$i] = unify($c[$i]);

        if ($c[$i] =~ /^s\@(\S+)\@(\S+)\@(i?)(r?)(R?)/) {
          my %st=();
             $st{'stype'}='rew';
             $st{'line'}=$i;
             $st{'from'}=$1;
             $st{'to'}=$2;
             $st{'flag_i'} = $3 ? 1 : 0;
             $st{'flag_r'} = $4 ? 1 : 0;
             $st{'flag_R'} = $5 ? 1 : 0;
          push(@members, \%st);  
        }

        $i++;
      }
      $section{'members'}=\@members;

      # All empty lines after the section
      # are counted to the section
      while (($i+1 < scalar(@c)) && (unify($c[$i+1]) eq "")) {
        $i++;
        $c[$i] = unify($c[$i]);
      }
      $section{'end_line'} = $i;


      push(@config, \%section);


    } elsif ($c[$i] =~ /^acl\s+\{\s*$/) {

      ###### ACL

      print "<B>acl token found ($i)</B><BR>\n" if $_DEBUG;
      my %section;
         $section{'sectype'}='acl';
         $section{'secname'}=$2;
         $section{'line'}=$i;

      my @members=();
      $c[$i] = unify($c[++$i]);
      while(($i < scalar(@c)) && ($c[$i] !~ /^\s*\}/)) {
        if ($c[$i] =~ /\s*([-_.a-zA-Z0-9]+)\s+((within|outside)\s+([-_.a-zA-Z0-9]+)\s+)?\{/ ) {
            my %st;
               $st{'stype'} = 'acl_item';
               $st{'line'} = $i;
               $st{'source'} = $1;
               $st{'tstype'} = $3 ? $3 : 'none';
               $st{'timespace'} = $4;

            print "<B>acl_item found ($i)</B><BR><UL>\n",
                  "<LI>source: $st{'source'}</LI>\n",
                  "<LI>tstype: $st{'tstype'}</LI>\n",
                  "<LI>timespace: $st{'timespace'}</LI></UL>\n"
              if ($_DEBUG);

          $c[$i] = unify($c[++$i]);
          while (($i < scalar(@c)) && ($c[$i] !~ /^\s*\}/)) {
            if ($c[$i] =~ /^pass/) {
              my @pass=split(/\s+/, $c[$i]);
              shift @pass; # delete the first, it's always 'pass'...
              $st{'pass'} = \@pass;
              $st{'pass_line'} = $i;
              print "<I>Pass Statement: $c[$i]</I><BR>",
                    join('::', @pass), "-> ", scalar(@pass), "<BR>" if $_DEBUG;
            } elsif ($c[$i] =~ /^rewrite/) {
              my @rew = split(/\s+/, $c[$i]);
              shift @rew; # delete the first, it's always 'rewrite'...
              $st{'rewrite'} = \@rew;
              $st{'rewrite_line'} = $i;
              print "<I>Rewrite Statement: $c[$i]</I><BR>\n" if $_DEBUG;
            } elsif ($c[$i] =~ /^redirect\s+(.*)/) {
              my $tmp=$1;
              $tmp =~ /((301|302):)?(.*)/;
              $st{'redmode'} = $2;
              $st{'redurl'} = $3;
              $st{'redirect_line'} = $i;
              print "<I>Redirection Statement: $c[$i]</I><BR>\n" if $_DEBUG;
            } else {
              print "<I>Unknown Statement: $c[$i]</I><BR>\n" if $_DEBUG;
            }

            $c[$i] = unify($c[++$i]);
          } # end inner while

          # All empty lines after the section
          # are counted to the section
          while (($i+1 < scalar(@c)) && (unify($c[$i+1]) eq "")) {
            $i++;
            $c[$i] = unify($c[$i]);
          }
          $st{'end_line'} = $i;

          push(@members, \%st);
        } # end if start of acl_item
        $i++;
        $c[$i] = unify($c[$i]);
      } # end outer while
      $section{'members'} = \@members;

      # All empty lines after the section
      # are counted to the section
      while (($i+1 < scalar(@c)) && (unify($c[$i+1]) eq "")) {
        $i++;
        $c[$i] = unify($c[$i]);
      }
      $section{'end_line'} = $i;

      push(@config, \%section);
    }

  } # End main FOR loop

return wantarray ? @config : \@config;
}



sub find_section {
  my %args=@_;

  my $c;
  foreach $c (@{$args{'config'}}) {
    my $ok=1;
    for (keys %args) {
      next if ($_ eq 'config');
      if ($c->{$_} !~ /^$args{$_}$/) {
        $ok=0;
        last;
      }
    }

    return $c if ($ok);
  }

return undef;
}


sub get_binary_path {
  my $squidguard_command=undef;

  if ($config{'binary'}) {
    # It's explicitly defined
    $squidguard_command = $config{'binary'};
  } else {
    # Unknown, try to find it
    for ('/usr/bin', '/usr/sbin', '/usr/local/bin',
         '/usr/local/sbin', '/bin', '/sbin') {
      if (-x "$_/squidguard") {
        $squidguard_command="$_/squidguard";
        last;
      } elsif (-x "$_/squidGuard") {
        $squidguard_command="$_/squidGuard";
        last;
      }
    }
  }

return $squidguard_command;
}

# sgchown($file)
# Change user/group of file to squid
sub sgchown {
  if (-e $_[0]) {
    system("chown $config{'squiduid'}.$config{'squidgid'} $_[0]");
  }
}
  


# rebuild_db($file)
# Rebuild the dbfile $file with squidguard -C
sub rebuild_db {
  my $bin = &get_binary_path();
  &terror('lib_nobin') if (! -x $bin);
  if (-e $_[0]) {
    &backquote_logged("$bin -C '$_[0]' -c '$config{'conf'}'");
    &webmin_log('rebuild', 'dbfile', $_[0]);
    &sgchown($_[0]);
    &sgchown("$_[0].db");
  }
  &reload_squid();
}

# reload_squid
# Send Squid the HUP signal when db is rebuild
sub reload_squid {
  if ($config{'pidfile'} && (-e $config{'pidfile'})) {
  	open(PID, $config{'pidfile'}) or return undef;
 	  my $pid = <PID>;
  	 chomp $pid;
  	close(PID) or return undef;
    system("kill -HUP $pid");
  }
return $pid;
}




# db_get($select)
# Get $select from database
sub db_get {
  my $select = $_[0];

  my $db = DBI->connect($config{'dbisource'}, $config{'dbiuser'}, $config{'dbipass'});

  $db || &terror('global_dbi_con', $DBI::errstr);
  my $st=$db->prepare($select) || &terror('global_dbi_prep', $db->errstr());
  $st->execute || &terror('global_dbi_exec', $db->errstr());

  my $rv = $st->fetchall_arrayref();

  $db->disconnect();

return $rv;
}

# db_list(name, $select)
# Return the HTML for a SELECT box with users from database
sub db_select {
  my $name = $_[0];
  my $current = $_[1];
  my $select = $_[2];

  my $selres = &db_get($select);

  my $rv = "<SELECT NAME=\"$name\">";
  foreach my $v (@{$selres}) {
    $rv .= "<OPTION";
    $rv .= ($v->[0] eq $current) ? " SELECTED" : "";
    $rv .= ">$v->[0]\n";
  }
  $rv .= "</SELECT>\n";

return $rv;
}

sub unify {
  my $string=$_[0];
  chomp $string;
  $string =~ s/\t+/ /g;
  $string =~ s/\s+/ /g;
  $string =~ s/^\s+//;

return $string;
}


1;
### END of squidguard-lib.cgi ###.