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

#    Created  : 21.05.2001


require "./squidguard-lib.pl";

&error_setup($text{'cpc_error'});

if (defined($in{'dbhome'}) && defined($in{'logdir'})) {
  &redirect() if (! $config{'conf'});
  &terror('cpc_err_exists') if (-e $config{'conf'});

  use File::Basename; # This comes with the standard install of PERL
  my $dir = dirname($config{'conf'});

  &terror('cpc_err_dir') if (! -d $dir);
  &terror('cpc_err_dir2') if (! -d $in{'dbhome'});
  &terror('cpc_err_dir3') if (! -d $in{'logdir'});

  open(TEMPLATE, "template.conf");
   @templ=<TEMPLATE>;
  close(TEMPLATE);
  my $newconf = &read_file_lines($config{'conf'});
  my $date=&make_date(time);

  foreach $l (@templ) {
    chomp $l;
    $l =~ s/\@DBHOME\@/$in{'dbhome'}/g;
    $l =~ s/\@LOGDIR\@/$in{'logdir'}/g;
    $l =~ s/\@DATE\@/$date/g;
    next if (($l =~ s/^PASS://) && ($in{'type'} == 2));
    next if (($l =~ s/^BLOCK://) && ($in{'type'} == 1));
    push(@$newconf, $l);
  }

  &flush_file_lines();
  &redirect();

} else {
  &header($text{'cpc_title'}, undef, "intro", 1, 1, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>",
        "<H3>$text{'cpc_heading'}</H3>",
        "$text{'cpc_desc'}",
        "<BR><BR>",
        "<FORM ACTION=create_plainconf.cgi>",
        "<TABLE BORDER=0>",
        "<TR><TD>$text{'cpc_dbhome'}</TD>",
        "<TD><INPUT TYPE=text SIZE=50 NAME=dbhome> ",
        &file_chooser_button('dbhome', 1),
        "</TD></TR><TR><TD>$text{'cpc_logdir'}</TD>",
        "<TD><INPUT TYPE=text SIZE=50 NAME=logdir> ",
        &file_chooser_button('logdir', 1),
        "</TD></TR></TABLE>\n",
        "<BR><BR>$text{'cpc_desc2'}<BR><BR>",
        "<INPUT TYPE=radio NAME=type VALUE=1 CHECKED> $text{'cpc_passall'}",
        "<INPUT TYPE=radio NAME=type VALUE=2> $text{'cpc_nothing'}",
        "<BR><BR>",
        "<INPUT TYPE=submit VALUE=\"$text{'save'}\">",
        "</FORM>\n";
  &footer();
}

### END of create_plainconf.cgi ###.
