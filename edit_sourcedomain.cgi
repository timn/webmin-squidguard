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

#    Created  : 01.04.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'esource'}) {
  &terror('edomain_acl');
}

@config = parse_config();

my $sec=&find_section( 'sectype' => "source",
                      'secname' => $in{'sourcegroup'},
                      'config'  => \@config );

&terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sec));

my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


&header($in{'new'} ? $text{'edomain_titleadd'} : $text{'edomain_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_sourcedomain.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=sourcegroup VALUE=\"$in{'sourcegroup'}\">",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text($in{'new'} ? 'edomain_headeradd' : 'edomain_header',
            $st->{'domain'}, $in{'sourcegroup'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD><B>$text{'edomain_name'}</B></TD>\n",
      "     <TD><INPUT TYPE=text NAME=domain VALUE=\"",
      $in{'new'} ? "" : $st->{'domain'}, "\"> ",
      "     </TD>\n",
      "    </TR>\n",

      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit NAME=\"save\" VALUE=\"$text{'save'}\">\n",
      $in{'new'} ? "" : "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"$text{'delete'}\">\n",
      "</FORM><HR>";


&footer("edit_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}", $text{'edomain_return'});

### END of edit_sourcedomain.cgi ###.