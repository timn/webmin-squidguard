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

#    Created  : 08.05.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'esource'}) {
  &terror('essubnet_acl');
}

@config = parse_config();

my $sg=&find_section( 'sectype' => "source",
                      'secname' => $in{'sourcegroup'},
                      'config'  => \@config );

&terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sg));

my $st=$sg->{'members'}->[$in{'index'}];


&header($in{'new'} ? $text{'essubnet_titleadd'} : $text{'essubnet_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_sourcelongsubnet.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=sourcegroup VALUE=\"$in{'sourcegroup'}\">",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",&text('essubnet_header', "$st->{'ip'}/$st->{'mask'}", $in{'sourcegroup'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD><B>$text{'essubnet_network'}</B></TD>\n",
      "     <TD><INPUT TYPE=text NAME=net VALUE=\"",
      $in{'new'} ? "" : $st->{'ip'}, "\" SIZE=15 MAXSIZE=15> / ",
      "<INPUT TYPE=text NAME=mask SIZE=15 VALUE=\"",
      $in{'new'} ? "" : $st->{'mask'}, "\" MAXSIZE=15>",
      "     </TD>\n",
      "    </TR>\n",

      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      $in{'new'} ? "" : "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"$text{'delete'}\">\n",
      "</FORM><HR>";


&footer("edit_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}", $text{'essubnet_return'});

### END of edit_sourcesubnet.cgi ###.