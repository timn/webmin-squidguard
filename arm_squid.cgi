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

#    Created  : 06.06.2001

# The file name is cool, right!? ;-)


require "./squidguard-lib.pl";
&error_setup($text{'arm_error'});

&foreign_require('squid', 'squid-lib.pl');
my $squidconf = &foreign_call('squid', 'get_config');

my $squidguard_command=&get_binary_path();

&terror('arm_sgnotfound') if (! -x $squidguard_command);
$squidguard_command .= " -c $config{'conf'}";

# my $dir = { 'name'   => "redirect_program",
#            'values' => [ $squidguard_command ] };

# &foreign_call('squid', 'save_directive', $squidconf, 'redirect_program', [ $dir ]);

local $dir = { 'name' => 'redirect_program', 'values' => [ $squidguard_command ] };
&foreign_call('squid', 'save_directive', $squidconf, 'redirect_program', [ $dir ]);

# Call the flush_file_lines function in the "sandbox"
# that we opened for the squid module with foreign_require.
# Not nice but needed.
&squid::flush_file_lines();

&redirect();

### END of arm_squid.cgi ###.
