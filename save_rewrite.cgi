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
if (! $access{'erewrite'}) {
  &terror('srew_acl');
}

@config = &parse_config();

&error_setup($text{'srew_error'});

my $sec=&find_section( 'sectype' => "rewrite",
                      'secname' => $in{'rewgroup'},
                      'config'  => \@config );
&terror('esg_err_notfound', $in{'rewgroup'}) if (! defined($sec));
my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


# Check input
&terror('sref_invalid') if (! ($in{'from'} && $in{'to'}) );

# Create a new line
my $newline = "s\@$in{'from'}\@$in{'to'}\@";

$newline .= "i" if ($in{'flagi'});
$newline .= "r" if ($in{'flagr'});
$newline .= "R" if ($in{'flagt'});

# Save the new line replacing the old one
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
  &redirect("edit_rewgroup.cgi?rewgroup=$in{'rewgroup'}");
} else {
  &redirect("edit_rewrite.cgi?rewgroup=$in{'rewgroup'}&index=$in{'index'}");
}

### END of save_rewrite.cgi ###.
