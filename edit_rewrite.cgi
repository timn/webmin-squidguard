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

#    Created  : 15.05.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'erewrite'}) {
  &terror('edrew_acl');
}

@config = &parse_config();

my $sec=&find_section( 'config' => \@config,
                       'sectype' => 'rewrite',
                       'secname' => $in{'rewgroup'} );

my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


&header($in{'new'} ? $text{'edrew_titleadd'} : $text{'edrew_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_rewrite.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=rewgroup VALUE=\"$in{'rewgroup'}\">\n",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">\n",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text($in{'new'} ? 'edrew_headeradd' : 'edrew_header', $in{'rewgroup'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD><B>$text{'edrew_from'}</B></TD>\n",
      "     <TD><B>$text{'edrew_to'}</B></TD>\n",
      "    </TR>\n",

      "    <TR>\n",
      "     <TD><INPUT TYPE=text NAME=from VALUE=\"$st->{'from'}\" SIZE=30></TD>",
      "     <TD><INPUT TYPE=text NAME=to VALUE=\"$st->{'to'}\" SIZE=30></TD>",
      "    </TR>\n",

      "    <TR>\n",
      "     <TD COLSPAN=2>\n",
      "      <TABLE BORDER=0 WIDTH=100%>\n",
      "       <TR>\n",
      "        <TD WIDTH=33%><INPUT TYPE=checkbox NAME=flagi",
      $st->{'flag_i'} ? " CHECKED" : "",
      "> $text{'edrew_casein'}</TD>\n",
      "        <TD WIDTH=34%><INPUT TYPE=checkbox NAME=flagr",
      $st->{'flag_r'} ? " CHECKED" : "",
      "> $text{'edrew_movetemp'}</TD>\n",
      "        <TD WIDTH=33%><INPUT TYPE=checkbox NAME=flagt",
      $st->{'flag_R'} ? " CHECKED" : "",
      "> $text{'edrew_moveperm'}</TD>\n",
      "       </TR>\n",
      "      </TABLE>\n",
      "     </TD>\n",
      "    </TR>\n",

      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      "</FORM><HR>";


&footer("edit_rewgroup.cgi?rewgroup=$in{'rewgroup'}", $text{'edrew_return'});

### END of edit_sourcedomain.cgi ###.