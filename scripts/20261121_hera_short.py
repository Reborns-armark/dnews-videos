"""Short (vertical, ~45 s) for the Hera / DART story. Ends by pointing to the 8-minute long video."""
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=700, scale=0.74)

OPT = ["約3分", "約33分", "約3時間"]
CUTS = [
    eyes(Cut("人類は、宇宙で、小惑星に、わざと体当たりした!", "人類は小惑星に\n{わざと体当たり}!", v_hook_crash, capsize=100, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("相手は、東京タワーの、半分くらいの、小さな小惑星。", "相手は\n東京タワーの{半分}くらい", v_sizes, capsize=100),
    Cut("ダートは、秒速六・一キロで、突っ込んだ!", "{秒速6.1km}で\n突っ込んだ!", v_dart_fly, capsize=104, point=True, word="ギュイーン"),
    Cut("これが、その瞬間の、本物の写真!", "その瞬間の\n{本物の写真}!", P_plume, capsize=104, point=True, sfx=[(0.1, "kira")]),
    teaser(),
    Cut("ダートが最後に送った写真は、とちゅうで、ぷつっと切れてる!", "最後の写真は\n{とちゅうで切れた}!", P_dart_final, capsize=96, word="ガーン!"),
    Cut("ちりのしっぽは、一万キロ以上!", "ちりのしっぽが\n{1万km以上}!", P_hubble, capsize=104, word="ヒュー"),
    Cut("そして四年後、現場検証の探査機、ヘラが、ついに到着!", "4年後\n探査機{ヘラ}が到着!", P_first, capsize=100, point=True),
    quiz("クイズ!体当たりで、小惑星の一周は、どれくらい短くなった?", "Q.1周は\n{どれくらい短く}?", OPT, 1),
    reveal("正解は、B!約三十三分!", "正解は{B}!\n約33分!", OPT, 1),
    Cut("相手の小惑星は、二・二時間で、くるっと一回転!", "{2.2時間}で\n1回転!", v_ridge, capsize=104, word="グルグル"),
    Cut("ヘラは、重力が弱すぎて、なんと、長方形に回ってる!", "重力が弱すぎて\n{長方形}に回る!", v_rect_orbit, capsize=96, point=True, word="ムムッ"),
    Cut("ヘラが撮った写真には、ダートが見ていない、反対側が!", "ダートが見てない\n{反対側}が写った!", P_didy, capsize=96, point=True, word="ワオ!"),
    Cut("しかも、クイーンのギタリスト、ブライアン・メイさんが、3Dにした!", "クイーンの\n{ブライアン・メイ}が3Dに!", P_brian, capsize=96, point=True, word="ジャーン!"),
    buildup(), openbox(),
    Cut("温度カメラは、日本のジャクサ製!影の小惑星まで、まるごと見える!", "温度カメラは\n{日本のJAXA製}!", P_tiri, dream=True, capsize=96, point=True, word="ピカーッ"),
    Cut("いつか、地球にぶつかりそうな小惑星が来ても、ずらして守れるかも!", "いつか{地球を守れる}\nかも!", v_shield, dream=True, capsize=96, point=True, word="キラーン"),
    Cut("十一月二十五日には、くわしい写真も公開予定!", "11月25日に\n{くわしい写真}公開!", v_calendar, dream=True, capsize=96, point=True),
    Cut("続きは、八分のくわしい版で!チャンネルの、長い動画を見てね!", "続きは{8分のくわしい版}で!\nチャンネルの長い動画へ", v_longvideo, capsize=88, sfx=[(0.2, "kira")]),
]

if __name__ == "__main__":
    run("20261121_hera_short", CUTS, 43, "宇宙", "#7B5CFF", 0)
