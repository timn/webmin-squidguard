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

#    Created  : 23.05.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'edest'}) {
  &terror('sde_acl');
}

@config = &parse_config();

&error_setup($text{'sde_error'});

my $sec=&find_section( 'sectype' => "dest",
                      'secname' => $in{'destgroup'},
                      'config'  => \@config );

my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );

my $dbhome=$dbsec->{'dbhome'};


# Error if group could not been found
# WRITEME


if (defined($in{'delete'})) {
  # Delete the entry...


  my $file;
  my $filename;
  if ($sec->{'exprlist'} =~ /^\//) {
    $filename=$sec->{'exprlist'};
  } else {
    $filename="$dbhome/$sec->{'exprlist'}";
  }
  # Read "manually" (and not with read_file_lines) because
  # otherwise the files gets "re-created" after flush_file_lines
  # that is done AFTER the unlink. So delete would not work...
  open(FILE, $filename);
  @file=<FILE>;
  close(FILE);


  splice(@file, $in{'index'}, 1);

  if (! scalar(@file)) {
    # File is empty, delete it and remove config entry

    if (-f $filename) {
      # Is a regular file
      unlink $filename;
      if (-f "${filename}.db") {
        unlink("${filename}.db");
      }
      my $conf = &read_file_lines($config{'conf'});
      splice(@$conf, $sec->{'exprlist_line'}, 1);
    } # else {
    # Could be an error message. We just leave it. Maybe
    # the author of the config had reasons
    # }
  } else {
    # Save back to disk
    open(FILE, ">$filename");
      print FILE @file;
    close(FILE);
    &sgchown($filename);
  }

} else {

  # Check input
  &terror('sde_invalid') if ($in{'expr'} !~ /^\S+$/);


  # Check if file for items exists
  if (! $sec->{'exprlist'}) {
    # It does not exist, create one
    if (-e "$dbhome/$in{'destgroup'}.destexprlist") {
      # Standard file exists, try some other
      my $i=1;
      while (($i < 500) && (-e "$dbhome/$in{'destgroup'}-$i.destexprlist")) {
        $i++;
      }
      if (-e "$dbhome/$in{'destgroup'}-$i.destexprlist") {
        # Cannot get a filename
        &terror('sdu_nofilename');
      } else {
        # We found a valid filename
        $sec->{'exprlist'} = "$in{'destgroup'}-$i.destexprlist";
      }
    } else {
      # OK, Standard Filename
      $sec->{'exprlist'} = "$in{'destgroup'}.destexprlist";
    }

    # We have to set the new value in the config file!
    my $conf = &read_file_lines($config{'conf'});
    my @newlines=($conf->[$sec->{'line'}],
                "\texpressionlist\t\t$sec->{'exprlist'}" );
    splice(@$conf, $sec->{'line'}, 1, @newlines);

  }


  # Save the new line replacing the old one
  my $filename;
  if ($sec->{'exprlist'} =~ /^\//) {
    $filename=$sec->{'exprlist'};
  } else {
    $filename="$dbhome/$sec->{'exprlist'}";
  }
  my $file=&read_file_lines($filename);

  if ($in{'new'}) {
    # Adding a new statement
    push(@$file, $in{'expr'});
  } else {
    # Modifying a statement
    $file->[$in{'index'}]="$in{'expr'}";
  }

  &flush_file_lines();
  &rebuild_db($filename);


}



if (defined($in{'new'}) || defined($in{'delete'})) {
  &redirect("edit_destgroup.cgi?destgroup=$in{'destgroup'}");
} else {
  &redirect("edit_destexpr.cgi?destgroup=$in{'destgroup'}&index=$in{'index'}");
}

### END of save_destexpr.cgi ###.
