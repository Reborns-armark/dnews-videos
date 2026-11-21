"""Long-form (16:9, ~8 min) episode: Hera arrives at the asteroid DART hit. Same look as the Shorts."""
import os, sys, math, subprocess
import cairo
from common4 import *
from hera_vis import *
import engine2 as E2, engine3 as E3, engine4 as E4

WW, HH = 1920, 1080


def C(say, cap, vis, **kw):
    kw.setdefault("capsize", 96)
    return Cut(say, cap, vis, **kw)


CH = lambda n, t: dict(chapter=f"第{n}章 {t}")
Q1 = ["約3分", "約33分", "約3時間"]
Q2 = ["アメリカ", "中国", "日本"]

CUTS = [
    # ---- opening
    eyes(C("四年前、人類は、宇宙で、小惑星に、わざと体当たりしました。", "人類は小惑星に\n{わざと体当たり}した", v_hook_crash, chapter="オープニング", mood="wow"), [], hit=True, word="ドーン!"),
    C("これが、その瞬間に、噴き出したちりの、本物の写真です。", "噴き出したちりの\n{本物の写真}", P_plume, point=True, word="バーン!"),
    C("そして今月、その事故現場に、ついに、探偵がやってきた!", "その現場に\n{探偵}がやってきた!", v_detective, point=True, sfx=[(0.1, "kira")]),
    C("ヨーロッパの探査機、ヘラが、小惑星に到着して、写真を送ってきたんです!", "探査機{ヘラ}が\n写真を送ってきた!", P_first, point=True),
    C("今日は、この、宇宙の現場検証を、本物の写真といっしょに、まるごと解説します!", "宇宙の現場検証を\n{写真つきで解説}!", v_question),
    C("最後には、地球を守る、すごい話も出てくるよ!", "最後には\n{地球を守る話}も!", v_shield, teaser=True, mood="wow"),

    # ---- ch1 the target
    C("まずは、主役の小惑星から。名前は、ディディモス。", "主役の小惑星\n{ディディモス}", P_didy_wide, **CH(1, "主役は2つの小惑星")),
    C("じつはこれ、ふたつで一組の、二重小惑星なんです。", "ふたつで一組の\n{二重小惑星}!", v_pair),
    C("大きいほうが、ディディモス。そのまわりを、小さなディモルフォスが、回っています。", "大きい{ディディモス}を\n小さい{ディモルフォス}が回る", P_dart_both),
    C("大きさは、ディディモスが、約七百八十メートル。東京タワーの、二倍以上です!", "ディディモスは\n{約780m}!", v_sizes, point=True, word="ドドド"),
    C("いっぽう、ディモルフォスは、約百五十一メートル。東京タワーの、半分くらいです。", "ディモルフォスは\n{約151m}", v_sizes),
    C("ヨーロッパの宇宙機関は、スペインの、サグラダ・ファミリアと、くらべた絵も、出しています。", "サグラダ・ファミリアと\n{くらべると}…", P_sagrada),
    C("ちなみに、名前は、ギリシャ語。ディディモスは、ふたご。ディモルフォスは、ふたつの形、という意味です。", "ディディモス={ふたご}\nディモルフォス={ふたつの形}", v_names),
    C("ディモルフォスという名前は、体当たりで、形が変わるかもしれない、ということから、つけられたそうです。", "体当たりで\n{形が変わる}から!?", v_names, word="ムムッ"),
    C("そして、探査機のヘラも、ギリシャ神話の、女神の名前なんです。", "ヘラは\n{ギリシャ神話の女神}", v_hera_goddess),
    C("ディディモスは、たった二・二時間で、くるっと一回転。ばらばらになりそうなくらいの、速さなんです。", "{2.2時間}で1回転\nばらばら寸前!?", v_ridge, word="グルグル"),
    C("このふたつ、地球にぶつかる心配は、ありません。安心してね。", "地球にぶつかる\n心配は{なし}", v_safe),

    # ---- ch2 DART
    # ---- ch new: why move asteroids
    C("ところで、そもそも、なんで、小惑星を動かす練習なんて、するんでしょう?", "そもそも\n{なんで動かすの}?", v_why, **CH(2, "なぜ小惑星を動かすの?")),
    C("大むかし、六千六百万年前。直径、約十キロの小惑星が、地球にぶつかりました。", "6600万年前\n{約10km}の小惑星", v_dino, word="ゴゴゴ"),
    C("これが、恐竜がいなくなった、大きな原因の一つと、考えられています。", "恐竜がいなくなった\n{原因の一つ}", v_dino, mood="wow"),
    C("二千十三年には、ロシアのチェリャビンスクに、小さな小惑星が落ちて、空で大爆発しました。", "2013年ロシアで\n{空で大爆発}", v_fireball, word="ピカーッ"),
    C("衝撃で、たくさんの建物の、窓ガラスが割れたんです。", "衝撃で\n{窓ガラスが割れた}", v_fireball),
    C("いま、ぶつかりそうな小惑星は、見つかっていません。でも、もしもの時のために、方法を確かめておきたい。", "もしもの時のために\n{方法を確かめたい}", v_shield, point=True),
    C("そこで考えられたのが、探査機を、ぶつけて、押す方法です。", "探査機を\n{ぶつけて押す}!", v_hook_crash),
    C("ビリヤードの玉みたいに、ぶつけた勢いで、小惑星の速さを、ほんの少しだけ、変えるんです。", "ビリヤードみたいに\n{少しだけ}押す", v_billiard, point=True, word="ポヨン"),
    C("ほんの少しでも、何年も前から押しておけば、地球に着くころには、大きくずれて、ぶつからなくなります。", "早めに押せば\n{大きくずれる}!", v_shield),
    C("では、四年前に、何が起きたのか。", "4年前に\n{何が起きた}?", v_why, **CH(3, "4年前の体当たり")),
    C("二千二十二年九月、NASAの探査機、ダートが、ディモルフォスに、まっすぐ突っ込みました。", "NASAの{ダート}が\n突っ込んだ!", v_hook_crash, mood="wow"),
    C("ダートの重さは、約五百八十キロ。スピードは、なんと、秒速六・一キロ!", "なんと\n{秒速6.1km}!", v_dart_fly, point=True, word="ギュイーン"),
    C("東京から大阪まで、一分ちょっとで着く、ものすごい速さです。", "東京→大阪を\n{1分ちょっと}!", v_dart_fly),
    C("これは、ダートが、ぶつかる直前に、撮った、ディモルフォスです。", "ぶつかる直前の\n{ディモルフォス}", P_dart_dimo, point=True),
    C("そして、こちらが、最後の一枚。通信がとぎれて、写真が、とちゅうで、切れています。", "最後の1枚は\n{とちゅうで切れた}", P_dart_final, word="ガーン!"),
    C("この、最後の、まるごと写った写真は、ぶつかる、約二秒前。距離は、たった十二キロでした。", "ぶつかる{約2秒前}\n距離{12km}!", P_dart_dimo, word="ドドド"),
    C("ぶつかった瞬間、ちりが、ぶわっと、噴き出しました。近くを飛んでいた、イタリアの小さな衛星が、撮った写真です。", "イタリアの衛星が\n{撮った瞬間}", P_plume),
    C("ハッブル宇宙望遠鏡で見ると、ちりが、まるで、しっぽのように、一万キロ以上も、のびていました!", "ちりのしっぽが\n{1万km以上}!", P_hubble, point=True, word="ヒュー"),
    C("これは、わざと小惑星の進む道を、変えられるか、試す実験だったんです。", "道を{変えられるか}\n試す実験!", v_shield),

    # ---- ch3 result + quiz
    C("では、結果はどうなったのか。", "結果は\n{どうなった}?", v_why, **CH(4, "実験の結果")),
    C("ディモルフォスは、もともと、約十一時間五十五分で、ディディモスを一周していました。", "もともと1周\n{11時間55分}", v_clock),
    quiz("ここでクイズ!体当たりで、一周の時間は、どれくらい短くなった?", "Q.1周は\n{どれくらい短く}なった?", Q1, 1),
    reveal("正解は、B!約三十三分も、短くなりました!", "正解は{B}!\n約33分!", Q1, 1),
    C("つまり、小惑星の通り道が、ちゃんと変わったんです!", "通り道が\n{ちゃんと変わった}!", v_orbit_change, point=True, word="ジャーン!"),
    C("しかも、この変化は、科学者の予想よりも、大きかったんです。", "変化は\n{予想より大きかった}", v_predict),
    C("なぜ、予想以上に動いたのか。まだ、だれにも分かっていません。", "なぜ?\n{まだ分からない}", v_why, mood="wow"),
    C("ひとつの考えは、飛び散ったちりの、反動です。", "ひとつの考えは\n{ちりの反動}", v_recoil),
    C("ちりが、うしろに、たくさん飛び出したので、その反動で、ロケットみたいに、さらに押されたのでは、というんです。", "ロケットみたいに\n{さらに押された}!?", v_recoil, point=True, word="ギュイーン"),
    C("クレーターができたのか。形が変わったのか。中身は、かたい岩なのか、すかすかなのか。", "クレーター?形?\n{中身は?}", v_why),
    C("それを、近くで確かめるのが、ヘラの仕事なんです!", "確かめるのが\n{ヘラの仕事}!", v_detective, point=True),

    # ---- ch4 journey
    C("ヘラが出発したのは、二千二十四年十月。大きさは、小さな車くらいです。", "出発は\n{2024年10月}", v_launch, **CH(5, "探偵ヘラの長い旅")),
    C("旅のとちゅう、二千二十五年三月には、火星のそばを通って、スピードをもらいました。", "火星の重力で\n{スピードアップ}!", v_mars),
    C("そのとき、ついでに、火星の小さな月、ダイモスの写真も、撮っています。", "ついでに火星の月\n{ダイモス}も撮影!", v_mars, word="キラーン"),
    C("火星の月の、裏側を、近くから撮った写真は、とてもめずらしいんです。", "めずらしい\n{月の裏側}!", v_mars),
    C("この作戦がうまくいって、予定より、一か月も早く、到着したんです!", "予定より\n{1か月早く}到着!", v_early, point=True, word="キラーン"),
    C("いま、ヘラがいるのは、地球から、約一億九千六百五十万キロ。", "地球から\n{約1億9650万km}", v_far),
    C("あまりに遠いので、地球と話せるのは、一日に、八時間くらいだけです。", "地球と話せるのは\n{1日8時間}ほど", v_far),

    C("電波が、ヘラから地球に届くまで、十分以上かかります。だから、ヘラは、自分で考えて、動く力も、もっているんです。", "電波は片道{10分以上}\n自分で考えて動く!", v_far, point=True),
    # ---- ch5 weird orbit
    C("ここで、ヘラの、ちょっと変わった飛び方を、しょうかいします。", "ヘラの\n{変わった飛び方}", v_rect_orbit, **CH(6, "長方形にまわる!?")),
    C("ふつう、探査機は、ぐるっと丸く回ります。でも、ヘラは、長方形に、回っているんです!", "丸じゃなく\n{長方形}に回る!", v_rect_orbit, point=True, word="ムムッ"),
    C("これが、ヨーロッパの宇宙機関が出した、本物の軌道の図。ほんとに、四角いでしょ?", "本物の軌道図も\n{ほんとに四角}!", P_square),
    C("理由は、小惑星の重力が、弱すぎるから。ディモルフォスの重力は、地球の、約二十万分の一。", "重力は\n{地球の20万分の1}", v_gravity, word="ヒュー"),
    C("ジャンプしたら、そのまま、宇宙に飛んでいきそうなくらい、弱いんです。", "ジャンプしたら\n{宇宙へ}飛んでいく!?", v_gravity, mood="wow"),
    C("だから、ヘラは、三日か四日ごとに、エンジンをふかして、九十度、向きを変えます。", "3〜4日ごとに\n{90度ターン}!", v_rect_orbit),
    C("回るスピードは、秒速十二センチ。カタツムリより、ちょっと速いくらいです。", "回る速さは\n{秒速12cm}", v_snail, point=True, word="ポヨン"),

    # ---- ch6 first photos
    C("さあ、いちばん気になる、ヘラの写真です。", "いちばん気になる\n{ヘラの写真}!", P_first, **CH(7, "写真でわかったこと")),
    C("十一月六日、二十八・五キロの近さから撮った、ディディモスがこちら!", "{28.5km}から\n撮ったディディモス!", P_didy, point=True, word="ワオ!"),
    C("チームの第一声は、わぁ、だったそうです!ダートが見られなかった、反対側が、写っていたんです。", "第一声は{わぁ!}\nダートが見てない反対側", P_didy_wide),
    C("大きな岩や、クレーター、みぞのような模様が、たくさんあります。", "岩・クレーター・\n{みぞ}がいっぱい", P_didy),
    C("赤道には、ぐるっと、山のようなでっぱり。たった二・二時間で、一回転する、速い回転で、できたと考えられています。", "{2.2時間}で1回転!\n赤道にでっぱり", v_ridge, point=True),
    C("さらに、びっくりニュース。なんと、ロックバンド、クイーンのギタリスト、ブライアン・メイさんが、この写真を、3Dにしました!", "クイーンの\n{ブライアン・メイ}が3Dに!", P_brian, point=True, word="ジャーン!"),
    C("じつは、ブライアン・メイさんは、天文学の博士で、ヘラのチームの、メンバーなんです!", "じつは{天文学の博士}で\nチームのメンバー!", P_brian),
    C("ヘラが、ぐるっと回りながら、少しずつ、ちがう角度で撮った、二枚の写真を、組み合わせたんです。", "ちがう角度の2枚を\n{組み合わせた}!", P_brian),
    C("赤と青のメガネで見ると、赤道のでっぱりが、くっきり、うかび上がります。", "赤青メガネで\n{立体に}見える!", P_brian),
    C("さらに、おもしろい説があります。この岩の一部は、体当たりで、ディモルフォスから飛ばされて、引っ越してきたかもしれない、というんです!", "岩が{お引っ越し}\nしたかも!?", v_transfer, point=True, word="ズバッ!"),
    C("ただし、これはまだ、ひとつの説。本当かどうかは、これから調べます。", "まだ{説}の段階\nこれから調べる", v_why),

    # ---- ch7 Japan + quiz
    C("じつは、このヘラには、日本も、参加しています。", "ヘラには\n{日本も参加}!", v_team, **CH(8, "日本も大活躍")),
    quiz("ここでクイズ!ヘラの温度カメラを作ったのは、どこの国?", "Q.温度カメラは\n{どこの国}?", Q2, 2),
    reveal("正解は、C!日本のジャクサです!", "正解は{C}!\n日本のJAXA!", Q2, 2),
    C("これが、その温度カメラの写真。赤いほど、あったかい場所です。", "温度カメラの写真\n{赤いほど暖かい}", P_tiri, point=True, word="ピカーッ"),
    C("ふつうのカメラでは、影になって見えない、ディモルフォスも、温度カメラなら、まるごと見えるんです!", "影のディモルフォスも\n{まるごと見える}!", P_tiri),
    C("温度の変わり方から、地面が、かたい岩か、すかすかか、砂かを、見分けます。", "温度で{岩か砂か}\nを見分ける!", v_thermal),
    C("同じしくみのカメラは、はやぶさ2にも、のっていて、小惑星リュウグウの岩が、すかすかだと、分かりました。", "{はやぶさ2}では\nリュウグウがすかすか", v_ryugu),
    C("さらに、別のカメラでは、二十五色に分けて、何でできているかを、調べています。", "{25色}に分けて\n成分を調べる", P_hsh),
    C("日本のカメラが、なぞを解く、大事なカギなんです!", "日本のカメラが\n{なぞのカギ}!", v_thermal, point=True),

    # ---- ch8 next
    C("では、ヘラはこれから、何をするのか。", "これから\n{何をする}?", v_question, **CH(9, "これからの予定")),
    C("まず、十一月二十五日に、ふたつの小惑星の、くわしい写真が、公開される予定です!", "11月25日\n{くわしい写真}公開!", v_calendar, point=True, word="ジャーン!"),
    C("その日は、ディモルフォスの、くわしい姿が、体当たりのあと、はじめて、近くから見られる日になります。", "体当たり後の姿が\n{はじめて近くで}!", v_calendar, point=True),
    C("来月からは、約二十キロまで、近づいて、くわしく調べます。", "来月は\n{約20km}まで接近", v_rect_orbit),
    C("さらに、くつ箱くらいの、小さな子機を、二台、送り出します。名前は、ユベンタスと、ミラニ。", "{くつ箱サイズ}の\n子機を2台!", P_cubesats),
    C("ユベンタスは、レーダーで、小惑星の中身を、のぞきます。ミラニは、まわりのちりを、調べます。", "レーダーで{中身}\nちりも{調べる}", v_cubesats),
    C("ユベンタスは、最後に、ディモルフォスへの、着陸にも、挑戦する予定です。", "子機も\n{着陸}に挑戦!", v_landing),
    C("ヘラの調査は、少なくとも、半年つづきます。", "調査は\n{少なくとも半年}", v_calendar),
    C("そして、最後には、ヘラ自身が、小惑星に、着陸に挑戦する予定です!", "最後は\n{着陸}に挑戦!", v_landing, point=True, word="ドーン!"),

    # ---- dream
    buildup(), openbox(),
    C("もし、いつか、本当に、地球にぶつかりそうな小惑星が、見つかったら。", "もし地球に\n{ぶつかりそうな}小惑星が…", v_shield, dream=True, word="ゴゴゴ"),
    C("探査機を、早めにぶつけて、通り道を、少しずらせば、地球を守れるかもしれません!", "早めにずらせば\n{地球を守れる}かも!", v_shield, dream=True, point=True, word="キラーン"),
    C("ダートとヘラは、そのための、世界ではじめての、本番の練習なんです。", "世界初の\n{地球防衛の練習}!", v_team, dream=True, point=True),
    C("そして、二千二十九年四月には、アポフィスという小惑星が、地球のすぐ近くを、通ります。", "2029年4月\n{アポフィス}が大接近!", v_shield, dream=True, word="ヒュー"),
    C("ぶつかる心配は、ありません。ヨーロッパは、次の探査機、ラムセスで、それを見に行く計画です。", "ぶつからない!\n次は{ラムセス}で見に行く", v_far, dream=True, point=True),
    C("アメリカと、ヨーロッパと、日本が、力を合わせて、地球を守る。ワクワクしますね!", "世界が力を合わせて\n{地球を守る}!", v_team, dream=True, point=True, word="ワクワク"),

    # ---- outro
    C("十一月二十五日の写真が出たら、またこのチャンネルで、しょうかいします!", "11/25の写真も\n{また紹介}します!", v_calendar, **CH(10, "まとめ")),
    C("今日のまとめ。四年前、人類は、小惑星を、本当に動かした。そして今、ヘラが、その現場を、調べはじめた!", "まとめ:人類は\n{小惑星を動かした}!", P_first, point=True),
    C("写真の、出典は、それぞれの写真の、下にのせています。くわしく知りたい人は、説明欄も見てね。", "写真の出典は\n{各写真の下と説明欄}", v_question),
    C("あなたなら、ヘラに、何を調べてほしい?", "ヘラに\n{何を調べてほしい}?", v_question),
    C("コメントで、教えてね!チャンネル登録も、よろしく!", "{コメント}と\n{チャンネル登録}よろしく!", v_comment, sfx=[(0.2, "kira")]),
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
    name = "20261121_hera_long"
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
