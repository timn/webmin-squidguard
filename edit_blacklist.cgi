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

#    Created  : 17.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'eblacklist'}) {
  &terror('ebl_acl');
}

@config = &parse_config();

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};

my $enabled=0;
foreach $c (@config) {
  if ( ($c->{'sectype'} eq 'dest') &&
       ($c->{'secname'} eq "bl_$in{'blacklist'}")) {
    $enabled = 1;
  }
}

&header($text{'ebl_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>\n\n";

print &text('ebl_status', $enabled ? $text{'ebl_sten'} : $text{'ebl_stdis'}),
      "<BR><BR>";


print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'ebl_domains'}</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n";

my @domains=();
if (-e "$dbhome/blacklists/$in{'blacklist'}/domains") {
  # Read File if it exists
  open(FILE, "$dbhome/blacklists/$in{'blacklist'}/domains");
   my @file=<FILE>;
  close(FILE);

  for (my $i=0; $i < @file; $i++) {
    next if ($file[$i] =~ /^#/);
    chomp $file[$i];
    my %dom=();
    $dom{'name'} = $file[$i];
    $dom{'index'} = $i;
    push(@domains, \%dom);
  }
@domains = sort { $a->{'name'} cmp $b->{'name'} } @domains;
}


if (scalar(@domains)) {
  if ((scalar(@domains) > 40) && (! $in{'listdomains'})) {
    print "<TR><TD>",
          "<FORM ACTION=\"edit_bldomain.cgi\">\n",
          "<INPUT TYPE=hidden NAME=blacklist VALUE=\"$in{'blacklist'}\">",
          "<INPUT TYPE=text NAME=search> ",
          "<INPUT TYPE=submit VALUE=\"$text{'ebl_search'}\">\n",
          "</TD></FORM></TR>",
          "<TR><TD>\n",
          "<A HREF=\"edit_blacklist.cgi?blacklist=$in{'blacklist'}&listdomains=1\">",
          "$text{'ebl_list'}</A></TD></TR>";
  } else {
    for (my $i=0; $i < scalar(@domains); $i++) {

      print "    <TR>\n" if (($i % 4)==0);
      print "     <TD WIDTH=25%><A HREF=\"edit_bldomain.cgi?blacklist=$in{'blacklist'}&index=$domains[$i]->{'index'}\">$domains[$i]->{'name'}</A></TD>\n";
      print "    </TR>\n" if (($i % 4)==3);

    }
    print "    </TR>\n" if ((scalar(@domains) % 4)!=0);
  }
} else {
  print "<TR><TD>$text{'ebl_nodom'}</TD></TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<B>[</B> <A HREF=\"edit_bldomain.cgi?blacklist=$in{'blacklist'}&new=1\">$text{'ebl_adddomain'}</A> <B>]</B><BR><BR>\n";



## URLs

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'ebl_urls'}</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=4 WIDTH=100%>\n";

my @urls=();
if (-e "$dbhome/blacklists/$in{'blacklist'}/urls") {
  # Read File if it exists
  open(FILE, "$dbhome/blacklists/$in{'blacklist'}/urls");
   my @file=<FILE>;
  close(FILE);

  for (my $i=0; $i < @file; $i++) {
    next if ($file[$i] =~ /^#/);
    chomp $file[$i];
    my %url=();
    $url{'name'} = $file[$i];
    $url{'index'} = $i;
    push(@urls, \%url);
  }
@urls = sort { $a->{'name'} cmp $b->{'name'} } @urls;
}

if (scalar(@urls)) {
  if ((scalar(@urls) > 40) && (! $in{'listurls'})) {
    print "<TR><TD>",
          "<FORM ACTION=\"edit_blurl.cgi\">\n",
          "<INPUT TYPE=hidden NAME=blacklist VALUE=\"$in{'blacklist'}\">",
          "<INPUT TYPE=text NAME=search> ",
          "<INPUT TYPE=submit VALUE=\"$text{'ebl_search'}\">\n",
          "</TD></FORM></TR>",
          "<TR><TD>\n",
          "<A HREF=\"edit_blacklist.cgi?blacklist=$in{'blacklist'}&listurls=1\">",
          "$text{'ebl_list'}</A></TD></TR>";
  } else {
    for (my $i=0; $i < scalar(@urls); $i++) {

      print "    <TR>\n" if (($i % 4)==0);
      print "     <TD WIDTH=25%><A HREF=\"edit_blurl.cgi?blacklist=$in{'blacklist'}&index=$urls[$i]->{'index'}\">$urls[$i]->{'name'}</A></TD>\n";
      print "    </TR>\n" if (($i % 4)==3);
    }
    print "    </TR>\n" if ((scalar(@urls) % 4)!=0);
  }

} else {
  print "<TR><TD>$text{'ebl_nourl'}</TD></TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      "<B>[</B> <A HREF=\"edit_blurl.cgi?blacklist=$in{'blacklist'}&new=1\">$text{'ebl_addurl'}</A> <B>]</B><BR><BR>\n";



print "<HR>\n",
      ($enabled)
        ? "<B>[</B> <A HREF=\"disable_blacklist.cgi?blacklist=$in{'blacklist'}\">$text{'ebl_disable'}</A> <B>]</B><BR><BR>\n"
        : "<B>[</B> <A HREF=\"enable_blacklist.cgi?blacklist=$in{'blacklist'}\">$text{'ebl_enable'}</A> <B>]</B><BR><BR>\n",
      "<HR>\n";

&footer("list_blacklists.cgi", $text{'ebl_return'});

### END of edit_blacklist.cgi ###.
