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

#    Created  : 18.10.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'esource'}) {
  &terror('esuser_acl');
}

@config = parse_config();

my $sec=&find_section( 'sectype' => "source",
                      'secname' => $in{'sourcegroup'},
                      'config'  => \@config );

&terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sec));

my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


my $dbselect = &db_select('username', $st->{'user'}, $config{'usersql'}) if ($config{'userdb'});

&header($in{'new'} ? $text{'esuser_titleadd'} : $text{'esuser_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_sourceuser.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=sourcegroup VALUE=\"$in{'sourcegroup'}\">",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text($in{'new'} ? 'esuser_headeradd' : 'esuser_header',
            $st->{'user'}, $in{'sourcegroup'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD><B>$text{'esuser_name'}</B></TD>\n",
      "     <TD>",
      ($config{'userdb'})
        ? $dbselect
        : "<INPUT TYPE=text NAME=username VALUE=\"$st->{'user'}\">",
      "     </TD>\n",
      "    </TR>\n",

      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit NAME=\"save\" VALUE=\"$text{'save'}\">\n",
      $in{'new'} ? "" : "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"$text{'delete'}\">\n",
      "</FORM><HR>";


&footer("edit_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}", $text{'esuser_return'});

### END of edit_sourceuser.cgi ###.