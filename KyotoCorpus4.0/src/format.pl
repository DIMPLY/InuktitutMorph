#!/usr/bin/perl

use encoding 'euc-jp';
use open IO => ':encoding(euc-jp)';
binmode(STDERR, ':encoding(euc-jp)');

# コーパスのタイプ
# Type of corpus
$TYPE = "形態素・構文コーパス"; # Morpheme / syntax corpus
# $TYPE = "文脈コーパス"; # Context corpus

#
# 対象外とする記事，文
# Articles excluded, articles, sentences
#
$neglect_aid{"950101140"} = 1;	# 選手紹介 # Players introduction
$neglect_aid{"950110251"} = 1;	# 各地の地震強度 # Earthquake intensity in each area
$neglect_aid{"950112293"} = 1;	# 出品者一覧 # Seller list
$neglect_aid{"950118034"} = 1;	# 人名一覧 # Person name list
$neglect_aid{"950118035"} = 1;	# 人名一覧
$neglect_aid{"950118045"} = 1;	# 人名一覧
$neglect_aid{"950118046"} = 1;	# 人名一覧
$neglect_aid{"950118240"} = 1;	# 人名一覧
$neglect_aid{"950118241"} = 1;	# 人名一覧
$neglect_aid{"950118243"} = 1;	# 人名一覧
$neglect_aid{"950118244"} = 1;	# 人名一覧
$neglect_aid{"950118245"} = 1;	# 人名一覧
$neglect_aid{"950118250"} = 1;	# 人名一覧
$neglect_aid{"950118252"} = 1;	# 人名一覧
$neglect_aid{"950118253"} = 1;	# 人名一覧
$neglect_aid{"950118254"} = 1;	# 人名一覧

my ($dirname) = ($0 =~ /^(.*?)[^\/]+$/);
$GIVEUP = $dirname ? "${dirname}giveup.dat" : "giveup.dat";
$OK = $dirname ? "${dirname}ok.dat" : "ok.dat";

@enu = ("０", "１", "２", "３", "４", "５", "６", "７", "８", "９");
$start_flag = 0;

# 引数の処理
# Processing arguments

$DATE = "";
for ($i = 0; ; $i++) {
    if ($ARGV[$i] =~ /^\-/) {
	if ($ARGV[$i] eq "-all") {
	    $SUBJECT = "全記事";  # All articles
	} elsif ($ARGV[$i] eq "-ed") {
	    $SUBJECT = "社説";  # editorial
	} elsif ($ARGV[$i] eq "-exed") {
	    $SUBJECT = "社説以外";  # Other than editorials
	}
    } else {
	$DATE = $ARGV[$i];
	last;
    }
}
die if (!$DATE || $DATE !~ /^95/); 

######################################################################
#		  毎日新聞CD-ROMデータのフォーマット
#             Mainichi Newspaper CD-ROM data format
######################################################################

#
# giveup.dat があれば読み込み，削除する．
# giveup.dat   If there is, read and delete it.
#

if (open(GIVEUP, $GIVEUP)) {
    while ( <GIVEUP> ) {
	if (/^([\d-]+)/) {
	    $neglect_h_sid{$1} = 1;
	}
    }
    close(GIVEUP);
}

#
# ok.dat があれば読み込み，削除する．
# ok.dat  If there is, read and delete it.
#

if (open(OK, $OK)) {
    while ( <OK> ) {
	if (/^(?:\# S-ID:)?([\d-]+)(.*)/) {
	    my ($id, $str) = ($1, $2);
	    $ok_h_sid{$id} = 1;
	    while ($str =~ / 部分削除:(\d+):([^ ]+)/g) {  # Delete part
		$ok_h_check{$id}{$1} = $2;
	    }
	}
    }
    close(OK);
}

while ( <STDIN> ) {

    $whole_article .= $_;

    if (/<\/ENTRY>/) {
	if ($start_flag) {
	    &check_article($aid, $title, $article);
	    # 記事に区切るだけ
	    # Just separate articles
	    
	    # print "$aid\n$title\n$article\n\n";
	    # print $whole_article;
	}
	$article = "";
	$whole_article = "";
    } elsif (/<C0>/) {
	/^<C0>(.+)<\/C0>\n/;
	$aid = $1;
	if ($aid =~ /^$DATE/) {
	    $start_flag = 1;
	} else {
	    if ($start_flag) {
		exit;
	    } else {
		;
	    }
	}
    } elsif (/<T1>/) {
	/^<T1>(.+)<\/T1>\n/;
	$title = $1;
    } elsif (/<T2>/) {
	$flag = 1;
    } elsif (/<\/T2>/) {
	$flag = 0;
    } else {
	$article .= $_ if ($start_flag && $flag);
    }
}

######################################################################
# コーパス作成から排除する記事
#
# ・タイトルに次の文字列があるもの
#	［余録］
#	［雑記帳］
#	［社告］
#	［人事］
#	［人物略歴］
#	死去＝
#
# ・本文中に(段落先頭を除いて)スペースを含むもの
#   (スペースの2つ連続を除けば表などはほとんど省けるが，とりあえず簡単の
#    ためスペースが一つでも入れば排除する)
#
# ・段落先頭に"　――"があるもの
#   (インタビュー記事，発言者名，発言全体が括弧に囲まれる可能性などがある
#    ため)
#

# Articles to exclude from corpus creation
#
# · The following character string is in the title
# 	[Overhead]
#	[notebook]
# 	[Company notice]
#	[human resources]
# 	[People Biography]
# 	Death =
#
# · Containing spaces (except paragraph head) in the text
# (Although it is possible to omit tables etc. except for two consecutive spaces, for the time being simple
# Because it eliminates if even one space is excluded)
#
# · With "-" at beginning of paragraph
# (There is a possibility that the interview article, the name of the speaker, the entire remark is enclosed in parentheses
# For)

######################################################################

sub check_article
{
    local($aid, $title, $artice) = @_;
    local($i, $flag);

    $flag = 1;

    if ($neglect_aid{$aid}) {
	$flag = 0;
    }
    elsif ($title =~ 
	/［余録］|［雑記帳］|［社告］|［人事］|［人物略歴］|死去＝|＝の葬儀・告別式/) {  # ...... =|= funeral ceremony of death
	$flag = 0;
    }
    elsif (($SUBJECT eq "社説" && $title !~ /［社説］/) || 
	   ($SUBJECT eq "社説以外" && $title =~ /［社説］/)) {
	$flag = 0;
    }
    else {
	foreach $i (split(/\n/, $article)) {
	    $flag = 0 if ($i =~ /　――/);
	    $i =~ s/^　//;
	    $flag = 0 if ($i =~ /　/);
	}
    }

    if ($flag == 0) {
	if ($TYPE eq "形態素・構文コーパス") {
	    print STDOUT "# A-ID:$aid 削除\n";
	}
    }
    else {
	if ($TYPE eq "形態素・構文コーパス") {
	    print STDOUT "# A-ID:$aid\n";
	    &breakdown_article($aid, $article, STDOUT);
	}
	elsif ($TYPE eq "文脈コーパス") {  # Context corpus
	    $aid =~ /....(.....)/;
	    open(OUT, "> $1.txt");
	    &breakdown_article($aid, $article, OUT);
	    close(OUT);
	}
    }
}

######################################################################
# 記事を文単位に分解
#
# ・括弧内以外の"。"
#
# ・"】"

# Disassemble articles by sentence
#
# · "." Other than in parentheses
#
# ・"】"
######################################################################

sub breakdown_article
{
    local($aid, $article, $OUT) = @_;
    local($paragraph, $sentence, $level, $last, $scount, $sid, $pcount);
    local($i, @char);

    chop($article);
    $scount = 1;
    $pcount = 1;
    foreach $paragraph (split(/\n/, $article)) {

	if ($TYPE eq "文脈コーパス") {
	    print $OUT "# ($pcount)\n";
	}

	$level = 0;
	$sentence = "";
	
	@char = split(//, $paragraph);

	for ($i = 0; $i < @char; $i++) {
	    if ($char[$i] eq "「" ||
		$char[$i] eq "＜" ||
		$char[$i] eq "（") {
		$level ++;
		# print STDERR "nesting 括弧:$sentence\n" if ($level == 2);
	    } elsif ($char[$i] eq "」" ||
		     $char[$i] eq "＞" ||
		     $char[$i] eq "）") {
		$level --;
		# print STDERR "invalid 括弧？:$paragraph\n" if ($level == -1);
	    }
	    $sentence .= $char[$i];
	    if (($level == 0 && $char[$i] eq "。" ) || 
		($char[$i] eq "】" && $char[$i+1] ne "。")) {
		$sid = sprintf("%s-%03d", $aid, $scount);

		if ($TYPE eq "形態素・構文コーパス") {
		    &check_sentence($sid, $sentence, $OUT);
		}
		elsif ($TYPE eq "文脈コーパス") {
		    $sentence =~ s/^　+//;
		    print $OUT "# $scount\n$sentence\n";
		}
		$scount++;
		$sentence = "";
	    }
	    $last = $char[$i];
	}

	if ($last ne "。" && $last ne "】") {
	    $sid = sprintf("%s-%03d", $aid, $scount);
	    
	    if ($TYPE eq "形態素・構文コーパス") {
		&check_sentence($sid, $sentence, $OUT);
	    }
	    elsif ($TYPE eq "文脈コーパス") {
		$sentence =~ s/^　+//;
		print $OUT "# $scount\n$sentence\n";
	    }
	    $scount++;
	    $sentence = "";
	}

	if ($TYPE eq "形態素・構文コーパス") {
	    print $OUT "# 改段落\n";  # Change paragraph
	}
	$pcount++;
    }
}

######################################################################
# 文，文内で削除するもの
#
# ・"【"，"◇"，"▽"，"●"，"＜"，"《"で始まる文は全体を削除
#
# ・"。"が内部に5回以上または長さ512バイト以上(多くは引用文)は全体を削除
#
# ・文頭の"　"，"　――";
#
# ・"（…）"の削除，ただし，"（１）"，"（２）"の場合は残す
#
# ・"＝…＝"の削除，ただし間に"，"がくればRESET
#
# ・"＝…(文末)"で，文末に"。"がないか，"…"が"写真。"であれば除削
#
# ・（１）…（２） という箇条書きがあるもの

# Statements, things to delete in statements
#
# · Statements beginning with "[", "◇", "▽", "●", "<", "<<"delete the whole
#
#. "." Inside it more than 5 times or longer 512 bytes or more (many quotes) delete the whole
#
# · At the beginning of the sentence "", "-";
#
# · Delete "(...)", except for "(1)", "(2)"
#
# · Deleting "= ... =", but if "," comes between, RESET
#
# · "= ... (end of sentence)", if there is no "." At the end of the sentence or "..." is "photo", remove it
#
# · With (1) ... (2) bullet point
######################################################################

sub check_sentence
{
    local($sid, $sentence, $OUT) = @_;
    local(@char_array, @check_array, $i, $flag);
    local($enu_num, $paren_start, $paren_level, $paren_str);

    (@char_array) = split(//, $sentence);

    for ($i = 0; $i < @char_array; $i++) {
	$check_array[$i] = 1;
    }

    # 人手削除
    if ($ok_h_sid{$sid}) {
	for my $pos (keys %{$ok_h_check{$sid}}) {
	    for (my $i = $pos; $i < $pos + length($ok_h_check{$sid}{$pos}); $i++) {
		$check_array[$i] = 0;
	    }
	}
	goto SENTENCE_CHECK_OK;
    }

    # 特別に対象外とする文
    # A statement to be excluded specially

    if ($neglect_sid{$sid}) {
	print $OUT "# S-ID:$sid 全体削除:$sentence\n";
	return;
    }
    if ($neglect_h_sid{$sid}) {
	print $OUT "# S-ID:$sid 人手削除:$sentence\n";
	return;
    }

    # "【"，"◇"，"▽"，"●"，"＜"，"《"で始まる文は全体を削除
    # Statements beginning with "[", "◇", "▽", "●", "<", "<<" delete the whole

    if ($sentence =~ /^(　)?(【|◇|▽|●|＜|《)/) {
	print $OUT "# S-ID:$sid 全体削除:$sentence\n";
	return;
    }

    # "。"が内部に5回以上または長さ512バイト以上(多くは引用文)は全体を削除
    # "." Inside more than 5 times or more than 512 bytes long (many quotes) delete the whole

    if ($sentence =~ /^.+。.+。.+。.+。.+。.+/ ||
	length($sentence) >= 256) {
	print $OUT "# S-ID:$sid 全体削除:$sentence\n";
	return;
    }

    # "………"だけの文は全体を削除
    # Delete the whole sentence "........." only
    
    if ($sentence =~ /^(…)+$/) {
	print $OUT "# S-ID:$sid 全体削除:$sentence\n";
	return;
    }

  SENTENCE_OK:
    # 文頭の"　"は削除
    # Delete "" at the beginning of the sentence
    $check_array[0] = 0 if ($char_array[0] eq "　");

    # 文頭の"　――"は削除
    # Delete "-" at beginning of sentence

    if ($sentence =~ "^　――") {
	$check_array[1] = 0;
	$check_array[2] = 0;
    }

    # "（…）"の削除，ただし，"（１）"，"（２）"の場合は残す
    # Delete "(...)", but leave it if "(1)", "(2)"

    $enu_num = 1;
    $paren_start = -1;
    $paren_level = 0;
    $paren_str = "";
    for ($i = 0; $i < @char_array; $i++) {
	if ($char_array[$i] eq "（") {
	    $paren_start = $i if ($paren_level == 0);
	    $paren_level++;
	} 
	elsif ($char_array[$i] eq "）") {
	    $paren_level--;
	    if ($paren_level == 0) {
		if ($paren_str eq $enu[$enu_num]) {
		    $enu_num++;
		}
		else {
		    for ($j = $paren_start; $j <= $i; $j++) {
			$check_array[$j] = 0;
		    }
		}
	    $paren_start = -1;
	    $paren_str = "";
	    }
	}
	else {
	    $paren_str .= $char_array[$i] if ($paren_level != 0);
	}
    }
    # print STDERR "enu_num(+1) = $enu_num\n" if ($enu_num > 1);

    # "＝…＝"の削除，ただし間に"，"がくればRESET
    # Delete "= ... =", but if "," comes between, RESET

    $paren_start = -1;
    $paren_level = 0;
    $paren_str = "";
    for ($i = 0; $i < @char_array; $i++) {
	if ($check_array[$j] == 0) {
	    ; # "（…）"の中はスキップ
	      # Skip inside "(...)"
	} elsif ($char_array[$i] eq "＝") {
	    if ($paren_level == 0) {
		$paren_start = $i; 
		$paren_level++;
	    } 
	    elsif ($paren_level == 1) {
		for ($j = $paren_start; $j <= $i; $j++) {
		    $check_array[$j] = 0;
		}
		$paren_start = -1;
		$paren_level = 0;
		$paren_str = "";
	    }
	}
	elsif ($char_array[$i] eq "、") {
	    if ($paren_level == 1) {

		# "＝…"となっていても，"、"がくればRESET
		# 例 "「中高年の星」＝米長と、若き天才＝羽生"
		
		# "= ...", but if "," comes, RESET
		# Example "「中高年の星」＝米長と、若き天才＝羽生"
		
		# print STDERR "＝…，…＝RESET:$paren_str:$sentence\n";

		$paren_start = -1;
		$paren_level = 0;
		$paren_str = "";
	    }
	}
	else {
	    $paren_str .= $char_array[$i] if ($paren_level == 1);
	}
    }

    # "＝…(文末)"で，文末に"。"がないか，"…"が"写真。"であれば除削
    # "= ... (end of sentence)", if there is no "." At the end of the sentence or "..." is "photo", remove it

    if ($paren_level == 1) {
	if ($paren_str =~ /^写真/ || $paren_str !~ /。$/) {
	    for ($j = $paren_start; $j < $i; $j++) {
		$check_array[$j] = 0;
	    }
	    # print STDERR "＝…DELETE:$paren_str:$sentence\n";
	} else {
	    # print STDERR "＝…KEEP:$paren_str:$sentence\n";
	}
    }

  SENTENCE_CHECK_OK:
    $flag = 0;
    for ($i = 0; $i < @char_array; $i++) {	
	if ($check_array[$i] == 1) {
	    $flag = 1;
	    last;
	}			# 有効部分がなければ全体削除
	                        # If there is no valid part, delete whole
    }
    if ($enu_num > 2 && !$ok_h_sid{$sid}) {	# （１）（２）とあれば全体削除
    						# If (1) (2) is present, the whole is deleted
	# print STDERR "# S-ID:$sid 全体削除:$sentence\n";
	$flag = 0;
    }

    if ($flag == 0) {
	print $OUT "# S-ID:$sid 全体削除:$sentence\n";
    } else {
	print $OUT "# S-ID:$sid";

	for ($i = 0; $i < @char_array; $i++) {
	    if ($check_array[$i] == 0) {
		print $OUT " 部分削除:$i:" 
		    if ($i == 0 || $check_array[$i-1] == 1);
		print $OUT $char_array[$i];
	    }
	}
	print $OUT "\n";

	for ($i = 0; $i < @char_array; $i++) {
	    print $OUT $char_array[$i] if ($check_array[$i] == 1);
	}
	print $OUT "\n";
    }
}

######################################################################
#				 END
######################################################################
