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
if (! $access{'etimespace'}) {
  &terror('ets_acl');
}

@config = parse_config();

my $ts=&find_section( 'sectype' => "time",
                      'secname' => $in{'timespace'},
                      'config'  => \@config );

&terror('ets_err_notfound', $in{'timespace'}) if (! defined($ts));


&header($text{'ets_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('ets_header', $in{'timespace'}), "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n";

for (my $i=0; $i < @{$ts->{'members'}}; $i++) {
  my $st=$ts->{'members'}->[$i];

  print "   <TR>\n";
  if ($st->{'stype'} eq 'weekly') {
    print   "     <TD><A HREF=\"edit_weekly.cgi?timespace=$in{'timespace'}&index=$i\">Weekly $st->{'days'}</TD>\n",
            "     <TD> &nbsp; &nbsp; </TD>\n",
            "     <TD>$st->{'time'}</TD>",
            "     <TD ALIGN=right><A HREF=\"del_statement.cgi?sectype=time&secname=$in{'timespace'}&index=$i&back=timespace\">",
            "$text{'ets_delst'}</A></TD>";
  } elsif ($st->{'stype'} eq 'date_range') {
    print   "     <TD><A HREF=\"edit_date.cgi?timespace=$in{'timespace'}&index=$i\">Date ",
            "$st->{'syear'}.$st->{'smonth'}.$st->{'sday'} - ",
            "$st->{'eyear'}.$st->{'emonth'}.$st->{'eday'}",
            "</A></TD>\n",
            "     <TD> &nbsp; &nbsp; </TD>\n",
            "     <TD>$st->{'time'}</TD>",
            "     <TD ALIGN=right><A HREF=\"del_statement.cgi?sectype=time&secname=$in{'timespace'}&index=$i&back=timespace\">",
            "$text{'ets_delst'}</A></TD>";
  } else {
    print   "     <TD><A HREF=\"edit_date.cgi?timespace=$in{'timespace'}&index=$i\">Date ",
            "$st->{'syear'}.$st->{'smonth'}.$st->{'sday'}</A></TD>\n",
            "     <TD> &nbsp; &nbsp; </TD>\n",
            "     <TD>$st->{'time'}</TD>",
            "     <TD ALIGN=right><A HREF=\"del_statement.cgi?sectype=time&secname=$in{'timespace'}&index=$i&back=timespace\">",
            "$text{'ets_delst'}</A></TD>";
  }
  print "</TR>\n";
}

print "<TR><TD>$text{'ets_nost'}</TD></TR>\n"
  if (! scalar(@{$ts->{'members'}}));

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "[ <A HREF=\"edit_weekly.cgi?timespace=$in{'timespace'}&new=1\">",
      "$text{'ets_addweekly'}</A> ] &nbsp; &nbsp; &nbsp;",
      "[ <A HREF=\"edit_date.cgi?timespace=$in{'timespace'}&new=1\">",
      "$text{'ets_adddate'}</A> ]",
      "<BR><BR><HR>",
      "<B>[</B> <A HREF=\"del_timespace.cgi?timespace=$in{'timespace'}\">",
      "$text{'ets_del'}</A> <B>]</B><HR>";

&footer("list_timespaces.cgi", $text{'ets_return'});

### END of edit_timespace.cgi ###.
