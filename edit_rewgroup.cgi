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
if (! $access{'erewrite'}) {
  &terror('erg_acl');
}

@config = &parse_config();

my $sec=&find_section( 'config' => \@config,
                       'sectype' => 'rewrite',
                       'secname' => $in{'rewgroup'} );

&terror('erg_err_notfound', $in{'rewgroup'}) if (! defined($sec));


&header($text{'erg_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";


print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('erg_header', $in{'rewgroup'}), "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n",

      "    <TR>\n",
      "     <TD WIDTH=40%><B>$text{'erg_from'}</B></TD>\n",
      "     <TD WIDTH=40%><B>$text{'erg_to'}</B></TD>\n",
      "     <TD WIDTH=10%><B>$text{'erg_flags'}</B></TD>\n",
      "     <TD WIDTH=10%></TD>\n",
      "    </TR>\n";

for (my $i=0; $i < scalar(@{$sec->{'members'}}); $i++) {

print "    <TR>\n",
      "     <TD WIDTH=40%><A HREF=\"edit_rewrite.cgi?rewgroup=$in{'rewgroup'}&index=$i\">$sec->{'members'}->[$i]->{'from'}</A></TD>\n",
      "     <TD WIDTH=40%>$sec->{'members'}->[$i]->{'to'}</TD>\n",
      "     <TD WIDTH=10%>",
      $sec->{'members'}->[$i]->{'flag_i'} ? ' i ' : '',
      $sec->{'members'}->[$i]->{'flag_r'} ? ' r ' : '',
      $sec->{'members'}->[$i]->{'flag_R'} ? ' R ' : '',
      "</TD>\n",
      "     <TD WIDTH=10% ALIGN=right><A HREF=\"del_statement.cgi?sectype=rewrite&secname=$in{'rewgroup'}&index=$i&back=rewgroup\">",
      "$text{'delete'}</A></TD>\n",
      "    </TR>\n";

}

if (! scalar(@{$sec->{'members'}})) {
  print "<TR><TD>$text{'erg_norule'}</TD></TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<B>[</B> <A HREF=\"edit_rewrite.cgi?rewgroup=$in{'rewgroup'}&new=1\">$text{'erg_addrule'}</A> <B>]</B><BR><BR>\n";

print "<BR><HR>\n",
      "<TABLE BORDER=0>\n",
      "<FORM ACTION=\"save_rewts.cgi\" METHOD=POST>",
      "<INPUT TYPE=hidden NAME=rewgroup VALUE=\"$in{'rewgroup'}\">",
      " <TR>\n",
      "  <TD><B>$text{'edg_timespace'}: </B></TD>\n",
      "  <TD><SELECT NAME=tstype>\n",
      "<OPTION VALUE=none",
      ($sec->{'tstype'} eq 'none') ? " SELECTED" : "",
      ">$text{'global_nots'}\n",
      "<OPTION VALUE=within",
      ($sec->{'tstype'} eq 'within') ? " SELECTED" : "",
      ">$text{'global_within'}\n",
      "<OPTION VALUE=outside",
      ($sec->{'tstype'} eq 'outside') ? " SELECTED" : "",
      ">$text{'global_outside'}\n",
      "   </SELECT>\n",
      "  </TD>\n",
      "  <TD><SELECT NAME=timespace>";

foreach $c (@config) {
  if ($c->{'sectype'} eq 'time') {
    print "<OPTION VALUE=\"$c->{'secname'}\"",
          ($sec->{'timespace'} eq $c->{'secname'}) ? " SELECTED" : "",
          ">$c->{'secname'}\n";
  }
}

print "   </SELECT>\n",
      "  </TD>\n",
      "  <TD><INPUT TYPE=submit VALUE=\"$text{'save'}\"></TD>\n",
      " </TR>\n",
      "</FORM>\n",
      "</TABLE>\n",
      "<HR>\n",
      "<B>[</B> <A HREF=\"del_rewgroup.cgi?rewgroup=$in{'rewgroup'}\">",
      "$text{'erg_del'}</A> <B>]</B><HR>";

&footer("list_rewgroups.cgi", $text{'erg_return'});

### END of edit_rewgroup.cgi ###.
