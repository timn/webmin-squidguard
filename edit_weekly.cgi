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
  &terror('eweekly_acl');
}

@config = &parse_config();

my $sec=&find_section( 'sectype' => "time",
                      'secname' => $in{'timespace'},
                      'config'  => \@config );

my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});

&terror('ets_err_notfound', $in{'timespace'}) if (! defined($sec));


&header($in{'new'} ? $text{'eweekly_titleadd'} : $text{'eweekly_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_weekly.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=timespace VALUE=\"$in{'timespace'}\">",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('eweekly_header', $in{'timespace'}), "</B></TD>\n",
      " </TR>\n",

      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD>\n",
      "      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0>\n",
      "       <TR>\n",
      "        <TD><B>$text{'eweekly_days'}</B></TD>\n",

      "        <TD><INPUT TYPE=radio NAME=daytype VALUE=1",
      ( ($st->{'days'} eq '*') || $in{'new'}) ? " CHECKED" : "", "> $text{'eweekly_all'}",
      "            <INPUT TYPE=radio NAME=daytype VALUE=2",
      ( ($st->{'days'} ne '*') && ! $in{'new'}) ? " CHECKED" : "", "> $text{'eweekly_selected'}<BR>\n",
      "        </TD>\n",
      "       </TR>\n",

      "       <TR>\n",
      "        <TD>&nbsp;</TD>\n",
      "        <TD><SELECT NAME=days MULTIPLE ROWS=7>",

      "<OPTION VALUE=m",
      ($st->{'days'} =~ /m/) ? " SELECTED" : "",
      ">$text{'eweekly_mon'}\n",

      "<OPTION VALUE=t",
      ($st->{'days'} =~ /t/) ? " SELECTED" : "",
      ">$text{'eweekly_tue'}\n",

      "<OPTION VALUE=w",
      ($st->{'days'} =~ /w/) ? " SELECTED" : "",
      ">$text{'eweekly_wed'}\n",
      "<OPTION VALUE=h",
      ($st->{'days'} =~ /h/) ? " SELECTED" : "",
      ">$text{'eweekly_thu'}\n",

      "<OPTION VALUE=f",
      ($st->{'days'} =~ /f/) ? " SELECTED" : "",
      ">$text{'eweekly_fri'}\n",

      "<OPTION VALUE=a",
      ($st->{'days'} =~ /a/) ? " SELECTED" : "",
      ">$text{'eweekly_sat'}\n",

      "<OPTION VALUE=s",
      ($st->{'days'} =~ /s/) ? " SELECTED" : "",
      ">$text{'eweekly_sun'}\n",

      "         </SELECT>\n",
      "        </TD>\n",
      "       </TR>\n",
      "      </TABLE>\n",
      "     </TD>\n",

      "     <TD> &nbsp; &nbsp; </TD>\n",

      "     <TD VALIGN=top>\n",
      "      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0>\n",
      "       <TR>\n",

      "        <TD><B>$text{'eweekly_from'}</B></TD>\n",
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
      "      $text{'eweekly_format'}",
      "        </TD>\n",

      "       </TR>\n",
      "       <TR>\n",


      "        <TD><B>$text{'eweekly_to'}</B></TD>\n",
      "        <TD><SELECT NAME=tohour>";


for (0..23) {
  print "<OPTION",
        ($_ == $st->{'ehour'}) ? " SELECTED" : "",
        ">$_\n";
}
print "         </SELECT> :\n",
      "     <SELECT NAME=tomin>";
for (0..59) {
  print "<OPTION",
        ($_ == $st->{'emin'}) ? " SELECTED" : "",
        ">$_\n";
}
print "         </SELECT>\n",
      "      $text{'eweekly_format'}",
      "        </TD>\n",
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

&footer("edit_timespace.cgi?timespace=$in{'timespace'}", $text{'eweekly_return'});

### END of edit_weekly.cgi ###.
