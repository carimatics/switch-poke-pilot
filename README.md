# Switch Poke Pilot

![Screenshot](assets/images/screenshot.png)

Nintendo Switchのポケモンの操作を自動化するためのツールです。  
厳密にはポケモンだけでなく、それ以外のゲームも自動化することができます。

Windows、macOSで動作します。

Switch Poke Pilotは[Poke-Controller-Modified](https://github.com/Moi-poke/Poke-Controller-Modified)
を参考に作られています。  
すべてのコードを新規に実装し直していますが、どうしても似ている部分はあると思います。

また、このツールは鋭意開発中です。  
v1.0.0に到達するまでは後方互換性が保たれない可能性があります。  
v1.0.0までに実現したいことに関しては[ロードマップ](https://github.com/carimatics/switch-poke-pilot/wiki/ロードマップ)
をご覧ください。

## ドキュメント

[Wiki](https://github.com/carimatics/SwitchPokePilot/wiki)に詳しい情報を記載しています。  
このツールを利用する場合、[ユーザーガイド](https://github.com/carimatics/switch-poke-pilot/wiki/ユーザーガイド)
には目を通しておくことをおすすめします。

## 目的

Switch Poke Pilotの目的はNintendo Switchの自動化ツールとして、以下を達成することです。

- 導入が容易(未達)
    - 実行ファイルをダウンロードするだけで利用できるようにすることを目標としています
- APIが利用しやすい
    - 利用しやすいAPIで簡単にコマンドが作成できることを目標としています
- 機能の拡張がしやすい
    - 独自コマンド単位でディレクトリ1つ用意すると、それがコマンドとして認識されます
    - 独自コマンド単位の影響範囲が最小限で、かつ、共有も容易にできます
