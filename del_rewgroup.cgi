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

#    Created  : 21.06.2001


require "./squidguard-lib.pl";

# ACL Checks
&terror('drg_acl') if (! $access{'erewrite'});

if (defined($in{'confirmed'})) {

  @config = &parse_config();
  my $sec=&find_section( 'sectype' => 'rewrite',
                         'secname' => $in{'rewgroup'},
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
    
    # Find all references and eliminate them, that's kinda job...
    # Only check ACL, rewgroups are only referenced there
    foreach $c (@config) {
      if ($c->{'sectype'} eq 'acl') {
        foreach $acl (@{$c->{'members'}}) {
          if (&indexof($in{'rewgroup'}, @{$acl->{'rewrite'}}) >= 0) {
            splice(@{$acl->{'rewrite'}}, &indexof($in{'rewgroup'}, @{$acl->{'rewrite'}}), 1);
            $conf->[$acl->{'rewrite_line'}] = "\t\trewrite " . join(' ', @{$acl->{'rewrite'}});
          }
        }
      }
    }

    &flush_file_lines();
    &redirect("list_rewgroups.cgi");
  }
} else {

  &header($text{'drg_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>\n\n",
        "<H3>", &text('drg_header', $in{'rewgroup'}), "</H3>\n",
        &text('drg_desription', $in{'rewgroup'}),
        "<BR><BR>",
        "<A HREF=\"del_rewgroup.cgi?rewgroup=$in{'rewgroup'}&confirmed=1\">",
        "$text{'drg_confirm'}</A><BR><BR><BR><BR>",
        "<HR>\n";
  &footer("edit_rewgroup.cgi?rewgroup=$in{'rewgroup'}", $text{'drg_return'});
}

### END of del_rewgroup.cgi ###.
