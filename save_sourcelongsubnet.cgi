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
if (! $access{'esource'}) {
  &terror('ssls_acl');
}

&error_setup($text{'ssls_error'});


if (defined($in{'delete'})) {
  &redirect("del_statement.cgi?sectype=source&secname=$in{'sourcegroup'}&index=$in{'index'}&back=sourcegroup");
} else {

  @config = &parse_config();


  my $sg=&find_section( 'sectype' => "source",
                        'secname' => $in{'sourcegroup'},
                        'config'  => \@config );
  &terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sg));
  my $st=$sg->{'members'}->[$in{'index'}];


  # Check input
  &terror('ssls_inv_net') if ($in{'net'} !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
  &terror('ssls_inv_mask') if ($in{'mask'} !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);

  # Create a new line
  my $newline = "ip\t\t$in{'net'}/$in{'mask'}";

  # Save the new line replacing the old one
  my $conf = &read_file_lines($config{'conf'});
  $conf->[$st->{'line'}]="\t$newline";
  &flush_file_lines();
  &sgchown($config{'conf'});

  # Go back to the edit page of this item
  &redirect("edit_sourcelongsubnet.cgi?sourcegroup=$in{'sourcegroup'}&index=$in{'index'}");

}

### END of save_sourcelongsubnet.cgi ###.
