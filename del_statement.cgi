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

#    Created  : 04.06.2001


require "./squidguard-lib.pl";

# ACL Checks
if ( (($in{'sectype'} eq 'source') && (! $access{'esource'})) ||
     (($in{'sectype'} eq 'dest') && (! $access{'edest'})) ||
     (($in{'sectype'} eq 'rewrite') && (! $access{'erewrite'})) ||
     (($in{'sectype'} eq 'time') && (! $access{'etimespace'})) ) {
  &terror('dst_acl');
}

@config = &parse_config();
my $sec=&find_section( 'sectype' => $in{'sectype'},
                       'secname' => $in{'secname'},
                       'config'  => \@config );

my $st;
$st=$sec->{'members'}->[$in{'index'}];

my $conf = &read_file_lines($config{'conf'});
splice(@$conf, $st->{'line'}, 1);
&flush_file_lines();

&redirect("edit_$in{'back'}.cgi?$in{'back'}=$in{'secname'}");

### END of del_statement.cgi ###.
