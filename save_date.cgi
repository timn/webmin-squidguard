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

#    Created  : 21.05.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'etimespace'}) {
  &terror('sdate_acl');
}

@config = &parse_config();
my $sec=&find_section( 'sectype' => "(time|date|date_range)",
                      'secname' => $in{'timespace'},
                      'config'  => \@config );

my $st;
$st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


&error_setup($text{'sdate_error'});

my $newline = "date ";

$in{'fromyear'} = sprintf("%0.4d", $in{'fromyear'}) if ($in{'fromyear'} ne '*');
$in{'frommonth'} = sprintf("%0.2d", $in{'frommonth'}) if ($in{'frommonth'} ne '*');
$in{'fromday'} = sprintf("%0.2d", $in{'fromday'}) if ($in{'fromday'} ne '*');

$newline .= "$in{'fromyear'}.$in{'frommonth'}.$in{'fromday'}";

if ($in{'datetype'} == 2) {
  $in{'toyear'} = sprintf("%0.4d", $in{'toyear'}) if ($in{'fromyear'} ne '*');
  $in{'tomonth'} = sprintf("%0.2d", $in{'tomonth'}) if ($in{'tomonth'} ne '*');
  $in{'today'} = sprintf("%0.2d", $in{'today'}) if ($in{'today'} ne '*');

  $newline .= "-$in{'toyear'}.$in{'tomonth'}.$in{'today'} ";
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
&sgchown($config{'conf'});

if ($in{'new'}) {
  &redirect("edit_timespace.cgi?timespace=$in{'timespace'}");
} else {
  &redirect("edit_date.cgi?timespace=$in{'timespace'}&index=$in{'index'}");
}

### END of save_date.cgi ###.
