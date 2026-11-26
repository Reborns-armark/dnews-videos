"""Long-form (16:9, ~8+ min) episode: the deepest explosive (pyroclastic) volcanic deposits ever found, >6,000 m down the Mariana Trench wall.
News: Stern RJ, Pujana I, Anderson MK, Chin EJ, Dygert N, Harigane Y, Le Roux V, Leybourne M, Ohara Y, Okumura T, Segee-Wright G, Etheridge E (2026)
'ROVing in the deep: tectonic and magmatic complexities of the Challenger Deep forearc segment, Southern Mariana convergent margin',
Front. Earth Sci. 14:1929806, doi:10.3389/feart.2026.1929806 (published 2026-11-23, CC BY). UT Dallas / EurekAlert release; Discover (2026-11-23);
The Brighter Side of News (2026-11-24); Marine Insight (2026-11-24).
Facts used: R/V Thomas G. Thompson cruise TN438, ROV Jason/Medea, late Nov - early Dec 2024, 7 dives along ~300 km of the forearc, limit 6,500 m;
155 rock samples; pyroclastic flow margins at 6,148 m and cooling-fractured slabs at 6,334 m; deepest known pyroclastic deposits; likely driven by
supercritical fluids, less explosive than low-pressure eruptions; supercritical water takes ~3% of the volume of steam (Discover);
vents not yet found; flows didn't travel far; eastern part = old mantle peridotite, western part = younger volcanic rock; magmatism unusually close
to the trench; Challenger Deep 10,935 m; subduction began ~52 Ma; plate convergence ~3 cm/yr. Stern: 'we were very surprised'.
Background: pure water critical point 374 C / ~218 atm; Shinkai Seep Field (found by Shinkai 6500, ~5.7 km); boninite named after the Bonin Islands.
Images: Stern et al. 2026, Frontiers in Earth Science (CC BY 4.0), Figs 1, 7, 8, 11, 12 (cropped)."""
import os, sys
from common4 import *
from hera_vis import *
from trench_vis import *
import engine2 as E2, engine4 as E4
from wide import make_wide, render_wide


def C(say, cap, vis, **kw):
    kw.setdefault("capsize", 96)
    return Cut(say, cap, vis, **kw)


CH = lambda n, t: dict(chapter=f"第{n}章 {t}")
Q1 = ["約3800m", "約8800m", "約1万900m"]
Q2 = ["水が冷たいから", "水蒸気にふくらめないから", "魚がじゃまするから"]

CR = "Stern et al. 2026, Frontiers in Earth Science(CC BY 4.0)"
P_flow = P("flow6148", CR, "6148mの本物の写真!", box=(960, 540))
P_flow2 = P("flow6148", CR, None, box=(960, 540), crop=(150, 60, 600, 340))
P_cool = P("cool6334", CR, "6334mの海の底", box=(860, 650))
P_rock1 = P("rock1", CR, "持ち帰った石", box=(860, 760))
P_rock2 = P("rock2", CR, "火山のかけらがギッシリ", box=(860, 760))
P_seep = P("seep2", CR, "シンカイ・シープ・フィールド", box=(940, 720))
P_seep1 = P("seep1", CR, "白いえんとつ", box=(900, 780))
P_slab = P("slab2", CR, "われた岩の板", box=(900, 690))
P_slab1 = P("slab1", CR, None, box=(940, 620))
P_rockh = P("rock_h", CR, "ゴツゴツの岩", box=(920, 690))
P_map = P("map_cdfs", CR, "しらべた場所", box=(960, 720))
P_mapw = P("map_wide", CR, "日本からマリアナへ", box=(640, 870))
P_fig12 = P("fig12", CR, "ふつうの場所とのちがい", box=(980, 710))
P_fig11 = P("fig11", CR, "深さと火山の記録", box=(780, 860))

CUTS = [
    # ---- opening
    C("深さ、六千メートルの、海の底で、火山が、爆発していた!", "深さ6000mの海の底で\n{火山が爆発}!?", v_hook, chapter="オープニング", mood="wow", word="エエッ!"),
    C("場所は、世界で、いちばん深い、マリアナ海溝。", "世界一深い\n{マリアナ海溝}", v_trench, point=True),
    C("海底ロボットが、海で、いちばん深い場所で、爆発した火山の、あとを、見つけたんです。", "海でいちばん深い\n{爆発のあと}", P_flow, point=True),
    C("でも、ちょっと待って。水の中で、火山って、爆発できるの?", "水の中で\n{爆発できるの}?", v_question, word="ハテ?"),
    C("その答えには、水が、水でも、水蒸気でもなくなる、ふしぎな、すがたが、かかわっていました。", "水でも水蒸気でもない\n{ふしぎなすがた}", v_super),
    C("今日は、本物の、海底の、写真と、いっしょに、深海の、火山の、なぞを、たっぷり、紹介します!", "深海の火山の\n{なぞ}を紹介!", v_volcano_ring),
    C("最後には、日本と、つながる、意外な話も、あるよ!", "日本との\n{意外なつながり}も!", v_japan, teaser=True, mood="wow"),

    # ---- ch1 trench
    C("まずは、舞台の、マリアナ海溝を、見てみましょう。", "マリアナ海溝って\n{どんなところ}?", v_trench, **CH(1, "世界一深い海")),
    C("マリアナ海溝は、日本の、ずっと南、グアム島の、近くに、あります。", "日本の南\n{グアムの近く}", P_mapw, point=True),
    C("長さは、およそ、二千五百キロメートル。海の底に、ほられた、ながーい、みぞです。", "海の底の\n{ながーいみぞ}", v_trench),
    C("その中で、いちばん深い場所が、チャレンジャー海淵。", "いちばん深い場所\n{チャレンジャー海淵}", v_trench, point=True),
    quiz("ここでクイズ!チャレンジャー海淵の、深さは、どれくらいでしょう?", "Q.チャレンジャー海淵の\n{深さ}は?", Q1, 2),
    reveal("正解は、C!およそ、一万九百メートルです!", "正解は{C}!\n{約1万900m}!", Q1, 2),
    C("世界一高い山、エベレストは、八千八百四十九メートル。", "エベレストは\n{8849m}", v_everest, point=True),
    C("エベレストを、しずめても、てっぺんの上に、まだ、二千メートル以上も、水が、あるんです!", "エベレストが\n{すっぽりしずむ}!", v_everest, word="スゴイ!"),
    C("深い海は、まっ暗で、とても、冷たい世界。", "まっ暗で\n{冷たい世界}", v_limit),
    C("そして、なにより、水の重さが、すごいんです。", "水の{重さ}が\nすごい!", v_pressure, point=True),
    C("深さ、六千メートルでは、指先くらいの、広さに、およそ、六百キロの、重さが、かかります。", "指先に\n{約600kg}!", v_pressure, word="オモイ!"),
    C("ここで意外な話。発ぽうスチロールの、カップを、深海に、しずめて、もどすと、ぎゅっと、ちぢんで、小さくなるんです。", "カップが\n{小さくなる}!?", v_cup, point=True, word="エッ!"),
    C("中の、空気が、おし出されて、まるで、ミニチュアの、ように、なるんですね。", "空気がぬけて\n{ミニチュア}に", v_cup),
    C("人が、はじめて、チャレンジャー海淵の、底に、着いたのは、千九百六十年。トリエステ号という、潜水艇でした。", "1960年\n{はじめて人が底へ}", v_dive_deeper, point=True),
    C("それから、六十年以上たった今でも、底まで、行ったことがある人は、ほんの、ひとにぎりです。", "底へ行った人は\n{ほんのひとにぎり}", v_limit),

    # ---- ch2 robot
    C("こんな、深い海を、どうやって、しらべたのでしょう?", "どうやって\n{しらべた}?", v_question, **CH(2, "海底ロボットの大冒険")),
    C("活やくしたのは、アメリカの、無人の、海底ロボット、ジェイソン。", "無人の海底ロボット\n{ジェイソン}", v_jason, point=True),
    C("調査船、トーマス・G・トンプソンから、長い、ケーブルで、つながれて、もぐっていきます。", "調査船から\n{ケーブル}でもぐる", v_ship),
    C("カメラと、ライトで、海の底を、うつし、ロボットの、うでで、石を、拾うことが、できます。", "カメラと{ロボットのうで}", v_jason),
    C("ジェイソンと、つきそい役の、メディア。どちらも、ギリシャ神話の、冒険の物語から、名前が、つけられました。", "名前は\n{ギリシャ神話}から", v_jason),
    C("調査が、行われたのは、二千二十四年の、十一月から、十二月。", "{2024年}\n11月〜12月", v_2024, point=True),
    C("マリアナ海溝の、南のかべに、そって、七回、もぐりました。", "南のかべを\n{7回}もぐった", P_map, point=True),
    C("しらべた、はんいは、およそ、三百キロメートル。", "{約300km}を\nしらべた", v_300km),
    C("ただし、ジェイソンが、もぐれるのは、六千五百メートルまで。", "もぐれるのは\n{6500mまで}", v_limit, point=True),
    C("それより、深い場所は、まだ、行けなかったんです。", "それより深くは\n{行けない}", v_limit),
    C("持ち帰った、石は、ぜんぶで、百五十五こ。", "持ち帰った石は\n{155こ}", v_samples, point=True, word="タクサン!"),
    C("ここで意外な話。とちゅうでは、海底から、しみ出す、水が、作った、白い、えんとつも、見つかりました。", "海底の\n{白いえんとつ}!?", P_seep1, point=True, word="エッ!"),
    C("深さ、およそ、五千七百メートル。シンカイ・シープ・フィールドと、よばれる場所です。", "{シンカイ・シープ・フィールド}", P_seep),

    # ---- ch3 discovery
    C("さあ、ここからが、今回の、大発見です。", "ここからが\n{大発見}", v_question, **CH(3, "6000mで見つけたもの")),
    C("深さ、六千百四十八メートル。ライトに、てらされた、海の底を、見てください。", "深さ\n{6148m}", v_6148, point=True),
    C("これが、その、本物の、写真です。", "これが\n{本物の写真}", P_flow, point=True),
    C("うすい、岩の、板が、何まいも、重なって、ふちが、まるく、なっていますね。", "ふちが{まるい}\n岩の板", P_flow2),
    C("これは、熱い、火山の、かけらの、流れが、止まった、先っぽの、あと、だと、考えられています。", "火山の流れが\n{止まったあと}", P_flow2, point=True),
    C("さらに深い、六千三百三十四メートルでは、こんな、岩も、ありました。", "深さ\n{6334m}では…", P_cool, point=True),
    C("まっすぐな、われめで、四角く、区切られていますね。", "{四角く}\n区切られている", P_cool),
    C("熱い岩が、冷えて、ちぢむときに、こうして、きれいに、われるんです。", "冷えてちぢんで\n{四角くわれた}", v_cracks, point=True, word="パキッ!"),
    C("一まいの、大きさは、一メートルくらい。まるで、床に、しきつめた、タイルのようです。", "まるで\n{床のタイル}", P_slab),
    C("ライトが、なければ、まっ暗。ジェイソンの、ライトだけが、たよりです。", "ライトだけが\n{たより}", P_slab1),
    C("持ち帰った、石を、切ってみると、角ばった、火山の、かけらが、ギッシリ。", "火山のかけらが\n{ギッシリ}", P_rock1, point=True),
    C("かけらを、かためて、くっつけた、ような、石です。", "かけらが\n{かたまった石}", P_rock2),
    C("研究チームは、これを、海で、いちばん、深い場所で、見つかった、爆発した、火山の、あと、だと、発表しました。", "海でいちばん深い\n{爆発の火山のあと}!", v_deepest, point=True, word="新記録!"),
    C("リーダーの、ロバート・スターンさんは、とても、おどろいた、と話しています。", "研究者も\n{びっくり}!", v_surprise),

    # ---- ch4 pyroclastic flow
    C("ところで、爆発した、火山の、あとって、どういうことでしょう?", "爆発した火山の\n{あと}って?", v_question, **CH(4, "火砕流ってなに?")),
    C("火山には、とろとろの、溶岩が、流れ出す、おだやかな、噴火と、ドカンと、爆発する、噴火が、あります。", "おだやかな噴火と\n{ドカンと爆発}", v_pyro_land),
    C("爆発すると、マグマが、こなごなに、くだけて、熱い、灰や、石に、なります。", "マグマが\n{こなごなに}", v_pyro_land, point=True, word="ドカーン!"),
    C("それが、山の、しゃめんを、いっきに、流れ下るのが、火砕流です。", "それが\n{火砕流}", v_pyro_land, point=True),
    C("火砕流が、冷えて、かたまった、岩には、とくちょうが、あります。", "かたまった岩の\n{とくちょう}", P_rock2),
    C("それが、さっきの、角ばった、かけらが、ギッシリ、つまった、つくり、なんです。", "角ばったかけらが\n{ギッシリ}", P_rock1),
    C("ふつうは、陸の上や、浅い海で、おきる、ことです。", "ふつうは\n{陸や浅い海}", v_pyro_land),
    C("それが、六千メートルの、深海で、見つかったから、大ニュース、なんですね。", "深海で見つかって\n{大ニュース}!", v_hook, point=True),
    C("ただし、深海の、火砕流は、遠くまでは、流れなかったと、考えられています。", "深海の火砕流は\n{遠くまで流れない}", v_pyro_sea, point=True),
    C("ゆっくり、短く、流れて、そこで、止まったようです。", "ゆっくり短く\n{流れて止まった}", v_pyro_sea),

    # ---- ch5 supercritical
    C("では、なぜ、深海では、火山の、爆発が、おだやかに、なるのでしょう?", "なぜ深海では\n{おだやか}になる?", v_question, **CH(5, "水が水でなくなる!?")),
    C("陸の、火山が、ドカンと、爆発するのは、マグマに、とけていた、水が、水蒸気に、なるからです。", "爆発のもとは\n{水蒸気}", v_steam, point=True),
    C("水は、水蒸気に、なると、体積が、およそ、千七百倍に、ふくらみます。", "水蒸気は\n{約1700倍}!", v_steam, word="ボワッ!"),
    C("このいきおいで、マグマが、ふきとばされるんです。", "そのいきおいで\n{ふきとぶ}", v_hook),
    quiz("ここでクイズ!深海で、爆発が、弱くなるのは、なぜでしょう?", "Q.深海で爆発が\n{弱くなる}のはなぜ?", Q2, 1),
    reveal("正解は、B!水蒸気に、ふくらめないから、です!", "正解は{B}!\n{水蒸気にふくらめない}!", Q2, 1),
    C("身近な、例で、いうと、圧力なべ。", "身近な例\n{圧力なべ}", v_cooker, point=True),
    C("ぎゅっと、おされた、水は、ふつうより、高い温度に、ならないと、ふっとう、しません。", "おされると\n{ふっとうしにくい}", v_cooker),
    C("深海の、ものすごい、水の重さでは、さらに、ふしぎなことが、おきます。", "深海では\n{さらにふしぎ}なことが", v_pressure),
    C("水は、およそ、三百七十四度、二百二十気圧を、こえると、液体でも、気体でもない、すがたに、なるんです。", "374℃・約220気圧を\n{こえると}…", v_374, point=True),
    C("これを、超臨界、と、いいます。", "液体でも気体でもない\n{超臨界}", v_super, point=True, word="フシギ!"),
    C("深さ、六千メートルの、圧力は、およそ、六百気圧。だから、マグマの、水は、超臨界に、なっていたと、考えられます。", "6000mは{約600気圧}\n水は超臨界に", v_super),
    C("超臨界の、水は、水蒸気の、およそ、三パーセントの、体積にしか、ふくらみません。", "水蒸気の\n{約3%}しかふくらまない", v_3pct, point=True),
    C("ここで意外な話。超臨界の、二酸化炭素は、コーヒーから、カフェインを、ぬくのにも、使われているんですよ。", "超臨界で\n{カフェインをぬく}!?", v_super, point=True, word="エッ!"),
    C("だから、爆発は、陸の上ほど、はげしくは、ならなかったんです。", "だから爆発は\n{おだやか}に", v_pyro_sea),
    C("それでも、マグマは、くだけて、熱いまま、流れ、冷えて、われた。それが、あの、四角い、岩なんですね。", "熱いまま流れ\n{冷えてわれた}", P_cool, word="ナルホド"),
    C("この、超臨界の、考えは、まだ、たしかめる、ひつようが、ある、と、研究チームは、書いています。", "超臨界の考えは\n{これからたしかめる}", v_question),

    # ---- ch6 why here
    C("それにしても、なぜ、ここに、火山が、あるのでしょう?", "なぜここに\n{火山}が?", v_question, **CH(6, "なぜここに火山が?")),
    C("地球の、表面は、何まいもの、大きな、岩の、板で、できています。", "地球の表面は\n{岩の板}", v_mantle),
    C("マリアナ海溝では、太平洋の、板が、となりの、板の下に、もぐりこんでいます。", "太平洋の板が\n{もぐりこむ}", v_plates, point=True),
    C("その速さは、一年に、およそ、三センチ。つめが、のびる、くらいの、速さです。", "1年に{約3cm}\nつめくらい", v_nail, point=True),
    C("もぐりこみが、始まったのは、およそ、五千二百万年前。", "始まりは\n{5200万年前}", v_52),
    C("ふつう、火山は、海溝から、二百キロメートルくらい、はなれた、場所に、ならびます。", "ふつう火山は\n{海溝からはなれる}", P_fig12, point=True),
    C("ところが、チャレンジャー海淵の、近くでは、その、きょりが、ぎゅっと、近いんです。", "ここは\n{海溝のすぐ近く}!", P_fig12),
    C("この場所では、板が、引っぱられて、うすく、のびています。", "板が引っぱられて\n{うすくのびる}", v_stretch, point=True),
    C("うすくなった、すきまから、地下の、熱い岩が、上がってきて、マグマが、生まれた、と考えられています。", "すきまから\n{マグマ}が生まれる", v_stretch),
    C("東がわでは、さらに、地球の、中の、マントルの、岩まで、海底に、顔を出していました。", "{マントルの岩}が\n顔を出す", v_mantle, point=True),
    C("ここで意外な話。マントルの、岩、かんらん岩には、宝石の、ペリドットと、同じ、なかまの、鉱物が、たくさん、ふくまれています。", "宝石{ペリドット}の\nなかま!", v_peridot, point=True, word="キラッ!"),
    C("チャレンジャー海淵が、とくべつ、深いのも、もぐりこむ板が、急な角度で、きつく、曲がっているから、などと、考えられています。", "板が{きつく曲がる}から\n深い!?", v_plates),
    C("ちなみに、日本の、近くにも、日本海溝や、伊豆・小笠原海溝など、同じように、板が、もぐりこむ、場所が、あります。", "日本の近くにも\n{海溝}がある", v_plates),
    C("火山と、深い海の、なぞは、つながっているのかも、しれないんです。", "火山と深い海の\n{なぞはつながる}", v_trench, word="ナルホド"),

    # ---- ch7 Japan
    C("じつは、この研究、日本とも、深い、つながりが、あります。", "日本との\n{つながり}", v_japan, **CH(7, "日本とのつながり")),
    C("研究チームには、海上保安庁や、産業技術総合研究所、高知大学などの、日本の、研究者も、加わっています。", "{日本の研究者}も\n参加!", v_japan, point=True),
    C("さっきの、シンカイ・シープ・フィールド。この名前は、日本の、潜水船、しんかい六千五百から、来ています。", "名前は\n{しんかい6500}から", v_shinkai, point=True),
    C("しんかい六千五百が、およそ、十五年前に、見つけた、場所なんです。", "しんかい6500が\n{見つけた場所}", P_seep),
    C("ここで、もう一つ、意外な話。見つかった石には、ボニナイト、という、めずらしい、岩も、ありました。", "めずらしい岩\n{ボニナイト}", P_rockh, point=True),
    C("ボニナイトの、名前は、小笠原諸島の、英語の名前、ボニン諸島から、ついたんです!", "名前は\n{小笠原諸島}から!", v_bonin, point=True, word="エッ!"),
    C("小笠原から、マリアナまで、海の底では、ひとつながりの、火山の、列が、続いているんですね。", "小笠原からマリアナへ\n{ひとつながり}", P_mapw),
    C("論文は、二千二十六年、十一月二十三日に、フロンティアーズ・イン・アース・サイエンスという、雑誌に、のりました。", "論文は\n{11月23日}発表", v_nov23),

    # ---- dream
    mod(buildup(), **CH(8, "まだわからないこと")), openbox(),
    C("じつは、この、火砕流が、どこから、ふき出したのかは、まだ、わかっていません。", "ふき出し口は\n{まだわからない}", v_vent, dream=True, point=True),
    C("海溝の、近くの、高まりか、しゃめんの、どこかに、あるかもしれない、と、考えられています。", "どこかに\n{かくれている}かも", v_vent, dream=True),
    C("いつ、ふき出したのかも、これから、石の、年れいを、はかって、しらべます。", "いつふき出したか\n{これからしらべる}", P_rock1, dream=True),
    C("そして、六千五百メートルより、深い場所は、まだ、ほとんど、見られていません。", "6500mより深くは\n{ほとんど見ていない}", v_limit, dream=True, point=True),
    C("持ち帰った、石を、くわしく、しらべれば、マグマに、どれくらい、水が、あったかも、わかってくるかもしれません。", "石から\n{マグマの水}がわかる!?", P_rock2, dream=True),
    C("もっと深く、もぐれる、ロボットが、行けば、さらに、おどろきの、発見が、待っているかも!", "もっと深くへ\n{おどろきの発見}!?", v_dive_deeper, dream=True, word="ワクワク"),
    C("宇宙より、わかっていないとも、いわれる、深海。まだまだ、なぞだらけ、なんです!", "深海は\n{なぞだらけ}!", v_volcano_ring, dream=True),

    # ---- outro
    C("では、今日の、まとめです。", "今日の\n{まとめ}", v_question, **CH(9, "まとめ")),
    C("マリアナ海溝の、深さ、六千メートルより、深い場所で、爆発した、火山の、あとが、見つかりました。", "6000mより深くで\n{爆発のあと}", P_flow),
    C("海で、いちばん、深い、記録です。", "海で{いちばん深い}記録", v_deepest),
    C("深海では、水が、超臨界に、なるので、爆発は、おだやかに、なったと、考えられています。", "水が{超臨界}で\nおだやかな爆発", v_super),
    C("あなたは、深海で、どんな、発見を、してみたい?コメントで、教えてね!", "深海で何を見つけたい?\n{コメントで教えてね}!", v_comment, mood="wow"),
    C("チャンネル登録も、よろしくね!またね!", "チャンネル登録\n{よろしくね}!", v_hello, sfx=[(0.2, "kira")]),
]


if __name__ == "__main__":
    name = "20261125_trench_long"
    tl = E4.build4(CUTS, seed=113)
    print("total", round(tl["total"], 1), "cuts", len(tl["cuts"]), "points", tl["npoints"], flush=True)
    if sys.argv[1:] and sys.argv[1] == "chapters":
        for e in tl["cuts"]:
            if e["cut"].kw.get("chapter"):
                t = int(e["t0"]); print(f"{t // 60}:{t % 60:02d} {e['cut'].kw['chapter']}")
        sys.exit()
    frame = make_wide(tl, genre="地球", gcol="#1FA37A")
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [c["t0"] + min(0.7, c["d"] / 2) for c in tl["cuts"]]
        if len(sys.argv) > 2:
            ts = ts[int(sys.argv[2]):int(sys.argv[3])]
        render_wide(None, tl, frame, ts, f"preview4/{name}")
    else:
        os.makedirs("out4", exist_ok=True)
        render_wide(f"out4/{name}_video.mp4", tl, frame)
        E4.build_audio4(f"out4/{name}.wav", tl, 0)
        E2.mux2(f"out4/{name}_video.mp4", f"out4/{name}.wav", f"out4/{name}_final.mp4")
        print("done", flush=True)
