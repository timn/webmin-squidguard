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

#    Created  : 16.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'eblacklist'}) {
  &terror('lbl_acl');
}

@config = &parse_config();

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};

&header($text{'lbl_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";


print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'lbl_header'}</B></TD>\n",
      " </TR>\n",
      "</TABLE>\n";

if (-d "$dbhome/blacklists") {


  my @enabled=();
  foreach $c (@config) {
    if ( ($c->{'sectype'} eq 'dest') &&
         ($c->{'secname'} =~ /^bl_(.+)$/)) {
      push(@enabled, $1);
    }
  }

  my @images = ();
  my @texts  = ();
  my @links  = ();

  opendir(DIR, "$dbhome/blacklists");
  while($entry = readdir(DIR)) {
    next if ($entry =~ /^\.\.?$/);
    if (-d "$dbhome/blacklists/$entry") {
      my $text =  $entry;
         $text .= (&indexof($entry, @enabled) >= 0) ? " (*)" : "";
      push(@images, "images/icon.blacklist.gif");
      push(@texts, $text);
      push(@links, "edit_blacklist.cgi?blacklist=$entry");
    }
  }
  closedir(DIR);


  if (@images) {
    &icons_table(\@links, \@texts, \@images, 4);
  } else {
    print "<BR><BR><B>$text{'lbl_nobl'}</B><BR><BR>";
  }

} else {
  print "<BR><BR><B>$text{'lbl_nobl'}</B><BR><BR>";
}

print "<HR>\n",
      "<B>[</B> <A HREF=get_blacklists.cgi>$text{'lbl_getbl'}</A> <B>]</B>\n",
      "<HR>\n";

&footer("", $text{'lsg_return'});

### END of list_blacklists.cgi ###.
