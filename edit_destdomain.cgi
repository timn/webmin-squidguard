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

#    Created  : 07.04.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'edest'}) {
  &terror('eddom_acl');
}

@config = &parse_config();

my $sec=&find_section( 'config' => \@config,
                       'sectype' => 'dest',
                       'secname' => $in{'destgroup'} );

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};


if ($sec->{'domainlist'} =~ /^\//) {
 open(FILE, $sec->{'domainlist'});
} else {
 open(FILE, "$dbhome/$sec->{'domainlist'}");
}
my @domains=<FILE>;
close(FILE);

my @dom=();
if ($in{'search'}) {
  # Soooo many domains, we need to search it

  for (my $i=0; $i<scalar(@domains); $i++) {
    next if ($domains[$i] =~ /^#/);
    if ($domains[$i] =~ /$in{'search'}/) {
      my %dom=();
      $dom{'name'} = $domains[$i];
      $dom{'index'} = $i;
      push(@dom, \%dom);
    }
  }
}


&header($in{'new'} ? $text{'eddom_titleadd'} : $text{'eddom_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_destdomain.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=destgroup VALUE=\"$in{'destgroup'}\">\n",
      "<INPUT TYPE=hidden NAME=index VALUE=\"$in{'index'}\">\n",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text($in{'new'} ? 'eddom_headeradd' : 'eddom_header', $in{'destgroup'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n";

if ($in{'search'}) {

  if (! scalar(@dom)) {
    # No matching domains found
    print "    <TR>\n",
          "     <TD><B>$text{'eddom_nosrchres'}</B></TD>\n",
          "     </TD>\n",
          "    </TR>\n";
    $nosubmit=1;

  } elsif (scalar(@dom) == 1) {
    # Exactly one matching record

    print "    <TR>\n",
          "     <TD><B>$text{'eddom_name'}</B></TD>\n",
          "     <TD><INPUT TYPE=text NAME=domain VALUE=\"$dom[0]->{'name'}\"> ",
          "     </TD>\n",
          "    </TR>\n",

  } else {
    # Multiple result

    print "    <TR>\n",
          "     <TD><B>$text{'eddom_multiple'}</B><BR><BR>&nbsp;</TD>\n",
          "    </TR>\n";

    foreach $d (@dom) {
      print "    <TR>\n",
            "     <TD><A HREF=\"edit_destdomain.cgi?destgroup=",
            "$in{'destgroup'}&index=$d->{'index'}\">$d->{'name'}</A></TD>\n",
            "    </TR>\n",
    }
  }


} else {
  # We do not need to search and got an explicit index
  chomp $domains[$in{'index'}];
  print "    <TR>\n",
        "     <TD><B>$text{'eddom_name'}</B></TD>\n",
        "     <TD><INPUT TYPE=text NAME=domain VALUE=\"",
        $in{'new'} ? "" : $domains[$in{'index'}],
        "\"> ",
        "     </TD>\n",
        "    </TR>\n";
}

print "   </TABLE>\n",
      "  </TD>",
      " </TR>",
      "</TABLE>\n",
      ($nosubmit) ? "" : "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      ($in{'new'} || $nosubmit) ? "" : "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"$text{'delete'}\">\n",
      "</FORM><HR>";


&footer("edit_destgroup.cgi?destgroup=$in{'destgroup'}", $text{'eddom_return'});

### END of edit_destdomain.cgi ###.