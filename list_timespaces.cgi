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

#    Created  : 30.03.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'etimespace'}) {
  &terror('lts_acl');
}

@config = &parse_config();

&header($text{'lts_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'lts_header'}</B></TD>\n",
      " </TR>\n",
      "</TABLE>\n";

my @images = ();
my @texts  = ();
my @links  = ();

foreach $c (@config) {
  if ($c->{'sectype'} =~ /^(time|date|date_range)$/) {

    push(@images, "images/icon.timespace.gif");
    push(@texts, $c->{'secname'});
    push(@links, "edit_timespace.cgi?timespace=$c->{'secname'}");

  }
}

&icons_table(\@links, \@texts, \@images, 4);


print "<HR>\n",
      "<FORM ACTION=add_timespace.cgi METHOD=POST>\n",
      "$text{'lts_newname'} <INPUT TYPE=text NAME=name>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'lts_add'}\">\n",
      "</FORM>\n",
      "<HR>\n";

&footer("", $text{'lts_return'});

### END of edit_paths.cgi ###.
