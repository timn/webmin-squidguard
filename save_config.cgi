#!/usr/bin/perl

#    SquidGuard Configuration Webmin Module Library
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

#    Created  : 06.06.2001
#    Partly taken from IPchains Firewalling Module

require './squidguard-lib.pl';

&read_file("$config_directory/$module_name/config", \%config);

for (keys %in) {
  next if ($_ eq 'save');
  $config{$_} = $in{$_};
}

mkdir("$config_directory/$module_name", 0700);
&write_file("$config_directory/$module_name/config", \%config);
&redirect("");

### END of save_config.cgi ###.
