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

#    Created  : 17.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'eblacklist'}) {
  &terror('ebu_acl');
}

@config = &parse_config();

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};


my @domains=();
open(FILE, "$dbhome/blacklists/$in{'blacklist'}/urls");
 @urls=<FILE>;
close(FILE);

&header($in{'new'} ? $text{'ebd_titleadd'} : $text{'ebu_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_blurl.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=blacklist VALUE=\"$in{'blacklist'}\">\n",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">\n",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text($in{'new'} ? 'ebu_headeradd' : 'ebu_header', $in{'blacklist'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n";

chomp $urls[$in{'index'}];
print "    <TR>\n",
      "     <TD><B>$text{'ebu_name'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=50 NAME=url VALUE=\"",
      $in{'new'} ? "" : $urls[$in{'index'}],
      "\"> ",
      "     </TD>\n",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      ($in{'new'}) ? "" : "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"$text{'delete'}\">\n",
      "</FORM><HR>";


&footer("edit_blacklist.cgi?blacklist=$in{'blacklist'}", $text{'ebu_return'});

### END of edit_blurl.cgi ###.