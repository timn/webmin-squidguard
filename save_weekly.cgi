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
if (! $access{'etimespace'}) {
  &terror('sweekly_acl');
}

@config = &parse_config();
my $sec=&find_section( 'sectype' => "(time|date|date_range)",
                      'secname' => $in{'timespace'},
                      'config'  => \@config );
my $st;
$st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});

&error_setup($text{'sweekly_error'});

my $newline = "weekly ";

if ($in{'daytype'} == 1) {
  $newline .= '*';
} else {
  $newline .= join('', split(/\0/, $in{'days'}));
}

$in{'fromhour'} = ($in{'fromhour'} < 10) ? "0$in{'fromhour'}" : $in{'fromhour'};
$in{'frommin'} = ($in{'frommin'} < 10) ? "0$in{'frommin'}" : $in{'frommin'};
$in{'tohour'} = ($in{'tohour'} < 10) ? "0$in{'tohour'}" : $in{'tohour'};
$in{'tomin'} = ($in{'tomin'} < 10) ? "0$in{'tomin'}" : $in{'tomin'};

$newline .= " $in{'fromhour'}:$in{'frommin'} -";
$newline .= " $in{'tohour'}:$in{'tomin'}";

my $conf = &read_file_lines($config{'conf'});
if ($in{'new'}) {
  # Adding a new statement
  my @newlines=($conf->[$sec->{'line'}],
                "\t$newline" );
  splice(@$conf, $sec->{'line'}, 1, @newlines);
} else {
  # Modifying a statement
  $conf->[$st->{'line'}]="\t$newline";
}
&flush_file_lines();
&chown($config{'conf'});

if ($in{'new'}) {
  &redirect("edit_timespace.cgi?timespace=$in{'timespace'}");
} else {
  &redirect("edit_weekly.cgi?timespace=$in{'timespace'}&index=$in{'index'}");
}

### END of save_weekly.cgi ###.
