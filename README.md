# dblec2018-eval

データベース工学の課題2（実用的なDBの構築と性能評価）


## 課題内容

講義ページを確認してください


## 使い方

1. MeCab（と辞書）をインストール

2. このパッケージをインストール（python3.6以上が必要です）

    ```bash
    $ git clone https://github.com/umemotsu/dblec2018-eval
    $ pip install -e ./dblec2018-eval
    ```

3. パッケージのCLIのヘルプを確認

    ```bash
    $ dblec2018-eval --help
    $ dblec2018-eval build-dataset --help
    ```

4. 開始URLとホップ数を指定してクローリング

    ```bash
    $ dblec2018-eval build-dataset <URL> <DEPTH> <PAGE_INDEX_FILE> <LINK_INDEX_FILE>
    ```
    
5. クロール結果を確認

    `PAGE_INDEX_FILE:`

    ```file:<PAGE_INDEX_FILE>
    URL_1<tab>TITLE_TOKEN_1<space>...<space>TITLE_TOKEN_L<tab>BODY_TOKEN_1<space>...<space>BODY_TOKEN_M
    URL_2<tab>...
    ...
    ```
    
    `LINK_INDEX_FILE:`

    ```file:<LINK_INDEX_FILE>
    SRC_URL_1<tab>DEST_URL_1<tab>ANCHOR_TOKEN_1<space>...<space>ANCHOR_TOKEN_N
    SRC_URL_1<tab>DEST_URL_2<tab>ANCHOR_TOKEN_1<space>...<space>ANCHOR_TOKEN_N'
    ...
    SRC_URL_2<tab>...
    ...
    ```

6. 各自が設計したテーブルに合わせて収集データを適当に加工・整形し，DBに挿入

7. インデックスの有無による性能（SQL実行時間）の差異を検証


## お願い

- 課題に取り組んでいる時にバグを見つけたら教えてください（Issueに投稿でもOK）
- 自分で解決した場合，どのようにしたかを教えてくれると助かります（Pull RequestでもOK）
