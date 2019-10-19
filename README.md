# SageMaker による ML のための CI/CD パイプライン
## 機械学習のコードの管理
- 機械学習モデル開発は試行錯誤を伴う
  - モデルそのもの
  - ハイパーパラメータ(設定ファイル)
  - 学習/検証データ(設定ファイル?やっぱりデータのバージョニングが鬼門)

## 実行環境・テスト環境の統一
- データや機械学習フレームワークがもろもろ
- 何をテストする？
  - 機械学習モデルとしてのテスト？
  - 機械学習システムとしてのテスト？

## モデルの管理
- 機械学習のモデルはコード・ハイパラ・データで管理

## エンドポイントの管理
- エンドポイントもモデルとコードで管理
- デプロイ先のアプリケーションのアーキテクチャの変更よりも早いサイクルで変更される可能性がある、疎結合

## CI/CD パイプラインの目的
- モデル改善のための試行錯誤と、データドリフトへ対応するための再学習の過程は対応するパイプラインも異なる？
  - PoC時の試行錯誤は複数のモデル学習を並行に行って、精度(単一指標じゃない場合も)を比較することがあるため、学習後にすぐにデプロイすることはない
- 自動化によって本番環境へのデプロイまでを効率化
- 機械学習における試行錯誤を記録、再現可能に
- 学習精度の評価、不具合のある学習モデルの誤ったデプロイを防止

## CI/CD でやること
- モデルデプロイの半自動化: データサイエンティスト→エンジニアのトランザクションの負担削減
- モデル精度確認

## Code Series
### CodeCommit
- SSH or HTTPS でセキュア
- Git オブジェクトは S3 で管理
- Git インデックスは DynamoDB で管理
- 暗号化キーは KMS で管理
- blobサイズ、メタデータは6MB以下、単一ファイルは2GBまで

### CodeBuild
- Build は基本的にコンパイル済バイナルを要求する言語が対象
- ソースコードのダウンロード
- buildspecで構成されたコマンドを実行
- 生成されたアーティファクトをS3バケットへアップロード
- 

```
aws codecommit create-reposigory
```


## 手順
- CodeCommit の準備をする
  - IAMでGitユーザー名とパスワードを生成する
  - git reposigoryを作る
- 本gitリポジトリをローカルにクローン
- CodeCommit へプッシュ

- 学習用のCode Build のプロジェクトを作成する
  - `Github` ならば `GitHub アカウントのリポジトリ` を選択
  - Webhook の設定で イベントタイプで `プッシュ` を選択
- デプロイ用のCode Build のプロジェクトを作成する
  - `Github` ならば `GitHub アカウントのリポジトリ` を選択
  - Webhook の設定で イベントタイプで `プッシュ` を選択
- 本リポジトリをクローン
- `train` ブランチの作成とcheckout 
- コードを改変しプッシュ
- 学習がされ、精度が良ければ `master` へプルリク

## モデルのデプロイ
- A/Bテスト
- カナリア
- Blue/Green など


## データの準備

データのダウンロード
```bash
aws s3 cp --recursive s3://floor28/data/cifar10 ./data
```

`S3` へのデータのアップロード
```python 
import os
import numpy as np
import boto3
import sagemaker
from sagemaker import get_execution_role

sagemaker_session = sagemaker.Session()
role = get_execution_role()
bucket='sagemaker-cicd'

dataset_location = sagemaker_session.upload_data(path='data', bucket=bucket, key_prefix='data/DEMO-cifar10')
```

