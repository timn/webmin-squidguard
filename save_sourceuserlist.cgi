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

#    Created  : 18.10.2001


require "./squidguard-lib.pl";

&error_setup($text{'ssul_error'});
# ACL Check
&terror('ssul_acl') if (! $access{'esource'});


# We ned the section on both, save and delete
@config = &parse_config();
# Find Section
my $sec=&find_section( 'sectype' => "source",
                       'secname' => $in{'sourcegroup'},
                       'config'  => \@config );
&terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sec));
my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


# Get dbhome for possible need when saving/deleting the userlist
my $dbsec=&find_section( 'config' => \@config,
                         'sectype' => 'dbhome' );
my $dbhome=$dbsec->{'dbhome'};



if (defined($in{'delete'})) {

  if ($st->{'userlist'} =~ /^\//) {
    system("rm -f $st->{'userlist'}") if (-e $st->{'userlist'});
  } else {
    system("rm -f $dbhome/users/$st->{'userlist'}") if (-e "$dbhome/users/$st->{'userlist'}");
  }
  &redirect("del_statement.cgi?sectype=source&secname=$in{'sourcegroup'}&index=$in{'index'}&back=sourcegroup");

} else {

  if ($in{'new'}) {
    # Create a new line
    my $newline = "userlist\t\tusers/$in{'userlist'}";

    # Save the new line replacing the old one
    my $conf = &read_file_lines($config{'conf'});

    # Adding a new statement
    my @newlines=($conf->[$sec->{'line'}],
                "\t$newline" );
    splice(@$conf, $sec->{'line'}, 1, @newlines);
    mkdir("$dbhome/users") if (! -d "$dbhome/users");
    system("touch $dbhome/users/$in{'userlist'}");

    if ($config{'userlistsql'} && $in{'field'}) {
      my $select = $config{'userlistsql'};
         $select =~ s/\@FIELD\@/$in{'field'}/ig;
      my $dbget = &db_get($select) if ($config{'userdb'});

      my $userfile = &read_file_lines("$dbhome/users/$in{'userlist'}");
      foreach my $v (@{$dbget}) {
        push(@$userfile, $v->[0]);
      }
    }

    &flush_file_lines();
    &sgchown("$dbhome/users/$in{'userlist'}");
  } else {
    # Modifying the users :-)
    $in{'users'} =~ s/\r//g;
    if ($st->{'userlist'} =~ /^\//) {
      open(USERLIST, ">$st->{'userlist'}");
    } else {
      open(USERLIST, ">$dbhome/$st->{'userlist'}");
    }
    print USERLIST $in{'users'};
    close(USERLIST);
  }

  if ($in{'new'}) {
    &redirect("edit_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}");
  } else {
    &redirect("edit_sourceuserlist.cgi?sourcegroup=$in{'sourcegroup'}&index=$in{'index'}");
  }
}

### END of save_sourceuserlist.cgi ###.
