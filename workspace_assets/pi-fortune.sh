#!/bin/bash
export PATH="/usr/games:$PATH"
export LANG=en_US.UTF-8
FORTUNES=(
    "今日の君は Agera 並みの瞬発力があるよっ！⚡️"
    "ラッキーアイテムは '1.1.1.1'！通信が安定しちゃうかも？📶"
    "お宝発見の予感！treasure_box をチェックしてみてっ🔎"
    "休憩も大事だよっ！s0u7a と Agera のクールダウンが必要かも☕️"
    "今日の冒険運は MAX！Sid の波を乗りこなそうっ🌊🚀"
)
/usr/games/cowsay -f kiss "${FORTUNES[$RANDOM % ${#FORTUNES[@]}]}" | /usr/games/lolcat -f
