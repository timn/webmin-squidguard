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

#    Created  : 03.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'erewrite'}) {
  &terror('srt_acl');
}

@config = &parse_config();

&error_setup($text{'ssts_error'});

my $sec=&find_section( 'sectype' => "rewrite",
                       'secname' => $in{'rewgroup'},
                       'config'  => \@config );

&terror('erg_err_notfound', $in{'rewgroup'}) if (! defined($sec));


# Create a new line
my $newline = "rewrite $in{'rewgroup'}";
if ($in{'tstype'} ne 'none') {
  $newline .= " $in{'tstype'} $in{'timespace'}";
}
$newline .= " {";

# Save the new line replacing the old one
my $conf = &read_file_lines($config{'conf'});
$conf->[$sec->{'line'}]=$newline;
&flush_file_lines();
&sgchown($config{'conf'});

&redirect("edit_rewgroup.cgi?rewgroup=$in{'rewgroup'}");

### END of save_rewts.cgi ###.
