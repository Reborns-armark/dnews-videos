# 作品「水が上がってくる世界」(縦型10秒・3D粘土・12fps・120フレーム)
1080x1920。water_render.py を `F_START=1 F_END=10 OUT_DIR=/tmp/out python3 water_render.py` で実行(pip install --break-system-packages bpy 後)。
- フレーム担当は各自の範囲のみレンダリングし、PNGを water3d/frames/ に push(ブランチ work-water3d)。
- 音は water3d/audio/ に wav(44.1kHz stereo)を push。
ストーリー: 1-21 寝てる粘土くんの周りに水たまり→22-32 目が覚めて驚く→33-70 木箱を積んで水位から逃げる→71-100 水が上がり木箱の塔の上で震える→101-120 引きで全景。
タイミング(12fps): f24=目を見開く, f40/48/56/64=木箱が出現して粘土くんが跳ぶ(各 +/-2フレームで着地), f68-84=震える/ドヤ, f100 水位が最大。
