# Switch Poke Pilot

Nintendo Switchのポケモンの操作を自動化するためのツールです。  
厳密にはポケモンだけでなく、それ以外のゲームも自動化することができます。

このツールは[Poke-Controller-Modified](https://github.com/Moi-poke/Poke-Controller-Modified)を参考に作られています。  
すべてのコードを新規に実装し直していますが、どうしても似ている部分はあると思います。

## 特徴

Switch Poke Pilotの特徴は高い拡張性です。  
現状、Switch Poke Pilotがコア機能として提供しているものは、大きく2つだけです。

- Nintendo Switchのコントローラーとしての機能
- Nintendo Switchの画面をキャプチャする機能

これらの機能がAPIとして提供されており、ユーザーはこのAPIを利用することでNintendo Switchを自由に操作することができます。

### Nintendo Switchのコントローラーとしての機能

Nintendo Switchコントローラーの操作をエミュレートして、ゲーム操作をすることができます。  
ただし、ジャイロ機能、振動機能、NFC機能はサポートしていません。

例えば、以下のような操作ができます。

- Aボタン連打
- 複数手持ちを持った状態での学校最強大会周回

### Nintendo Switchの画面をキャプチャする機能

Nintendo Switchの画面をキャプチャして、画像認識(Template Matching)やスクリーンショットを保存できます。  
Template Matchingとは、画像の中から特定の画像を探し出す技術です。  
あらかじめ特定の画像を用意しておくと、その画像がゲーム画面内にあるかどうかを判定し、それに応じた処理ができるようになります。

画像認識の機能とコントローラーの機能を組み合わせることで、以下のような操作ができます。

- 戦闘の自動化
- ポケモン捕獲の自動化
- ポケモン厳選の自動化
- 孵化による色違い厳選

## (WIP)動作環境

(近いうちに最小限の導入手順をまとめます。
PyInstallerで実行ファイルに固めているので、それが配布できればハードウェアが動作するところまで準備できているとOKのはずです。)

ざっくりですが[Poke-Controller-Modified](https://github.com/Moi-poke/Poke-Controller-Modified)の導入ができていればこのツールも動くはずです。

- [Poke-Controller Guide](https://pokecontroller.info/)のハードウェアの導入まで完了している
  - それに加えて、Arduino等マイコンのセットアップやファームウェアの導入も完了していること

## 使い方

以下の2つができていれば、Switch Poke Pilotを使うことができます。

- ユーザー定義ファイルを配置する
- プログラムを実行する

### ユーザー定義ファイルの配置

1番簡単な方法は、[`examples`](https://github.com/carimatics/SwitchPokePilot/tree/main/examples)
ディレクトリの中身をホームディレクトリ(`~`)にコピーすることです。  
コピーすると以下のようなレイアウトになります。

```
~/
├── SwitchPokePilot
│   ├── config.json
│   ├── captures
│   ├── commands
│   ├── images
│   │   └── no_image_available.png
│   └── templates
│       └── game_freak_logo.png
└── SwitchPokePilot.config.json
```

### プログラムの実行

現状は開発環境を構築し、自前でアプリケーションの実行ファイルを作成する必要があります。  
詳しいやり方は開発環境構築の項目を参照してください。

## 開発環境構築

以下のコマンドを実行することで、開発環境を構築ができます。

```bash
# Git clone
$ git clone https://github.com/carimatics/SwitchPokePilot.git
$ cd SwitchPokePilot

# Pythonのインストール
$ pyenv install
$ pyenv rehash

# 依存ライブラリのインストール
$ make install
```

開発環境構築ができていると、以下のコマンドで`dist`ディレクトリ以下に実行ファイルが作成されます。

```bash
$ make pack
```
