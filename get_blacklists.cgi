#!/usr/bin/perl
#
#    SquidGuard Configuration Webmin Module
#    Copyright (C) 2001 by Tim Niemueller <tim@niemueller.de>
#    http://www.niemueller.de/webmin/modules/squidguard/
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

#    Created  : 21.06.2001


require './squidguard-lib.pl';

@config = &parse_config();

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};

&ReadParse();

# from ftp or http url
&error_setup($text{'gbl_error'});

if ($in{'url'}) {

  if ($in{'url'} == 1) {
    $url = "http://ftp.ost.eltele.no/pub/www/proxy/squidGuard/contrib/blacklists.tar.gz";
  } elsif ($in{'url'} == 10) {
    $url = $in{'customurl'};
  }

  $file = &tempname();
  if ($url =~ /^http:\/\/([^\/]+)(\/.*)$/) {
    $host = $1; $page = $2; $port = 80;
    if ($host =~ /^(.*):(\d+)$/) { $host = $1; $port = $2; }
    &http_download($host, $port, $page, $file);
  } elsif ($in{'url'} =~ /^ftp:\/\/([^\/]+)\/(.*)$/) {
    $host = $1; $ffile = $2;
    &ftp_download($host, $ffile, $file);
  } else { &terror('gbl_invurl'); }

  # Uncompress the module file if needed
  open(MFILE, $file);
  read(MFILE, $two, 2);
  close(MFILE);

  if ($two eq "\037\235") {
    if (!&has_command("uncompress")) {
      unlink($file) if ($need_unlink);
      &terror('gbl_comp', "<tt>uncompress</tt>");
    }
  	local $temp = $file =~ /\/([^\/]+)\.Z/i ? "/tmp/$1" : &tempname();
  	local $out = `uncompress -c $file 2>&1 >$temp`;
  	unlink($file);
  	if ($?) {
		  unlink($temp);
  		&error('gbl_ecomp', $out);
  	}
  	$file = $temp;
  	$need_unlink = 1;
  } elsif ($two eq "\037\213") {
  	if (!&has_command("gunzip")) {
  		unlink($file) if ($need_unlink);
  		&terror('gbl_gzip', "<tt>gunzip</tt>");
  	}
  	local $temp = $file =~ /\/([^\/]+)\.gz/i ? "/tmp/$1" : &tempname();
  	local $out = `gunzip -c $file 2>&1 >$temp`;
  	unlink($file);
  	if ($?) {
  		unlink($temp);
  		&terror('gbl_egzip', $out);
  	}
  	$file = $temp;
  }

  $tar = `tar tf $file 2>&1`;
  if ($?) { &terror('gbl_tar', $tar); }

  my %blacklists=();
  my $blcount=0;
  foreach $f (split(/\n/, $tar)) {

    if ( ($f =~ /^\.\/blacklists\/([^\/]+)\/domains$/) ||
         ($f =~ /^blacklists\/([^\/]+)\/domains$/) ||
         ($f =~ /^\.\/blacklists\/([^\/]+)\/urls$/) ||
         ($f =~ /^blacklists\/([^\/]+)\/urls$/) ) {
      # we have a valid blacklist
      $blacklists{$1}++;
      $blcount++;
    }
  }

  if (! $blcount) {
    unlink($file);
    &terror('gbl_nolists');
  }

  # Extract blacklists
  $out = `cd $dbhome ; tar xf $file 2>&1 >/dev/null`;
  if ($?) {
    unlink($file);
    &terror('gbl_extract', $out);
  }
  unlink($file);

  system("chown -R $config{'squiduid'}.$config{'squidgid'} $dbhome/blacklists");


  &header($text{'gbl_title'}, undef, undef, undef, undef, undef,
          "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>";

  print "<H3>$text{'gbl_header'}</H3>\n",
        "$text{'gbl_lists'}<BR><BR>\n";

  for (keys %blacklists) {
    print "<LI>$_</LI>\n";
  }

  print "<BR><BR><A HREF=\"list_blacklists.cgi\">$text{'gbl_goto'}</A>";

  &footer();

} else {

  &header($text{'gbl_title'}, undef, undef, undef, undef, undef,
          "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>";

  print "<H3>$text{'gbl_header2'}</H3>\n",
        "$text{'gbl_location'}<BR><BR>\n",
        "<FORM ACTION=get_blacklists.cgi>\n",
        "<INPUT TYPE=radio NAME=url VALUE=1 CHECKED> SquidGuard.org<BR>\n",
        "<INPUT TYPE=radio NAME=url VALUE=10> <INPUT TYPE=text SIZE=50 NAME=customurl>\n",
        "<BR><BR><INPUT TYPE=submit VALUE=\"$text{'gbl_get'}\">\n",
        "</FORM>",
        "<BR><BR><HR>";

  &footer("list_blacklists.cgi", $text{'gbl_return'});

}

### END of get_blacklists.cgi ###.
