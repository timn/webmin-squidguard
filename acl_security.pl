
#    SquidGuard Configuration Webmin Module
#    Copyright (C) 2001 by Tim Niemueller <tim@niemueller.de>
#    Website: http://www.niemueller.de/webmin/modules/squidguard/
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

#    Created  : 05.06.2001


require "./squidguard-lib.pl";

# acl_security_form(&options)
# Output HTML for editing security options for the apache module
sub acl_security_form
{

print "<TR><TD>$text{'acl_epaths'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"epaths\" VALUE=\"1\"",
      ($_[0]->{'epaths'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"epaths\" VALUE=\"0\"",
      ($_[0]->{'epaths'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n",
      
      "<TR><TD>$text{'acl_esource'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"esource\" VALUE=\"1\"",
      ($_[0]->{'esource'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"cesource\" VALUE=\"0\"",
      ($_[0]->{'esource'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n",

      "<TR><TD>$text{'acl_edest'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"edest\" VALUE=\"1\"",
      ($_[0]->{'edest'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"edest\" VALUE=\"0\"",
      ($_[0]->{'edest'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n",

      "<TR><TD>$text{'acl_etimespace'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"etimespace\" VALUE=\"1\"",
      ($_[0]->{'etimespace'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"etimespace\" VALUE=\"0\"",
      ($_[0]->{'etimespace'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n",

      "<TR><TD>$text{'acl_erewrite'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"erewrite\" VALUE=\"1\"",
      ($_[0]->{'erewrite'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"erewrite\" VALUE=\"0\"",
      ($_[0]->{'erewrite'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n",

      "<TR><TD>$text{'acl_eacl'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"eacl\" VALUE=\"1\"",
      ($_[0]->{'eacl'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"eacl\" VALUE=\"0\"",
      ($_[0]->{'eacl'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n",

      "<TR><TD>$text{'acl_eblacklist'}</TD>",
      "<TD><INPUT TYPE=radio NAME=\"eblacklist\" VALUE=\"1\"",
      ($_[0]->{'eblacklist'}) ? " CHECKED" : "", "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=\"eblacklist\" VALUE=\"0\"",
      ($_[0]->{'eblacklist'}) ? "" : " CHECKED", "> $text{'no'}</TD><TR>\n";

}

# acl_security_save(&options)
# Parse the form for security options for the apache module
sub acl_security_save
{

$_[0]->{'esource'} = $in{'esource'};
$_[0]->{'epaths'} = $in{'epaths'};
$_[0]->{'edest'} = $in{'edest'};
$_[0]->{'etimespace'} = $in{'etimespace'};
$_[0]->{'erewrite'} = $in{'erewrite'};
$_[0]->{'eacl'} = $in{'eacl'};

}

### END.