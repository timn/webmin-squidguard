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

#    Created  : 26.03.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'epaths'}) {
  &terror('epaths_acl');
}


&header($text{'epaths_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

@config = &parse_config();


my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $logsec=&find_section( 'config' => \@config,
                          'sectype' => 'logdir' );


print "<FORM ACTION=\"save_paths.cgi\" METHOD=POST>\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'epaths_header'}</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD><B>$text{'epaths_logdir'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=40 NAME=logdir VALUE=\"$logsec->{'logdir'}\"> ",
      &file_chooser_button('logdir'),
      "     </TD>\n",
      "    </TR>\n",

      "    <TR>\n",
      "     <TD><B>$text{'epaths_dbhome'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=40 NAME=dbhome VALUE=\"$dbsec->{'dbhome'}\"> ",
      &file_chooser_button('dbhome'),
      "     </TD>\n",
      "    </TR>\n",
      
      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      "</FORM><HR>";

&footer("", $text{'epaths_return'});

### END of edit_paths.cgi ###.
