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
  &terror('esg_acl');
}

@config = parse_config();

my $sg=&find_section( 'sectype' => "source",
                      'secname' => $in{'sourcegroup'},
                      'config'  => \@config );

&terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sg));

&header($text{'esg_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('esg_header', $in{'sourcegroup'}), "</B></TD>\n",
      " </TR>\n",
      "</TABLE>\n";

my @images = ();
my @texts  = ();
my @links  = ();


for (my $i=0; $i < scalar(@{$sg->{'members'}}); $i++) {
 my $m=$sg->{'members'}->[$i];

 if ($m->{'stype'} eq 'ip') {
   push(@images, "images/host.gif");
   push(@texts, $m->{'ip'});
   push(@links, "edit_sourcehost.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 } elsif ($m->{'stype'} eq 'iprange') {
   push(@images, "images/group.gif");
   push(@texts, "$m->{'ip'}-$m->{'end'}");
   push(@links, "edit_sourcerange.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 } elsif ($m->{'stype'} eq 'subnet') {
   push(@images, "images/subnet.gif");
   push(@texts, "$m->{'ip'}/$m->{'prefix'}");
   push(@links, "edit_sourcesubnet.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 } elsif ($m->{'stype'} eq 'subnet_long') {
   push(@images, "images/subnet.gif");
   push(@texts, "$m->{'ip'}/$m->{'mask'}");
   push(@links, "edit_sourcelongsubnet.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 } elsif ($m->{'stype'} eq 'domain') {
   push(@images, "images/domain.gif");
   push(@texts, "$m->{'domain'}");
   push(@links, "edit_sourcedomain.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 } elsif ($m->{'stype'} eq 'user') {
   push(@images, "images/user.gif");
   push(@texts, "$m->{'user'}");
   push(@links, "edit_sourceuser.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 } elsif ($m->{'stype'} eq 'userlist') {
   push(@images, "images/userlist.gif");
   push(@texts, "$m->{'name'}");
   push(@links, "edit_sourceuserlist.cgi?sourcegroup=$in{'sourcegroup'}&index=$i");
 }

}


&icons_table(\@links, \@texts, \@images, 4);

if (! scalar(@links)) {
  print "$text{'esg_nost'}<BR><BR>\n";
}


print "<HR>",
      "<TABLE BORDER=0 WIDTH=100%>\n",
      " <TR>\n",
      "  <TD ALIGN=center WIDTH=15%><B>[</B> ",
      "<A HREF=\"edit_sourcehost.cgi?sourcegroup=$in{'sourcegroup'}&new=1\">",
      $text{'esg_addhost'}, "</A> <B>]</B></TD>\n",
      "  <TD ALIGN=center WIDTH=15%><B>[</B> ",
      "<A HREF=\"edit_sourcerange.cgi?sourcegroup=$in{'sourcegroup'}&new=1\">",
      $text{'esg_addrange'}, "</A> <B>]</B></TD>\n",
      "  <TD ALIGN=center WIDTH=15%><B>[</B> ",
      "<A HREF=\"edit_sourcesubnet.cgi?sourcegroup=$in{'sourcegroup'}&new=1\">",
      $text{'esg_addsubnet'}, "</A> <B>]</B></TD>\n",
      "  <TD ALIGN=center WIDTH=15%><B>[</B> ",
      "<A HREF=\"edit_sourcedomain.cgi?sourcegroup=$in{'sourcegroup'}&new=1\">",
      $text{'esg_adddomain'}, "</A> <B>]</B></TD>\n",
      "  <TD ALIGN=center WIDTH=15%><B>[</B> ",
      "<A HREF=\"edit_sourceuser.cgi?sourcegroup=$in{'sourcegroup'}&new=1\">",
      $text{'esg_adduser'}, "</A> <B>]</B></TD>\n",
      "  <TD ALIGN=center WIDTH=15%><B>[</B> ",
      "<A HREF=\"edit_sourceuserlist.cgi?sourcegroup=$in{'sourcegroup'}&new=1\">",
      $text{'esg_adduserlist'}, "</A> <B>]</B></TD>\n",
      " </TR>\n",
      "</TABLE>\n",
      "<HR>\n",
      "<TABLE BORDER=0>\n",
      "<FORM ACTION=\"save_sourcets.cgi\" METHOD=POST>",
      "<INPUT TYPE=hidden NAME=sourcegroup VALUE=\"$in{'sourcegroup'}\">",
      " <TR>\n",
      "  <TD>$text{'esg_timespace'}: </TD>\n",
      "  <TD><SELECT NAME=tstype>\n",
      "<OPTION VALUE=none",
      ($sg->{'tstype'} eq 'none') ? " SELECTED" : "",
      ">$text{'global_nots'}\n",
      "<OPTION VALUE=within",
      ($sg->{'tstype'} eq 'within') ? " SELECTED" : "",
      ">$text{'global_within'}\n",
      "<OPTION VALUE=outside",
      ($sg->{'tstype'} eq 'outside') ? " SELECTED" : "",
      ">$text{'global_outside'}\n",
      "   </SELECT>\n",
      "  </TD>\n",
      "  <TD><SELECT NAME=timespace>";

foreach $c (@config) {
  if ($c->{'sectype'} eq 'time') {
    print "<OPTION VALUE=\"$c->{'secname'}\"",
          ($sg->{'timespace'} eq $c->{'secname'}) ? " SELECTED" : "",
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
      "<B>[</B> <A HREF=\"del_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}\">",
      "$text{'esg_del'}</A> <B>]</B><HR>";

&footer("list_sourcegroups.cgi", $text{'esg_return'});

### END of edit_sourcegroup.cgi ###.
