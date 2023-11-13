# Switch Poke Pilot

Nintendo Switchのポケモンの操作を自動化するためのツールです。  
厳密にはポケモンだけでなく、それ以外のゲームも自動化することができます。

Switch Poke Pilotは[Poke-Controller-Modified](https://github.com/Moi-poke/Poke-Controller-Modified)
を参考に作られています。  
すべてのコードを新規に実装し直していますが、どうしても似ている部分はあると思います。

また、このツールは鋭意開発中です。  
v1.0.0に到達するまでは後方互換性が保たれない可能性があります。

## ドキュメント

[Wiki](https://github.com/carimatics/SwitchPokePilot/wiki)に詳しい情報を記載しています。

## 特徴

Switch Poke Pilotの特徴は高い拡張性です。  
現状、Switch Poke Pilotがコア機能として提供しているものは、大きく2つだけです。

- Nintendo Switchのコントローラーとしての機能
- Nintendo Switchの画面をキャプチャする機能

これらの機能がAPIとして提供されており、ユーザーはこのAPIを利用することで独自のコマンドを作成し、Nintendo
Switchを自由に操作することができます。
