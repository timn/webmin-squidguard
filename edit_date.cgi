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
  &terror('edate_acl');
}

@config = &parse_config();

my $ts=&find_section( 'sectype' => "time",
                      'secname' => $in{'timespace'},
                      'config'  => \@config );

my $st;
$st=$ts->{'members'}->[$in{'index'}] if (! $in{'new'});

&terror('ets_err_notfound', $in{'timespace'}) if (! defined($ts));


&header($in{'new'} ? $text{'edate_titleadd'} : $text{'edate_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";


print "<FORM ACTION=\"save_date.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=timespace VALUE=\"$in{'timespace'}\">",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('edate_header', $in{'timespace'}), "</B></TD>\n",
      " </TR>\n",

      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "        <TD><B>$text{'edate_type'}</B></TD>\n",
      "        <TD><INPUT TYPE=radio NAME=datetype VALUE=\"1\"",
      (($st->{'stype'} eq 'date') || $in{'new'}) ? " CHECKED" : "",
      "> ",
      "$text{'edate_exact'}\n",
      "        <TD><INPUT TYPE=radio NAME=datetype VALUE=\"2\"",
      ($st->{'stype'} eq 'date_range') ? " CHECKED" : "",
      "> ",
      "$text{'edate_range'}\n",


      "    <TR>\n",
      "        <TD><B>$text{'edate_from'}</B></TD>\n",
      "        <TD><SELECT NAME=fromyear>\n",
      "<OPTION VALUE=*",
      ($st->{'syear'} eq '*') ? " SELECTED" : "",
      ">All\n";

my $year=(localtime(time))[5] + 1900;
my $month=(localtime(time))[4] + 1;
my $mday=(localtime(time))[3];

for ($year..$year+20) {
  print "<OPTION",
        (! $in{'new'} && ($_ == $st->{'syear'})) ? " SELECTED" : "",
        ($in{'new'} && ($_ == $year)) ? " SELECTED" : "",
        ">$_\n";
}

print "     </SELECT> /\n",
      "     <SELECT NAME=frommonth>\n",
      "<OPTION VALUE=*",
      ($st->{'smonth'} eq '*') ? " SELECTED" : "",
      ">All\n";

for (1..12) {
  print "<OPTION",
        (! $in{'new'} && ($_ == $st->{'smonth'})) ? " SELECTED" : "",
        ($in{'new'} && ($_ == $month)) ? " SELECTED" : "",
        ">$_\n";
}

print "     </SELECT> /\n",
      "     <SELECT NAME=fromday>\n",
      "<OPTION VALUE=*",
      ($st->{'sday'} eq '*') ? " SELECTED" : "",
      ">All\n";

for (1..31) {
  print "<OPTION",
        (! $in{'new'} && ($_ == $st->{'sday'})) ? " SELECTED" : "",
        ($in{'new'} && ($_ == $mday)) ? " SELECTED" : "",
        ">$_\n";
}

print "     </SELECT> $text{'edate_dateformat'}</TD>\n",
      "    </TR>\n",



      "    <TR>\n",
      "        <TD><B>$text{'edate_to'}</B></TD>\n",
      "        <TD><SELECT NAME=toyear>\n",
      "<OPTION VALUE=*",
      ($st->{'eyear'} eq '*') ? " SELECTED" : "",
      ">All\n";

for ($year..$year+20) {
  print "<OPTION",
        ($_ == $st->{'eyear'}) ? " SELECTED" : "",
        ">$_\n";
}

print "     </SELECT> /\n",
      "     <SELECT NAME=tomonth>\n",
      "<OPTION VALUE=*",
      ($st->{'emonth'} eq '*') ? " SELECTED" : "",
      ">All\n";

for (1..12) {
  print "<OPTION",
        ($_ == $st->{'emonth'}) ? " SELECTED" : "",
        ">$_\n";
}

print "     </SELECT> /\n",
      "     <SELECT NAME=today>\n",
      "<OPTION VALUE=*",
      ($st->{'eday'} eq '*') ? " SELECTED" : "",
      ">All\n";

for (1..31) {
  print "<OPTION",
        ($_ == $st->{'eday'}) ? " SELECTED" : "",
        ">$_\n";
}

print "     </SELECT> $text{'edate_dateformat'}</TD>\n",
      "    </TR>\n",


      "       <TR>\n",
      "        <TD><B>$text{'edate_fromtime'}</B></TD>\n",
      "        <TD><SELECT NAME=fromhour>";
for (0..23) {
  print "<OPTION",
        ($_ == $st->{'shour'}) ? " SELECTED" : "",
        ">$_\n";
}
print "            </SELECT> :\n",
      "<SELECT NAME=frommin>";
for (0..59) {
  print "<OPTION",
        ($_ == $st->{'smin'}) ? " SELECTED" : "",
        ">$_\n";
}
print "</SELECT>\n",
      "      $text{'edate_timeformat'}",
      "        </TD>\n",
      "       </TR>\n",



      "       <TR>\n",
      "        <TD><B>$text{'edate_totime'}</B></TD>\n",
      "        <TD><SELECT NAME=tohour>";
for (0..23) {
  print "<OPTION",
        ($_ == $st->{'ehour'}) ? " SELECTED" : "",
        ">$_\n";
}
print "            </SELECT> :\n",
      "<SELECT NAME=tomin>";
for (0..59) {
  print "<OPTION",
        ($_ == $st->{'emin'}) ? " SELECTED" : "",
        ">$_\n";
}
print "</SELECT>\n",
      "      $text{'edate_timeformat'}",
      "        </TD>\n",

      "       </TR>\n",


      
      "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      "</FORM><HR>";

&footer("edit_timespace.cgi?timespace=$in{'timespace'}", $text{'edate_return'});

### END of edit_date.cgi ###.
