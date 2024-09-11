# better-deploy-sample

GitHub の Actions や Releases 機能をうまく使って、ステージング環境と本番環境にデプロイするための CI 練習

## 実装要件

ここでは簡易的に、商品の価格を調べる API を想定したものを作る。

## CD

### 本番環境へのデプロイ

### テスト環境へのデプロイ

## CI

### PyTest

すべてのブランチに対して、変更があったときに PyTest が実行されるようになっています。テストコードは`./tests`にまとめられています。

### Dependabot / CodeQL

Dependabot でバージョン更新を、CodeQL でコードの品質管理を行っています。GitHub 標準のものを使っています。
