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

#    Created  : 02.06.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'eacl'}) {
  &terror('eai_acl');
}

@config = &parse_config();

my $sec=&find_section( 'sectype' => "acl",
                       'config'  => \@config );

my $acl=$sec->{'members'}->[$in{'aclindex'}] if (! $in{'new'});

&terror('eai_err_notfound', $in{'aclindex'}) if (! defined($sec));


&header($in{'new'} ? $text{'eai_titleadd'} : $text{'eai_title'}, undef, undef, undef, undef, undef,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<HR><BR>";

print "<FORM ACTION=\"save_aclitem.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=aclindex VALUE=\"$in{'aclindex'}\">",
      ($in{'new'}) ? "<INPUT TYPE=hidden NAME=new VALUE=\"1\">" : "",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      $in{'new'} ? $text{'eai_headeradd'} : $text{'eai_header'},
      "</B></TD>\n",
      " </TR>\n",

      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=2>\n",

      "    <TR>\n",
      "     <TD WIDTH=22% VALIGN=top>\n",
      "      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH=100%>\n",
      "       <TR>\n",
      "        <TD><B>$text{'eai_source'}</B></TD>\n";

if ($acl->{'source'} eq 'default') {
  print "<TD>$text{'eai_srcna'}",
        "<INPUT TYPE=hidden NAME=source VALUE=default>",
        "</TD>\n";
} else {
  print "        <TD><SELECT NAME=source>";

  foreach $c (@config) {

    if ($c->{'sectype'} eq 'source') {
      print "<OPTION VALUE=\"$c->{'secname'}\"",
            ($acl->{'source'} eq $c->{'secname'}) ? " SELECTED" : "",
            ">$c->{'secname'}\n";
    }
  }

  print "         </SELECT>\n",
        "        </TD>\n";
}
print "       </TR>\n",
      "       <TR>\n",
      "        <TD><B>$text{'eai_tstype'}</B></TD>\n",
      "        <TD><SELECT NAME=tstype>\n",
      "<OPTION VALUE=none",
      ($acl->{'tstype'} eq 'none') ? " SELECTED" : "",
      ">$text{'eai_tsmnone'}\n",
      "<OPTION VALUE=within",
      ($acl->{'tstype'} eq 'within') ? " SELECTED" : "",
      ">$text{'eai_within'}\n",
      "<OPTION VALUE=outside",
      ($acl->{'tstype'} eq 'outside') ? " SELECTED" : "",
      ">$text{'eai_outside'}\n",
      "         </SELECT>\n",
      "        </TD>\n",
      "       </TR>\n",

      "       <TR>\n",
      "        <TD><B>$text{'eai_timespace'}</B></TD>\n",
      "        <TD><SELECT NAME=timespace>";

foreach $c (@config) {

  if ($c->{'sectype'} eq 'time') {
    print "<OPTION VALUE=\"$c->{'secname'}\"",
          ($acl->{'timespace'} eq $c->{'secname'}) ? " SELECTED" : "",
          ">$c->{'secname'}\n";
  }
}

print "         </SELECT>\n",
      "        </TD>\n",
      "       </TR>\n",

      "      </TABLE>\n",
      "     </TD>\n",
      "     <TD WIDTH=4%> &nbsp; &nbsp; </TD>\n",
      "     <TD WIDTH=22% VALIGN=top>\n",
      "      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH=100%>\n",

      "       <TR>\n",
      "        <TD VALIGN=top><B>$text{'eai_dest'}</B></TD>\n",
      "        <TD><SELECT NAME=pass MULTIPLE SIZE=6>",
      "<OPTION VALUE=\"in-addr\"",
      (&indexof('in-addr', @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
      ">$text{'eai_in-addr'}\n",

      "<OPTION VALUE=\"!in-addr\"",
      (&indexof('!in-addr', @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
      ">! $text{'eai_in-addr'}\n";

foreach $c (@config) {

  if (($c->{'sectype'} eq 'dest') && ($c->{'secname'} !~ /^bl_/)) {
    print "<OPTION VALUE=\"$c->{'secname'}\"",
          (&indexof($c->{'secname'}, @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
          ">$c->{'secname'}\n",

          "<OPTION VALUE=\"!$c->{'secname'}\"",
          (&indexof("!$c->{'secname'}", @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
          ">! $c->{'secname'}\n";
  }
}

print "<OPTION VALUE=\"any\"",
      (&indexof('any', @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
      ">$text{'eai_any'}\n",

      "<OPTION VALUE=\"none\"",
      (&indexof('none', @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
      ">$text{'eai_none'}\n";


print "         </SELECT>\n",
      "        </TD>\n",
      "       </TR>\n",

      "      </TABLE>\n",
      "     </TD>\n",

      "     <TD WIDTH=4%> &nbsp; &nbsp; </TD>\n",
      "     <TD WIDTH=22% VALIGN=top>\n",
      "      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH=100%>\n",

      "       <TR>\n",
      "        <TD VALIGN=top><B>$text{'eai_rew'}</B></TD>\n",
      "        <TD><SELECT NAME=rewrite MULTIPLE SIZE=6>";

foreach $c (@config) {
  if ($c->{'sectype'} eq 'rewrite') {
    print "<OPTION VALUE=\"$c->{'secname'}\"",
          (&indexof($c->{'secname'}, @{$acl->{'rewrite'}}) >= 0) ? " SELECTED" : "",
          ">$c->{'secname'}\n";
  }
}

print "         </SELECT>\n",
      "        </TD>\n",
      "       </TR>\n",

      "      </TABLE>\n",
      "     </TD>\n",

# Blacklists
      "     <TD WIDTH=4%> &nbsp; &nbsp; </TD>\n",
      "     <TD WIDTH=22% VALIGN=top>\n",
      "      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH=100%>\n",

      "       <TR>\n",
      "        <TD VALIGN=top><B>$text{'eai_bl'}</B></TD>\n",
      "        <TD><SELECT NAME=blacklists MULTIPLE SIZE=6>";

foreach $c (@config) {
  if (($c->{'sectype'} eq 'dest') && ($c->{'secname'} =~ /^bl_(.+)$/)) {
    my $bl=$1;
    print "<OPTION VALUE=\"!$c->{'secname'}\"",
          (&indexof("!$c->{'secname'}", @{$acl->{'pass'}}) >= 0) ? " SELECTED" : "",
          ">$bl\n";
  }
}

print "         </SELECT>\n",
      "        </TD>\n",
      "       </TR>\n",

      "      </TABLE>\n",
      "     </TD>\n",


      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0>\n",
      "    <TR>\n",
      "     <TD><B>$text{'eai_redirect'}</B></TD>\n",
      "        <TD><SELECT NAME=redmode>\n",
      "<OPTION VALUE=\"\">$text{'eai_default'}\n",
      "<OPTION VALUE=301",
      ($acl->{'redmode'} eq '301') ? " SELECTED" : "",
      ">$text{'eai_movedtemp'}\n",
      "<OPTION VALUE=302",
      ($acl->{'redmode'} eq '302') ? " SELECTED" : "",
      ">$text{'eai_movedperm'}\n",
      "         </SELECT>\n",
      "        </TD>\n",
      "     <TD><INPUT TYPE=text NAME=redurl SIZE=60 VALUE=\"$acl->{'redurl'}\"></TD>\n",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\">\n",
      $in{'new'} ? "" : "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"$text{'delete'}\">\n",
      "</FORM><HR>";

&footer("list_acls.cgi", $text{'eai_return'});

### END of edit_aclitem.cgi ###.
