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

#    Created  : 17.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'eblacklist'}) {
  &terror('sbu_acl');
}

@config = &parse_config();
&error_setup($text{'sbu_error'});

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};
my $filename="$dbhome/blacklists/$in{'blacklist'}/urls";
my $file=&read_file_lines($filename);

if (defined($in{'delete'})) {
  # Delete the entry...
  splice(@$file, $in{'index'}, 1);

} else {

  # Check input
  &terror('sbu_invalid') if ($in{'url'} !~ /^\S+$/);


  if ($in{'new'}) {
    # Adding a new statement
    push(@$file, $in{'url'});
  } else {
    # Modifying a statement
    $file->[$in{'index'}]="$in{'url'}";
  }


}

# Save back to disk, we do that ALWAYS and do NOT
# delete and empty file for blacklist "compatibility"
&flush_file_lines();
&rebuild_db($filename);


if (defined($in{'new'}) || defined($in{'delete'})) {
  &redirect("edit_blacklist.cgi?blacklist=$in{'blacklist'}");
} else {
  &redirect("edit_blurl.cgi?blacklist=$in{'blacklist'}&index=$in{'index'}");
}



### END of save_blurl.cgi ###.
