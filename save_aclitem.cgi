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
if (! $access{'eacl'}) {
  &terror('sai_acl');
}

@config = &parse_config();

&error_setup($text{'ssd_error'});

&terror('sacl_none') if (! $in{'source'});
&terror('sacl_default') if ( ($in{'source'} eq 'default') &&
                             defined($in{'delete'}) );


my $sec=&find_section( 'sectype' => "acl",
                       'config'  => \@config );

&terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sec));
my $acl=$sec->{'members'}->[$in{'aclindex'}] if (! $in{'new'});

# Check input


# Read File
my $conf = &read_file_lines($config{'conf'});


if (defined($in{'delete'})) {
  # Delete an entry

  my $count= $acl->{'end_line'} - $acl->{'line'} + 1;
  splice(@$conf, $acl->{'line'}, $count);

  # Flush File
  &flush_file_lines();
  &sgchown($config{'conf'});
  &redirect("list_acls.cgi");


} else {

  # Modify an entry

  if ( ($in{'tstype'} ne $acl->{'tstype'}) ||
       ($in{'timespace'} ne $acl->{'timespace'}) ||
       ($in{'source'} ne $acl->{'source'}) ) {

    my $new_headline="\t$in{'source'}";
    if ($in{'tstype'} ne 'none') {
      $new_headline .= " $in{'tstype'} $in{'timespace'}";
    }
    $new_headline .= " {";

    $conf->[$acl->{'line'}] = $new_headline;
  }

  # We use an array for new lines so that we do no need to
  # reparse the file (for current line numbers) after inserting
  # a new statement.
  my @newlines=($conf->[$acl->{'line'}]);

  my @pass = split(/\0/, $in{'pass'});
  my @blacklists = split(/\0/, $in{'blacklists'});
  if (scalar(@pass)) {
    if (defined($acl->{'pass_line'})) {
      # It's a modify
      $conf->[$acl->{'pass_line'}] = "\t\t" . join(' ', "pass", @blacklists, @pass);
    } else {
      # It's new
      push(@newlines, "\t\tpass ". join(' ', @blacklists, @pass));
    }
  }

  my @rew = split(/\0/, $in{'rewrite'});
  if (scalar(@rew)) {
    if (defined($acl->{'rewrite_line'})) {
      # It's a modify
      $conf->[$acl->{'rewrite_line'}] = "\t\t" . join(' ', "rewrite", @rew);
    } else {
      # It's new
      push(@newlines, "\t\trewrite ". join(' ', @rew));
    }
  }

  if ($in{'redurl'}) {
    my $new_redirect = "\t\tredirect ";
    $new_redirect .= ($in{'redmode'}) ? "$in{'redmode'}:" : "";
    $new_redirect .= $in{'redurl'};
  
    if (defined($acl->{'redirect_line'})) {
      # It's a modify
      $conf->[$acl->{'redirect_line'}] = $new_redirect;
    } else {
      # It's new
      push(@newlines, $new_redirect);
    }
  }

  if (scalar(@newlines) > 1) {
    # New lines created, insert them
    splice(@$conf, $acl->{'line'}, 1, @newlines);
  }

  # Flush File
  &flush_file_lines();
  &sgchown($config{'conf'});

  &redirect("edit_aclitem.cgi?aclindex=$in{'aclindex'}");

} # end else delete


### END of save_sourcedomain.cgi ###.
