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
&terror('dts_acl') if (! $access{'etimespace'});

if (defined($in{'confirmed'})) {

  @config = &parse_config();
  my $sec=&find_section( 'sectype' => 'time',
                         'secname' => $in{'timespace'},
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
    # Only check ACL, timespaces are only referenced there
    foreach $c (@config) {
      if ($c->{'sectype'} eq 'acl') {
        # ACL
        foreach $acl (@{$c->{'members'}}) {
          if ($acl->{'timespace'} eq $in{'timespace'}) {
            $conf->[$acl->{'line'}] = "\t$acl->{'source'} {";
          }
        }
      } elsif ($c->{'sectype'} eq 'dest') {
        # Destination Group
        if ($c->{'timespace'} eq $in{'timespace'}) {
          $conf->[$c->{'line'}] = "destination $c->{'secname'} {";
        }
      } elsif ($c->{'sectype'} eq 'source') {
        # Source Group
        if ($c->{'timespace'} eq $in{'timespace'}) {
          $conf->[$c->{'line'}] = "source $c->{'secname'} {";
        }
      } elsif ($c->{'sectype'} eq 'rewrite') {
        # Source Group
        if ($c->{'timespace'} eq $in{'timespace'}) {
          $conf->[$c->{'line'}] = "rewrite $c->{'secname'} {";
        }
      }
    }

    &flush_file_lines();
    &redirect("list_timespaces.cgi");
  }
} else {

  &header($text{'dts_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
  print "<HR><BR>\n\n",
        "<H3>", &text('dts_header', $in{'timespace'}), "</H3>\n",
        &text('dts_desription', $in{'timespace'}),
        "<BR><BR>",
        "<A HREF=\"del_timespace.cgi?timespace=$in{'timespace'}&confirmed=1\">",
        "$text{'dts_confirm'}</A><BR><BR><BR><BR>",
        "<HR>\n";
  &footer("edit_timespace.cgi?timespace=$in{'timespace'}", $text{'dts_return'});
}

### END of del_timespace.cgi ###.
