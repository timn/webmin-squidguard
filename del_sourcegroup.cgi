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

#    Created  : 19.06.2001


require "./squidguard-lib.pl";

# ACL Checks
&terror('ddg_acl') if (! $access{'esource'});

if (defined($in{'confirmed'})) {

  @config = &parse_config();
  my $sec=&find_section( 'sectype' => 'source',
                         'secname' => $in{'sourcegroup'},
                         'config'  => \@config );

  # Number of lines to be deleted, +1 to include interval border
  my $count = $sec->{'end_line'} - $sec->{'line'} + 1;


  if ($_DEBUG) {
    &header("DEBUG");
    print "Start: $sec->{'line'}<BR>\n",
          "End: $sec->{'end_line'}<BR>\n",
          "Count: $count<BR>\n";
    &footer();
  } else {
    my $conf = &read_file_lines($config{'conf'});
    splice(@$conf, $sec->{'line'}, $count);
    &flush_file_lines();

    @config = &parse_config();
    my $conf = &read_file_lines($config{'conf'});

    # Find all references and eliminate them, that's kinda job...
    # Only check ACL, sourcegroups are only referenced there
    foreach $c (@config) {
      if ($c->{'sectype'} eq 'acl') {
        foreach $acl (reverse sort { $a->{'line'} cmp $b->{'line'} } @{$c->{'members'}}) {
          # reverse sort because:
          # if we need to splice some entries, we start at the END.
          # Otherwise line numbers of coming acl_items would be
          # wrong since there would be fewer lines in the file...
          # Not nice code but working (I hope :-)
          if ($acl->{'source'} eq $in{'sourcegroup'}) {
            my $aclcount = $acl->{'end_line'} - $acl->{'line'} + 1;
            splice(@$conf, $acl->{'line'}, $aclcount);
          }
        }
        # Stop here. Ther IS only ONE ACL section, so we do not
        # need to read further
        last;
      }
    }
    &flush_file_lines();
    &redirect("list_sourcegroups.cgi");
  }
} else {

  &header($text{'dsg_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>\n\n",
        "<H3>", &text('dsg_header', $in{'sourcegroup'}), "</H3>\n",
        &text('dsg_desription', $in{'sourcegroup'}),
        "<BR><BR>",
        "<A HREF=\"del_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}&confirmed=1\">",
        "$text{'dsg_confirm'}</A><BR><BR><BR><BR>",
        "<HR>\n";
  &footer("edit_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}", $text{'dsg_return'});
}

### END of del_section.cgi ###.
