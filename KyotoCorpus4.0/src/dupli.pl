#!/usr/bin/perl

use encoding 'euc-jp';

# 毎日新聞で一日の記事の中で重複している文を削除
# Delete duplicate sentences in the article of the day in the Mainichi Newspaper

while ( <STDIN> ) {

    if (/^\# S-ID:([\d\-]+) (全体削除|人手削除):(.+\n)$/) {  # Delete whole / manually deleted
	$id = $1;
	$sentence = $3;
	$check{$sentence} = $id;

	print;
    }
    elsif (/^\# S-ID:([\d\-]+)[\n ]/ && !/(全体削除|人手削除)/) {  # Delete whole / manually deleted
	$id = $1;
	$all_id = $_;
	$sentence = <STDIN>;

	if ($check{$sentence}) {

	    # 重複していれば，文はID行に出力する
	    # If there is duplication, the statement is outputted to the ID row

	    chop($all_id);
	    print "$all_id 重複:$check{$sentence}$sentence";
	}
	else {

	    # 重複していなければ通常出力，テーブル追加
	    # If it does not overlap, normal output, add table

	    print $all_id;
	    print $sentence;
	    $check{$sentence} = $id;
	}
    }
    else {
	print;
    }
}
