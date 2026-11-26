"""Long-form (16:9, ~8 min) episode: BepiColombo reaches Mercury. Same look as the Shorts."""
import os, sys, math, subprocess
import cairo
from common4 import *
from hera_vis import *
from mercury_vis import *
from space3 import eyes
import engine2 as E2, engine3 as E3, engine4 as E4

WW, HH = 1920, 1080


def C(say, cap, vis, **kw):
    kw.setdefault("capsize", 96)
    return Cut(say, cap, vis, **kw)


CH = lambda n, t: dict(chapter=f"第{n}章 {t}")
Q1 = ["3回", "6回", "9回"]
Q2 = ["1日", "59日", "176日"]

CUTS = [
    # ---- opening
    eyes(C("太陽系で、いちばん、行くのが大変な惑星って、どこだと思いますか?", "いちばん行くのが\n{大変な惑星}は?", v_question, chapter="オープニング", mood="wow"), [], hit=True, word="ムムッ"),
    C("遠い海王星?それとも、冥王星?", "遠い{海王星}?\nそれとも{冥王星}?", v_pluto),
    C("じつは、答えは、太陽にいちばん近い、水星なんです!", "答えは\n太陽に近い{水星}!", v_hook_mercury, point=True, word="ドーン!"),
    C("その水星に、ヨーロッパと日本の探査機、ベピコロンボが、八年かけて、たどり着きました!", "8年かけて\n{ベピコロンボ}が到着!", v_eight_years, point=True, sfx=[(0.1, "kira")]),
    C("これは、ベピコロンボが、自分で撮った、本物の水星の写真です。", "自分で撮った\n{本物の水星}!", P_flyby6, point=True),
    C("そして、いよいよ、水星をまわる軌道に入る、大作戦の日を、迎えました!", "水星をまわる\n{大作戦の日}!", v_capture),
    C("今日は、この、八年がかりの大冒険を、本物の写真といっしょに、まるごと解説します!", "8年がかりの冒険を\n{写真つきで解説}!", v_question),
    C("最後には、日本の探査機、みおの、すごい話も出てくるよ!", "最後には\n日本の{みお}の話も!", v_mio, teaser=True, mood="wow"),

    # ---- ch1 Mercury
    C("まずは、水星って、どんな星なのか。", "水星って\n{どんな星}?", v_solar, **CH(1, "水星ってどんな星?")),
    C("水星は、太陽にいちばん近い惑星で、太陽系で、いちばん小さな惑星です。", "太陽にいちばん近くて\n{いちばん小さい}", v_solar, point=True),
    C("大きさは、月より、ひとまわり大きいくらい。", "大きさは\n{月よりひとまわり大きい}", v_dark),
    C("英語の名前は、マーキュリー。ローマ神話の、足の速い、神さまの名前です。", "英語では\n{マーキュリー}", v_solar, word="ビュン"),
    C("太陽のまわりを、いちばん速く、かけまわる惑星に、ぴったりの名前ですね。", "いちばん速く\n{かけまわる}惑星!", v_solar, point=True),
    C("太陽のまわりを、たった、八十八日で、一周します。", "1年は\nたった{88日}!", v_day, word="ビュン"),
    C("昼の地面は、四百度以上。なまりが、とけてしまうほどの熱さです。", "昼は\n{400℃以上}!", v_temp, point=True, word="アチチ"),
    C("ところが、夜になると、マイナス百七十度くらいまで、冷えこみます。", "夜は\n{-170℃}くらい!", v_temp, word="ブルブル"),
    C("空気が、ほとんどないので、熱を、ためておけないんです。", "空気がほとんどなく\n{熱をためられない}", v_temp),
    quiz("ここでクイズ!水星の一日、つまり、日の出から、次の日の出までは、地球の何日分?", "Q.水星の1日は\n{地球の何日分}?", Q2, 2),
    reveal("正解は、C!なんと、百七十六日!", "正解は{C}!\n{176日}!", Q2, 2),
    C("水星では、一年が八十八日なのに、一日は、百七十六日。一日のほうが、一年より、長いんです!", "1日が\n{1年より長い}!", v_day, point=True, word="ガーン!"),
    C("日の出から、日の入りまで、地球の、三か月くらい、ずっと、昼がつづくんですね。", "昼が\n{約3か月}つづく!", v_temp),

    # ---- ch2 why hard
    C("では、なぜ、近いはずの水星に、行くのが、大変なのでしょう?", "近いのに\n{なぜ大変}?", v_question, **CH(2, "なぜ水星は行きにくい?")),
    C("ヒントは、太陽の、重力です。", "ヒントは\n{太陽の重力}", v_slope),
    C("太陽に近づくのは、長い坂道を、転がり落ちるようなもの。", "{長い坂道}を\n転がり落ちるみたい", v_slope, word="ゴロゴロ"),
    C("どんどん、スピードが、上がってしまうんです。", "スピードが\n{どんどん上がる}!", v_slope, point=True, word="ギュイーン"),
    C("そのままだと、水星の前を、びゅんと、通りすぎてしまいます。", "そのままだと\n{通りすぎちゃう}!", v_brake),
    C("水星をまわるには、思いきり、ブレーキを、かけないといけません。", "思いきり\n{ブレーキ}が必要!", v_brake, word="キキーッ"),
    C("じつは、水星をまわる軌道に入るのは、冥王星に行くより、たくさんの、エネルギーが、いると、言われています。", "冥王星へ行くより\n{エネルギーが必要}!", v_pluto, point=True, word="ドドド"),
    C("ちなみに、冥王星に行った、NASAの探査機、ニューホライズンズは、約九年半かかりました。", "冥王星までは\n{約9年半}", v_pluto),
    C("お隣の水星に、八年かかるのは、それくらい、大変なことなんです。", "お隣の水星まで\n{8年}!", v_eight_years),
    C("水星を、ぐるぐるまわった探査機は、これまで、アメリカのメッセンジャー、ただ一機だけでした。", "水星をまわったのは\n{メッセンジャーだけ}", v_messenger),
    C("ちなみに、メッセンジャーは、四年間、水星をまわって、二千十五年に、役目を終えました。", "メッセンジャーは\n{2015年}に役目を終えた", v_messenger),
    C("ベピコロンボは、その、次の、ランナーなんです。", "ベピコロンボは\n{次のランナー}!", v_hook_mercury, point=True),

    # ---- ch3 the journey
    C("では、ベピコロンボの旅を、見てみましょう。", "ベピコロンボの\n{旅}を見てみよう", v_launch, **CH(3, "8年・100億kmの旅")),
    C("出発は、二千十八年十月。南アメリカの、フランス領ギアナから、アリアン5ロケットで、打ち上げられました。", "2018年10月\n{アリアン5}で出発!", v_launch, word="ゴゴゴ"),
    C("ベピコロンボは、じつは、三つの部分が、重なった、合体ロボみたいな探査機です。", "3つが重なった\n{合体ロボ}!", v_ion, point=True),
    C("いちばん下は、エンジン係。真ん中が、ヨーロッパの、水星をくわしく調べる探査機。", "下は{エンジン係}\n真ん中は{ヨーロッパ}", v_ion),
    C("そして、いちばん上に、日本の探査機、みおが、乗っています。", "いちばん上に\n{日本のみお}!", v_mio, point=True, word="キラーン"),
    C("エンジン係は、電気で、ガスを押し出して進む、イオンエンジン。青く光るんです。", "電気で進む\n{イオンエンジン}", v_ion),
    C("力は弱いけれど、何か月も、休まずに、ふかし続けられます。", "弱いけど\n{何か月も続く}!", v_ion),
    C("それでも、ブレーキは、ぜんぜん足りません。", "それでも\n{ブレーキが足りない}", v_brake),
    C("そこで使ったのが、惑星のそばを通って、重力で、スピードを調整する、スイングバイです。", "惑星の重力を使う\n{スイングバイ}!", v_swingby, point=True, word="ヒュー"),
    quiz("ここでクイズ!ベピコロンボは、水星に着くまでに、何回、惑星のそばを、通ったでしょう?", "Q.惑星のそばを\n{何回}通った?", Q1, 2),
    reveal("正解は、C!九回です!", "正解は{C}!\n{9回}!", Q1, 2),
    C("地球で一回、金星で二回、そして、水星で、六回!", "地球1・金星2\n{水星6回}!", v_flybys, point=True),
    C("旅した距離は、なんと、約百億キロ!", "旅した距離は\n約{100億km}!", v_route, point=True, word="ドドド"),
    C("地球と太陽の、六十倍以上の、距離です。", "地球と太陽の\n{60倍以上}!", v_route),
    C("じつは、二千二十四年、エンジン係の、電気が足りなくなる、トラブルがありました。", "2024年\n{電気が足りない}!", v_trouble, word="ガーン!"),
    C("エンジンを、全力で使えなくなったので、道のりを、計算しなおしたんです。", "道のりを\n{計算しなおし}", v_trouble),
    C("そのせいで、到着は、約一年、遅れました。でも、あきらめずに、ここまで来たんです!", "約1年おくれても\n{あきらめない}!", v_route, point=True),

    # ---- ch4 photos
    C("旅のとちゅうで、ベピコロンボは、たくさんの写真を、送ってきました。", "旅のとちゅうで\n{写真がいっぱい}", P_best6, **CH(4, "本物の写真でわかったこと")),
    C("撮ったのは、エンジン係についた、自撮り用の、モニターカメラです。", "撮ったのは\n{自撮りカメラ}!", v_selfie, point=True, word="パシャ"),
    C("だから、写真のはしに、探査機の、アンテナや、うでが、写りこんでいるんです。", "はしに{探査機のうで}が\n写りこんでる!", P_flyby6),
    C("これは、二千二十五年一月、六回目の、水星フライバイで、撮った写真。", "2025年1月\n{6回目のフライバイ}", P_north),
    C("水星の、地面から、たった、二百九十五キロのところを、通りすぎました。", "地面から\n{たった295km}!", P_north, point=True, word="ヒュー"),
    C("ここは、水星の北極。クレーターの底が、まっ黒な影に、なっていますね。", "水星の北極\n{まっ黒な影}", P_north_lab),
    C("このクレーターの底には、一度も、日の光が、当たりません。", "一度も\n{日が当たらない}", v_ice),
    C("太陽にいちばん近い惑星なのに、太陽系で、いちばん寒い場所の、ひとつなんです。", "太陽に近いのに\n{いちばん寒い場所}!", v_ice, point=True, word="ブルブル"),
    C("そして、そこには、凍った水、つまり、氷がある、かもしれないんです!", "なんと\n{氷があるかも}!", v_ice, point=True, word="ワオ!"),
    C("こちらは、日の当たる、北の平原。三十七億年前に、流れ出た、溶岩で、できた、平らな土地です。", "37億年前の\n{溶岩の平原}", P_sunlit),
    C("しわしわの、すじは、水星が、冷えて、ちぢんだときに、できたと、考えられています。", "しわは\n{ちぢんでできた}!?", v_shrink, word="ムムッ"),
    C("じつは、水星は、月より、黒っぽい星。月の、三分の二くらいしか、光を、はね返しません。", "水星は\n{月より黒っぽい}", v_dark),
    C("だから、明るく見える場所は、新しい場所なんです。", "明るい場所は\n{新しい場所}!", P_lava, point=True),
    C("この明るいところは、水星で、いちばん大きな、火山の大爆発の、あと。", "水星いちばんの\n{火山の大爆発}のあと", P_lava, word="ドカーン!"),
    C("左下には、水星でいちばん大きな、カロリス盆地。直径、千五百キロ以上の、巨大なクレーターです。", "カロリス盆地は\n直径{1500km以上}!", P_sunlit, point=True, word="ドドド"),
    C("東京から、沖縄までと、同じくらいの、大きさです。", "{東京〜沖縄}と\n同じくらい!", P_sunlit),
    C("ふき出した物が、直径、三百キロ以上に、広がっています。", "直径{300km以上}に\n広がった!", P_lava),

    # ---- ch5 names (surprise)
    C("ところで、ベピコロンボって、ふしぎな名前ですよね。", "ベピコロンボって\n{ふしぎな名前}", v_question, **CH(5, "名前のひみつ")),
    C("これは、イタリアの科学者、ジュゼッペ・コロンボさんの、ニックネームなんです。", "イタリアの科学者\n{コロンボさん}!", v_colombo, point=True),
    C("コロンボさんは、半世紀前、アメリカの探査機、マリナー10号に、水星に、何度も会える、道のりを、考えました。", "水星に{何度も会える}\n道を考えた!", v_mariner, point=True),
    C("そのおかげで、マリナー10号は、水星のそばを、三回も、通ることができたんです。", "マリナー10号は\n{3回}も会えた!", v_mariner),
    C("そして、日本の探査機の名前、みおは、漢字で、さんずいに、ひだり、みぎの、みお。", "日本の探査機は\n{みお(澪)}", v_mio),
    C("船が通る、水の道、という意味です。遠い水星までの、長い旅が、無事に進むように、という願いがこめられています。", "船が通る\n{水の道}という意味", v_mio, point=True, word="キラーン"),

    # ---- ch6 capture
    C("さあ、いよいよ、水星をまわる、軌道に入ります。", "いよいよ\n{水星の軌道へ}!", v_capture, **CH(6, "水星につかまえてもらう")),
    C("二千二十六年九月、まず、エンジン係が、切りはなされました。", "2026年9月\n{エンジン係}とお別れ", P_art, point=True),
    C("ここからは、水星の、重力に、そっと、つかまえてもらう作戦です。", "水星の重力に\n{そっとつかまえてもらう}", v_capture),
    C("ヨーロッパ宇宙機関の、予定表では、十一月二十一日に、水星の重力に、つかまります。", "予定表では\n{11月21日}につかまる", P_timeline),
    C("日本時間では、二十二日の、未明にあたります。", "日本時間では\n{22日の未明}", v_calendar2("11月", "22日", "日本時間")),
    C("最初の軌道は、とても細長い、だ円。いちばん遠いときは、水星から、約十七万八千キロも、はなれます。", "最初は{細長いだ円}\n最遠 約17万8000km", v_capture, point=True, word="ヒュー"),
    C("地球から月までの、半分くらいの、距離ですね。", "地球〜月の\n{半分くらい}!", v_capture),
    C("ここで、日の光の強さも、地球の、約十倍。探査機には、ものすごく、きびしい場所です。", "日ざしは\n{地球の約10倍}!", v_sunlight, word="アチチ"),

    # ---- ch7 next / Japan
    C("では、これから、どうなるのか。", "これから\n{どうなる}?", v_question, **CH(7, "これからの予定")),
    C("十二月九日から十日ごろ、ヨーロッパの探査機と、日本のみおが、ふたつに分かれます。", "12月9〜10日ごろ\n{ふたつに分かれる}!", v_split, point=True, word="パカッ"),
    C("みおは、くるくる回りながら、水星から、遠くまで、ふくらむ、細長い軌道を、まわります。", "みおは\n{くるくる回りながら}", v_mio),
    C("みおの仕事は、水星の、磁石の力と、太陽から吹いてくる、風との、たたかいを、調べることです。", "みおは\n{磁石の力}を調べる", v_magnet, point=True),
    C("水星には、小さいのに、地球みたいな、磁石の力が、あるんです。強さは、地球の、百分の一くらい。", "強さは\n地球の{100分の1}くらい", v_magnet, word="ムムッ"),
    C("なぜ、こんな小さな星に、磁石の力が、あるのか。それも、大きななぞなんです。", "なぜあるの?\n{大きななぞ}", v_question),
    C("ヨーロッパの探査機は、もっと低い軌道から、地面を、くわしく調べます。", "ヨーロッパの探査機は\n{地面をくわしく}", v_twoorbits),
    C("水星の、中には、とても大きな、鉄のしんが、あると、考えられています。", "中には\n{大きな鉄のしん}", v_core, point=True, word="ドドド"),
    C("なぜ、そんなに鉄が多いのか。昔、大きな星と、ぶつかったから、という説もあります。", "なぜ鉄が多い?\n{ぶつかった説}も", v_core),
    C("二機が、同時に、水星をまわるのは、史上はじめて!", "2機で同時は\n{史上はじめて}!", v_twoorbits, point=True, word="ジャーン!"),
    C("本番の観測は、二千二十七年四月から、始まる予定です。", "本番の観測は\n{2027年4月}から", P_timeline_late),

    # ---- ch8 fun
    C("最後に、ちょっと、ほっこりする話を。", "最後に\n{ほっこりする話}", v_contest, **CH(8, "ようこそ水星へ")),
    C("ヨーロッパ宇宙機関は、到着を記念して、ようこそ水星へ、という作品を、募集しました。", "{ようこそ水星へ}\n作品を募集!", v_contest),
    C("人形劇、詩、歌、ししゅう、ねんど。六十をこえる作品が、集まったそうです。", "{60作品以上}が\n集まった!", v_contest, point=True),
    C("その中で、日本から、ベピコロンボの、アフタヌーンティーを作った人が、特別に、紹介されました!", "日本から\n{アフタヌーンティー}!", v_tea, point=True, word="ワオ!"),
    C("宇宙の探査は、科学者だけのものじゃない。みんなで、楽しむものなんですね。", "宇宙は\n{みんなで楽しむもの}", v_team2),

    # ---- dream
    buildup(), openbox(),
    C("もし、水星の、日かげのクレーターに、本当に、氷があったら。", "もし本当に\n{氷があったら}…", v_ice, dream=True, word="ゴゴゴ"),
    C("太陽のすぐそばで、水が、何億年も、守られてきたことになります。", "太陽のそばで\n{水が守られてきた}!", v_ice, dream=True, point=True, word="キラーン"),
    C("水星が、どうやって、生まれたのか。地球のような、岩の惑星の、ひみつも、わかるかもしれません。", "地球のような惑星の\n{ひみつ}がわかるかも!", v_solar, dream=True, point=True),
    C("ヨーロッパと、日本が、力を合わせて、いちばん行きにくい惑星の、なぞにいどむ。ワクワクしますね!", "ヨーロッパ×日本で\n{なぞにいどむ}!", v_team2, dream=True, point=True, word="ワクワク"),

    # ---- outro
    C("では、今日のまとめです。", "今日の\n{まとめ}", v_question, **CH(9, "まとめ")),
    C("水星は、太陽に近いせいで、いちばん、行きにくい惑星。", "水星は\n{いちばん行きにくい}", v_slope),
    C("ベピコロンボは、九回のスイングバイと、約百億キロの旅で、八年かけて、水星にたどり着きました。", "9回のスイングバイ\n{8年・約100億km}", v_route),
    C("このあと、日本のみおと、ヨーロッパの探査機に分かれて、二千二十七年から、本番の観測です!", "2027年から\n{本番の観測}!", v_split),
    C("あなたなら、水星の、どんななぞを、調べてみたい?コメントで、教えてね!", "どんななぞを調べたい?\n{コメントで教えてね}!", v_question, mood="wow"),
    C("チャンネル登録も、よろしくね!またね!", "チャンネル登録\n{よろしくね}!", v_hook_mercury, sfx=[(0.2, "kira")]),
]


# ---------------------------------------------------------------- widescreen frame
def _patch(w, h):
    for m in (E2, E3, E4):
        m.W, m.H = w, h


def chapter_at(tl, idx):
    name = "オープニング"
    for e in tl["cuts"][: idx + 1]:
        name = e["cut"].kw.get("chapter", name)
    return name


def make_wide(tl, genre="宇宙", gcol="#7B5CFF"):
    cuts = tl["cuts"]; total = tl["total"]
    pts = [e for e in cuts if e["point"]]
    P = max(1, len(pts))
    stage = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)

    def frame(ctx, gt):
        e = cuts[-1]
        for c in cuts:
            if c["t0"] <= gt < c["t0"] + c["d"]:
                e = c; break
        lt = gt - e["t0"]
        nb = sum(1 for b in e["beats"] if b <= lt)
        pal = e["pal"]
        if nb:
            pal = E3.EXTRA_PATS[(e["i"] + nb) % len(E3.EXTRA_PATS)] if nb % 2 else E2.PALETTES[(e["i"] * 2 + nb) % len(E2.PALETTES)]
            if e["dream"]:
                pal = E3.DREAM_PALS[(e["i"] + nb) % len(E3.DREAM_PALS)]
        _patch(WW, HH)
        try:
            hi = E3.draw_bg3(ctx, pal, lt, gt)
        finally:
            _patch(1080, 1920)
        # --- stage: the vertical scene, drawn on a transparent layer, placed on the left
        sc = cairo.Context(stage)
        sc.set_operator(cairo.OPERATOR_CLEAR); sc.paint(); sc.set_operator(cairo.OPERATOR_OVER)
        sc.save(); E2.camera(sc, e, lt); e["cut"].vis(sc, lt, e["d"], gt)
        for (ex, ey, er) in e["cut"].kw.get("eyes", []):
            E3.googly(sc, ex, ey, er, gt, e["i"])
        sc.restore()
        E3.word_sticker(sc, e, lt)
        stage.flush()
        S = 0.80
        wob = 0.02 * math.sin(gt * 5.3)
        ctx.save(); ctx.translate(560, 650); ctx.rotate(wob); ctx.scale(S, S); ctx.translate(-540, -960)
        ctx.set_source_surface(stage, 0, 0); ctx.paint(); ctx.restore()
        # --- right panel: chapter + caption
        chap = chapter_at(tl, e["i"])
        rrect(ctx, 1110, 170, 760, 96, 48); fill_stroke(ctx, "#FFFFFF", lw=6)
        cs = text_sprite(chap, 44, color="#1B1B3A", hi="#FF3D7F", stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS["mochiy"])
        draw_sprite(ctx, cs, 1490, 218, min(1.0, 700 / max(1, cs.get_width())), 1)
        cap = e["cut"].cap
        if cap:
            size = 88
            spr = text_sprite(cap, size, color="#FFFFFF", hi=hi, stroke="#1B1B3A", stroke_w=12, path=FONTS[e["font"]])
            fit = min(1.0, 740 / max(1, spr.get_width()), 420 / max(1, spr.get_height()))
            p = clamp((lt - 0.04) / 0.28) if e["i"] else 1.0
            s = fit * (ease_out_back(p, 2.4) if p < 1 else 1.0)
            for b in e["beats"]:
                if b <= lt < b + 0.2:
                    s *= 1 + 0.06 * (1 - (lt - b) / 0.2)
            draw_sprite(ctx, spr, 1490, 560, max(s, 1e-3), clamp(p * 3), -0.02 if e["i"] % 2 else 0.02)
        # chapter splash on the first second of a chapter
        if e["cut"].kw.get("chapter") and e["i"] > 0 and lt < 1.4:
            q = clamp(lt / 0.25); a = clamp((1.4 - lt) / 0.3)
            rrect(ctx, 140, 510, 840, 200, 40); ctx.set_source_rgba(0.1, 0.1, 0.23, 0.85 * a); ctx.fill()
            draw_sprite(ctx, text_sprite(chap, 76, color="#FFE14D", hi="#FF3D7F", path=FONTS["dela"]), 560, 610, ease_out_back(q, 2.2), a)
        # --- mascot (bottom right), talking bounce
        bounce = abs(math.sin(gt * 7)) * 18
        mood = "wow" if (nb % 2 or e["cut"].kw.get("mood") == "wow") else "smile"
        piko(ctx, 1780, 930 - bounce, gt, 0.55, mood, look=-0.6)
        # --- header
        card(ctx, 40, 24, 1840, 104, "#FFFFFF", 0.97, 52)
        draw_sprite(ctx, text_sprite("今日の{ワクワク}ニュース 特別編", 52, color="#1B1B3A", hi="#FF3D7F", stroke="#FFFFFF",
                                     stroke_w=3, shadow=False, path=FONTS["mochiy"]), 460, 76)
        rrect(ctx, 1620, 44, 236, 64, 32); fill_stroke(ctx, gcol, lw=6)
        draw_sprite(ctx, text_sprite(genre, 38, color="#FFFFFF", stroke="#1B1B3A", stroke_w=5, shadow=False, path=FONTS["mochiy"]), 1738, 76)
        # progress (whole video) + chapter ticks
        rrect(ctx, 40, 140, 1840, 14, 7); ctx.set_source_rgba(0, 0, 0, 0.3); ctx.fill()
        pr = clamp(gt / total)
        if pr > 0.005:
            rrect(ctx, 40, 140, 1840 * pr, 14, 7); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.fill()
        for c in cuts:
            if c["cut"].kw.get("chapter") and c["i"] > 0:
                x = 40 + 1840 * c["t0"] / total
                circle(ctx, x, 147, 11, "#FFFFFF", lw=4)
        # --- wakuwaku meter (right panel, bottom)
        got = sum(1 for x in pts if gt >= x["t0"] + 0.85)
        rrect(ctx, 1130, 900, 520, 30, 15); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()
        if got:
            g = cairo.LinearGradient(1130, 0, 1650, 0)
            for k, c in enumerate(["#4FF0FF", "#FFE14D", "#FF3D7F"]):
                g.add_color_stop_rgb(k / 2, *hexc(c)[:3])
            rrect(ctx, 1130, 900, max(30, 520 * got / P), 30, 15); ctx.set_source(g); ctx.fill()
        rrect(ctx, 1130, 900, 520, 30, 15); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(4); ctx.stroke()
        lab = "ワクワク度 MAX!" if got == P else f"ワクワク度 {got}/{P}"
        draw_sprite(ctx, text_sprite(lab, 36, color="#FFFFFF", hi="#FFE14D", stroke="#1B1B3A", stroke_w=5, path=FONTS["dela"]), 1390, 960, 1, 1)
        for x in pts:
            l2 = gt - x["t0"]
            if 0.35 <= l2 < 0.85:
                q = ease_in_out((l2 - 0.35) / 0.5)
                tx = 1130 + 520 * (x["pidx"] / P)
                cx_, cy_ = 560 + (tx - 560) * q, 650 + (915 - 650) * q - math.sin(q * math.pi) * 200
                circle(ctx, cx_, cy_, 34 * (1 - 0.4 * q), "#FFD23F", lw=6)
                draw_sprite(ctx, text_sprite("+1", 52, color="#FFE14D", path=FONTS["dela"]), cx_ + 56, cy_ - 40, 1, 1 - q * 0.5)
        # transition flash
        if lt < 0.12 and e["i"]:
            ctx.rectangle(0, 0, WW, HH); ctx.set_source_rgba(1, 1, 1, 0.5 * (1 - lt / 0.12)); ctx.fill()

    return frame


def render_wide(path, tl, frame, preview_times=None, preview_dir=None, vbit="1250k"):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WW, HH)
    def draw(t):
        ctx = cairo.Context(surf); frame(ctx, t); surf.flush()
    if preview_times:
        os.makedirs(preview_dir, exist_ok=True)
        for pt in preview_times:
            draw(pt); surf.write_to_png(os.path.join(preview_dir, f"t{pt:06.2f}.png"))
        return
    tmp = path[:-4] + ".tmp.mp4"
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{WW}x{HH}",
                             "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-b:v", vbit,
                             "-maxrate", "1800k", "-bufsize", "3600k", "-g", "60", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = int(round(tl["total"] * 30))
    for i in range(n):
        draw(i / 30)
        proc.stdin.write(bytes(surf.get_data()))
        if i % 1800 == 0:
            print(f"frame {i}/{n}", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    os.replace(tmp, path)


if __name__ == "__main__":
    name = "20261122_mercury_long"
    tl = E4.build4(CUTS, seed=41)
    print("total", round(tl["total"], 1), "cuts", len(tl["cuts"]), "points", tl["npoints"], flush=True)
    frame = make_wide(tl)
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [c["t0"] + min(0.7, c["d"] / 2) for c in tl["cuts"]][::4] + [tl["cuts"][5]["t0"] + 0.3]
        render_wide(None, tl, frame, ts, f"preview4/{name}")
    elif sys.argv[1:] and sys.argv[1] == "time":
        pass
    else:
        os.makedirs("out4", exist_ok=True)
        render_wide(f"out4/{name}_video.mp4", tl, frame)
        E4.build_audio4(f"out4/{name}.wav", tl, 0)
        E2.mux2(f"out4/{name}_video.mp4", f"out4/{name}.wav", f"out4/{name}_final.mp4")
        print("done", flush=True)
