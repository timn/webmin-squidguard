#! /usr/bin/perl

# perl-metrics.pl
# version 0.02

# Copyright (C) 2000 Hal J Eisen (eisen@dunhackin.org)

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# this program is intended to help perl programmers write better code
# by becoming more aware of their coding style.  in particular, one
# would like to know the code:comment ratio, the average number of
# lines per subroutine, the longest subroutine, and things like that.

use Getopt::Std;

# constants

$non_subroutine_warning_threshold    = 50;
$subroutine_length_warning_threshold = 65;
$code_to_comment_threshold           = 4;

##########################################################################

sub usage {
    print "perl-metrics.pl [-s] file [file file ...]\n";
    print "  provides metrics about the list of files provided\n";
    print "  use -s to get a list of subroutines sorted by linecount\n";
}

##########################################################################

# gets rid of the contents of single- and double-quoted strings so that
# they don't throw off the count of comments etc

sub remove_strings {
    my $line = shift;

    $line =~ s/".*?"/""/g;
    $line =~ s/'.*?'/''/g;

    return $line;
}

##########################################################################

# keeps an array of all the subroutines and their linecount, but in a
# good format for sorting later

sub register_subroutine {
    my $name = shift;
    my $count = shift;

    if (!defined($opt_s)) {
	return;
    }

    push @subroutines, "$count:$name";
}

##########################################################################

# initialize the various counters used in a run against a particular
# file.  be sure to get them all, or else when running against
# multiple files the counts will be cumulative, which we don't want.

sub init {
    undef %count;
    undef @subroutines;
    $longest_subroutine = undef;
    $max_subroutine_linecount = 0;
    $line_number = 0;
    $subroutine_begins_at = -1;
    $count{subroutines} = 0;
}

##########################################################################

# if we are currently NOT inside a subroutine, increase the count of
# nonsubroutine lines

sub possibly_bump_non_subroutine_lines {
    if ($subroutine_begins_at == -1) {
	$count{non_subroutine_lines}++;
    }
}

##########################################################################

# detect subroutine boundary lines

sub count_subroutine_things {
    my $line = shift;

    # count subroutine lines
    # these regexes are naive, but seem sufficient
    if ($line =~ /^sub\s+(\w+)\s*{.*}/) {
	# one line subroutine
	$count{non_subroutine_lines}++;
	&register_subroutine($1, 1);
	# print "-> $line\n";
    }
    elsif ($line =~ /^sub\s+(\w+)\s*\{?/) {
	# begining of a multiline subroutine
	$this_subroutine_name = $1;
	$subroutine_begins_at = $line_number;
    }
    elsif ($line =~ /^\}/ and $subroutine_begins_at != -1) {
	# end of a multiline subroutine
	$this_subroutine_linecount = $line_number - $subroutine_begins_at - 1;

	$count{subroutine_lines} += $this_subroutine_linecount;
	if ($this_subroutine_linecount > $max_subroutine_linecount) {
	    $max_subroutine_linecount = $this_subroutine_linecount;
	    $longest_subroutine = $this_subroutine_name;
	}

	$subroutine_begins_at = -1;

	&register_subroutine($this_subroutine_name, $this_subroutine_linecount);
    }
    else {
	# not a subroutine boundary line
    }
}

##########################################################################

# this is the heart and soul of the program.

sub count_things {
    open(FILE, "<$file") || die "cannot open $file\n: $!";

    while ($line = <FILE>) {
	chomp $line;
	$line_number++;

	$line = &remove_strings($line);

	last if ($line =~ /^__END__$/);

	# count all lines
	$count{total_lines}++;

	# count number of blank lines
	if ($line =~ /^\s*$/) {
	    $count{blank_lines}++;
	}

	# count number of comment lines
	elsif ($line =~ /^\s*\#/) {
	    $count{comment_lines}++;
	}

	# count number of subroutines
	elsif ($line =~ /^\s*sub\b/) {
	    # start of subroutine declaration
	    $count{subroutines}++;
	}

	# count pure code lines
	elsif ($line =~ /^[^\#]+$/) {
	    $count{pure_code}++;
	    &possibly_bump_non_subroutine_lines();
	}

	# count code + comment lines
	else {
	    # BUG: regexes with `#' (pound signs) in them get counted here
	    $count{code_with_comment}++;
	    &possibly_bump_non_subroutine_lines();
	}

	&count_subroutine_things($line);
    }
}

##########################################################################

sub numerically_desc { $b <=> $a }

##########################################################################

sub print_stats {
    my $file = shift;

    print "\n===> $file <===\n\n";

    # loop over the various counts and show each one
    foreach $key (keys %count) {
	printf("%-30s %4d\n", $key, $count{$key});
    }

    # warning for files with lots of non-subroutine code
    if (($count{non_subroutine_lines}) > $non_subroutine_warning_threshold) {
	printf("DANGER -->  %d non-subroutine lines\n", $count{non_subroutine_lines});
    }

    # code-to-comment ratio
    if ($count{comment_lines} == 0) {
	print "DANGER --> No comments\n";
    }
    else {
	$code_to_comment_ratio = ($count{non_subroutine_lines} + $count{subroutine_lines}) / $count{comment_lines};
	printf("%-30s %4.1f%s\n", "code-to-comment ratio", $code_to_comment_ratio, ($code_to_comment_ratio > $code_to_comment_threshold) ? " (DANGER)" : "");
    }

    # special subroutine stat: avg lines per subroutine
    if ($count{subroutines} > 0) {
	printf("%-30s %4.1f\n", "avg lines per subroutine", $count{subroutine_lines} / $count{subroutines});
    }

    # gripe about the largest subroutine
    if (defined($longest_subroutine)) {
	if ($max_subroutine_linecount > $subroutine_length_warning_threshold) {
	    print "DANGER -->  longest subroutine: $longest_subroutine ($max_subroutine_linecount lines)\n";
	}
	else {
	    print "longest subroutine: $longest_subroutine ($max_subroutine_linecount lines)\n";
	}
    }

    # (optionally) show subroutine list sorted by linecount
    if (defined($opt_s)) {
	foreach $item (sort numerically_desc @subroutines) {
	    ($count, $name) = split(/:/, $item);
	    printf("\t%-40s %4d\n", $name, $count);
	}
    }

    print "\n";
}

##########################################################################

# the main program harness

getopts('s');

if (scalar(@ARGV) == 0) {
    &usage();
    exit 0;
}

while (scalar(@ARGV) > 0) {
    $file = shift;

    &init();
    &count_things($file);
    &print_stats($file);
}

exit 0;

