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
if (! $access{'edest'}) {
  &terror('edg_acl');
}

@config = &parse_config();

my $sec=&find_section( 'config' => \@config,
                       'sectype' => 'dest',
                       'secname' => $in{'destgroup'} );

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};

&terror('edg_err_notfound', $in{'destgroup'}) if (! defined($sec));


&header($text{'edg_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>\n\n";

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('edg_domains', $in{'destgroup'}), "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n";

if ($sec->{'domainlist'} =~ /^\//) {
 open(FILE, $sec->{'domainlist'});
} else {
 open(FILE, "$dbhome/$sec->{'domainlist'}");
}
 my @file=<FILE>;
close(FILE);

my @domains=();
for (my $i=0; $i < @file; $i++) {
  next if ($file[$i] =~ /^#/);
  chomp $file[$i];
  my %dom=();
  $dom{'name'} = $file[$i];
  $dom{'index'} = $i;
  push(@domains, \%dom);
}
@domains = sort { $a->{'name'} cmp $b->{'name'} } @domains;


if ((scalar(@domains) > 40) && (! $in{'listdomains'})) {
  print "<TR><TD>",
        "<FORM ACTION=\"edit_destdomain.cgi\">\n",
        "<INPUT TYPE=hidden NAME=destgroup VALUE=\"$in{'destgroup'}\">",
        "<INPUT TYPE=text NAME=search> ",
        "<INPUT TYPE=submit VALUE=\"$text{'edg_search'}\">\n",
        "</TD></FORM></TR>",
        "<TR><TD>\n",
        "<A HREF=\"edit_destgroup.cgi?destgroup=$in{'destgroup'}&listdomains=1\">",
        "$text{'edg_list'}</A></TD></TR>";

} else {
  for (my $i=0; $i<scalar(@domains); $i++) {
    print "    <TR>\n" if (($i % 4)==0);
    print "     <TD WIDTH=25%><A HREF=\"edit_destdomain.cgi?destgroup=$in{'destgroup'}&index=$domains[$i]->{'index'}\">$domains[$i]->{'name'}</A></TD>\n";
    print "    </TR>\n" if (($i % 4)==3);

  }
}


print "    </TR>\n" if ((scalar(@domains) % 4)!=0);

if (! scalar(@domains)) {
  print "<TR><TD>$text{'edg_nodom'}</TD></TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<B>[</B> <A HREF=\"edit_destdomain.cgi?destgroup=$in{'destgroup'}&new=1\">$text{'edg_adddomain'}</A> <B>]</B><BR><BR>\n";





print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('edg_urls', $in{'destgroup'}), "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n";


if ($sec->{'urllist'} =~ /^\//) {
 open(FILE, $sec->{'urllist'});
} else {
 open(FILE, "$dbhome/$sec->{'urllist'}");
}
 my @file=<FILE>;
close(FILE);

my @urls=();
for (my $i=0; $i < @file; $i++) {
  next if ($file[$i] =~ /^#/);
  chomp $file[$i];
  my %dom=();
  $dom{'name'} = $file[$i];
  $dom{'index'} = $i;
  push(@urls, \%dom);
}
@urls = sort { $a->{'name'} cmp $b->{'name'} } @urls;

if ((scalar(@urls) > 40) && (! $in{'listurls'})) {
  print "<TR><TD>",
        "<FORM ACTION=\"edit_desturl.cgi\">\n",
        "<INPUT TYPE=hidden NAME=destgroup VALUE=\"$in{'destgroup'}\">",
        "<INPUT TYPE=text NAME=search> ",
        "<INPUT TYPE=submit VALUE=\"$text{'edg_search'}\">\n",
        "</TD></FORM></TR>",
        "<TR><TD>\n",
        "<A HREF=\"edit_destgroup.cgi?destgroup=$in{'destgroup'}&listurls=1\">",
        "$text{'edg_list'}</A></TD></TR>";

} else {
  for (my $i=0; $i<scalar(@urls); $i++) {
    print "    <TR>\n" if (($i % 4)==0);
    print "     <TD WIDTH=25%><A HREF=\"edit_desturl.cgi?destgroup=$in{'destgroup'}&index=$urls[$i]->{'index'}\">$urls[$i]->{'name'}</A></TD>\n";
    print "    </TR>\n" if (($i % 4)==3);

  }
}


print "    </TR>\n" if ((scalar(@urls) % 4)!=0);

if (! scalar(@urls)) {
  print "<TR><TD>$text{'edg_nourl'}</TD></TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<B>[</B> <A HREF=\"edit_desturl.cgi?destgroup=$in{'destgroup'}&new=1\">$text{'edg_addurl'}</A> <B>]</B><BR><BR>\n";






print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>", &text('edg_expressions', $in{'destgroup'}), "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n";


if ($sec->{'exprlist'} =~ /^\//) {
 open(FILE, $sec->{'exprlist'});
} else {
 open(FILE, "$dbhome/$sec->{'exprlist'}");
}
my @exprs=<FILE>;
close(FILE);

if ((scalar(@exprs) > 20) && (! $in{'listexprs'})) {
  print "<TR><TD>",
        "<FORM ACTION=\"edit_destexpr.cgi\">\n",
        "<INPUT TYPE=hidden NAME=destgroup VALUE=\"$in{'destgroup'}\">",
        "<INPUT TYPE=text NAME=search> ",
        "<INPUT TYPE=submit VALUE=\"$text{'edg_search'}\">\n",
        "</TD></FORM></TR>",
        "<TR><TD>\n",
        "<A HREF=\"edit_destgroup.cgi?destgroup=$in{'destgroup'}&listexprs=1\">",
        "$text{'edg_list'}</A></TD></TR>";

} else {
  for (my $i=0; $i<scalar(@exprs); $i++) {
    chomp $exprs[$i];

    print "    <TR>\n",
          "     <TD WIDTH=100%><A HREF=\"edit_destexpr.cgi?destgroup=$in{'destgroup'}&index=$i\">",
          (length($exprs[$i]) > 100) ? substr($exprs[$i], 0, 100)."..." : $exprs[$i],
          "</A></TD>\n";
          "    </TR>\n";

  }
}


print "    </TR>\n" if ((scalar(@exprs) % 4)!=0);

if (! scalar(@exprs)) {
  print "<TR><TD>$text{'edg_noexpr'}</TD></TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<B>[</B> <A HREF=\"edit_destexpr.cgi?destgroup=$in{'destgroup'}&new=1\">$text{'edg_addexpr'}</A> <B>]</B><BR><BR>\n";



print "<HR>\n",
      "<TABLE BORDER=0>\n",
      "<FORM ACTION=\"save_destts.cgi\" METHOD=POST>",
      "<INPUT TYPE=hidden NAME=destgroup VALUE=\"$in{'destgroup'}\">",
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
      "<B>[</B> <A HREF=\"del_destgroup.cgi?destgroup=$in{'destgroup'}\">",
      "$text{'edg_del'}</A> <B>]</B><HR>";

&footer("list_destgroups.cgi", $text{'edg_return'});

### END of edit_destgroup.cgi ###.
