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

#    Created  : 25.05.2001


require "./squidguard-lib.pl";

# ACL Checks
if (! $access{'edest'}) {
  &terror('adg_acl');
}

&terror('global_reserved') if ($in{'name'} =~ /^bl_/);

@config = &parse_config();

my $line=-1;
for (my $i=0; $i < scalar(@config); $i++) {

  # Find section where we PREpend our new section
  # The sections have a specific order they have
  # to appear in. So we check from the first down
  # to the last and take the first match

  # We do not search for "time" and "dest" sections,
  #  since these sections have to be created AFTER
  # all time sections

  if ($config[$i]->{'sectype'} eq "dest") {
    $line = $config[$i]->{'line'};
    last;

  } elsif ($config[$i]->{'sectype'} eq "rewrite") {
    $line = $config[$i]->{'line'};
    last;

  } elsif ($config[$i]->{'sectype'} eq "acl") {
    $line = $config[$i]->{'line'};
    last;

  } # else {
    # Nothing, could be a dbhome or logdir section
    # we catch a "no line found" later
    # }
}

# Some Debug code just to be cool
# &header("TEST");
# print $line, "<BR>\n";
# &footer();


# Read the config file
my $conf = &read_file_lines($config{'conf'});

if ($line < 0) {
  # No section!? That's strange but possible, so
  # we just append the new section to the file!

  push(@$conf, "", "destination $in{'name'} {", "}");
} else {
  # we found a section we want to prepend our
  # new section to

  my @newlines=( "destination $in{'name'} {",
                 "}",
                 "",
                 $conf->[$line] );

  splice(@$conf, $line, 1, @newlines);
}

&flush_file_lines();

&redirect("list_destgroups.cgi");

### END of add_destgroup.cgi ###.
