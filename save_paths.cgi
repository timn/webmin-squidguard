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

#    Created  : 20.05.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'epaths'}) {
  &terror('spaths_acl');
}

@config = &parse_config();
my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $logsec=&find_section( 'config' => \@config,
                         'sectype' => 'logdir' );

&error_setup('spaths_error');
&terror('spaths_logdir') if (! -d $in{'logdir'});
&terror('spaths_dbhome') if (! -d $in{'dbhome'});

my $conf = &read_file_lines($config{'conf'});
$conf->[$dbsec->{'line'}]="dbhome $in{'dbhome'}";
$conf->[$logsec->{'line'}]="logdir $in{'logdir'}";
&flush_file_lines();

&redirect("edit_paths.cgi");

### END of save_paths.cgi ###.
