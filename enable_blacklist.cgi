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

&error_setup($text{'enbl_error'});

# ACL Checks
if (! $access{'eblacklist'}) {
  &terror('enbl_acl');
}

@config = &parse_config();

my $enabled=0;
foreach $c (@config) {
  if ( ($c->{'sectype'} eq 'dest') &&
       ($c->{'secname'} eq "bl_$in{'blacklist'}")) {
    $enabled = 1;
  }
}

&terror('enbl_already') if ($enabled);

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};

&terror('enbl_notexist') if (! -d "$dbhome/blacklists/$in{'blacklist'}");
&terror('enbl_nodata') if ( (! -e "$dbhome/blacklists/$in{'blacklist'}/domains") ||
                            (! -e "$dbhome/blacklists/$in{'blacklist'}/urls") );

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

# Read the config file
my $conf = &read_file_lines($config{'conf'});

my @section = ("destination bl_$in{'blacklist'} {");

foreach ('domain', 'url') {
	my $filename = "$dbhome/blacklists/$in{'blacklist'}/${_}s";
	next if (! -e $filename);
	push(@section, "\t${_}list\t\tblacklists/$in{'blacklist'}/${_}s")
	 if (-e "${filename}.db");

  my @list = stat $filename;
  my @db = stat "${filename}.db";
  next if ($db[9] > $list[9]); # 9 is 'mtime'

	&rebuild_db($filename);
}

push(@section, "}");

if ($line < 0) {
  # No section!? That's strange but possible, so
  # we just append the new section to the file!

  push(@$conf, "", @section);
} else {
  # we found a section we want to prepend our
  # new section to

  my @newlines=( @section,
                 "",
                 $conf->[$line] );

  splice(@$conf, $line, 1, @newlines);
}

&flush_file_lines();
&redirect("edit_blacklist.cgi?blacklist=$in{'blacklist'}");

### END of enable_blacklist.cgi ###.
