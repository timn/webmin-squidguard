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

#    Created  : 18.06.2001


require "./squidguard-lib.pl";

# ACL Checks
&terror('dbl_acl') if (! $access{'edest'});

if (defined($in{'confirmed'})) {

  @config = &parse_config();
  my $sec=&find_section( 'sectype' => 'dest',
                         'secname' => "bl_$in{'blacklist'}",
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
    # Only check ACL, destgroups are only referenced there
    foreach $c (@config) {
      if ($c->{'sectype'} eq 'acl') {
        foreach $acl (@{$c->{'members'}}) {
          if (&indexof("bl_$in{'blacklist'}", @{$acl->{'pass'}}) >= 0) {
            splice(@{$acl->{'pass'}}, &indexof("bl_$in{'blacklist'}", @{$acl->{'pass'}}), 1);
            $conf->[$acl->{'pass_line'}] = "\t\tpass " . join(' ', @{$acl->{'pass'}});
          }
        }
      }
    }

    &flush_file_lines();
    &redirect("edit_blacklist.cgi?blacklist=$in{'blacklist'}");
  }
} else {

  &header($text{'dbl_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>\n\n",
        "<H3>", &text('dbl_header', $in{'blacklist'}), "</H3>\n",
        &text('dbl_desription', $in{'blacklist'}),
        "<BR><BR>",
        "<A HREF=\"disable_blacklist.cgi?blacklist=$in{'blacklist'}&confirmed=1\">",
        "$text{'dbl_confirm'}</A><BR><BR><BR><BR>",
        "<HR>\n";
  &footer("edit_blacklist.cgi?blacklist=$in{'blacklist'}", $text{'dbl_return'});
}

### END of disable_blacklist.cgi ###.
