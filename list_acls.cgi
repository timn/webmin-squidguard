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

#    Created  : 02.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'eacl'}) {
  &terror('lacls_acl');
}

@config=&parse_config();
my $sec=&find_section( 'config' => \@config,
                       'sectype' => 'acl');

&header($text{'lacls_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'lacls_header'}</B></TD>\n",
      " </TR>\n",
      "</TABLE>\n";


my @images = ();
my @texts  = ();
my @links  = ();

for (my $i=0; $i < @{$sec->{'members'}}; $i++) {
  # iterate through all acl_items

  push(@images, "images/icon.acls.gif");
  my $tmp =  $sec->{'members'}->[$i]->{'source'};
     $tmp .= ($sec->{'members'}->[$i]->{'tstype'} ne 'none')
             ? ' ' . $sec->{'members'}->[$i]->{'tstype'} .
               ' ' . $sec->{'members'}->[$i]->{'timespace'}
             : '';
  push(@texts, $tmp);
  push(@links, "edit_aclitem.cgi?aclindex=$i");

}
&icons_table(\@links, \@texts, \@images, 4);

print "<HR>\n",
      "<FORM ACTION=add_aclitem.cgi METHOD=POST>\n",
      "$text{'lacls_source'} <SELECT NAME=source>\n";

foreach $c (@config) {
  if ($c->{'sectype'} eq 'source') {
    print "<OPTION>$c->{'secname'}\n";
  }
}

print " </SELECT>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'lacls_add'}\">\n",
      "</FORM>\n",
      "<HR>\n";

&footer("", $text{'lacls_return'});

### END of list_acls.cgi ###.
