#!/usr/bin/perl
#
#    SquidGuard Webmin Module
#    Copyright (C) 2001 by Tim Niemueller <tim@niemueller.de>
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

require './squidguard-lib.pl';

&foreign_require('squid', 'squid-lib.pl');
my $squidconf = &foreign_call('squid', 'get_config');
my $directive = &foreign_call('squid', 'find_config', 'redirect_program', $squidconf);
my $squid_not_armed = ($directive->{'value'} =~ /squid[gG]uard/i) ? 0 : 1;
my $bin=&get_binary_path();

&header($text{'index_title'}, undef, "intro", 1, 1, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

if (! $config{'conf'}) {
  # Config file is not defined

  print "<H3>$text{'index_noconfhead'}</H3>\n",
        "$text{'index_noconfdesc'}",
        "<BR><FORM ACTION=save_config.cgi>",
        "<INPUT TYPE=text NAME=conf SIZE=50> ",
        &file_chooser_button('conf'),
        "<BR><INPUT TYPE=submit NAME=save VALUE=\"$text{'save'}\">",
        "</FORM>";
  &footer();

} elsif (! -e $config{'conf'}) {
  # Config is set but file does not exist

  print "<H3>$text{'index_nofilehead'}</H3>\n",
        "$text{'index_nofiledesc'}<BR><BR>",
        "<A HREF=\"create_plainconf.cgi\">$text{'create'}</A>";
  &footer();

} elsif (! $bin) {
  # Binary could not been found

  print "<H3>$text{'index_nobinhead'}</H3>\n",
        "$text{'index_nobindesc'}",
        "<BR><FORM ACTION=save_config.cgi>",
        "<INPUT TYPE=text NAME=binary SIZE=50> ",
        &file_chooser_button('binary'),
        "<BR><INPUT TYPE=submit NAME=save VALUE=\"$text{'save'}\">",
        "</FORM>";
  &footer();

} elsif ($squid_not_armed) {
  # Squid is not configured to use SquidGuard

  print "<H3>$text{'index_squidnotarmedhead'}</H3>\n",
        "$text{'index_squidnotarmedconf'}<BR><BR>",
        "<A HREF=\"arm_squid.cgi\">$text{'index_armsquid'}</A>";
  &footer();

} else {
  # Wow, everything is fine, show the menu :-)

  my @images = ("images/icon.paths.gif", "images/icon.timespaces.gif", "images/icon.sourcegroups.gif",
                "images/icon.destgroups.gif", "images/icon.rewgroups.gif", "images/icon.acls.gif",
                "images/icon.blacklist.gif");
  my @texts  = ($text{'index_paths'}, $text{'index_time'}, $text{'index_source'},
                $text{'index_dest'}, $text{'index_rewr'}, $text{'index_acl'},
                $text{'index_blacklist'});
  my @links  = ("edit_paths.cgi", "list_timespaces.cgi", "list_sourcegroups.cgi",
                "list_destgroups.cgi", "list_rewgroups.cgi", "list_acls.cgi",
                "list_blacklists.cgi");

  &icons_table(\@links, \@texts, \@images, 4);

  if ($_DEBUG) {
    my @config=&parse_config();

    print "--", scalar(@config), "<BR><BR>";
    foreach (@config) {
      print "$_->{'sectype'} - $_->{'secname'}<BR>\n";
      print "Mem: $_->{'members'}->[0]->{'days'}<BR>\n";
      print "Time: $_->{'members'}->[0]->{'time'}<BR>\n";
      print "Count: ", scalar(@{$_->{'members'}}), "<BR>\n";
    }
  }


  print "<HR>\n<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0 WIDTH=100%>\n",
        " <TR>\n",
        "  <TD ALIGN=right>[ v $version ]</TD>\n",
        " </TR>\n",
        "</TABLE>";

  &footer("/", $text{'index_return'});
}

### END of index.cgi ###.
