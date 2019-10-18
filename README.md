# MLのためのCI/CD パイプライン
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
- 自動化によって本番環境へのデプロイまでを効率化
- 機械学習における試行錯誤を記録、再現可能に
- 学習精度の表kあ、不具合のある学習モデルの誤ったデプロイを防止



## 考えたいポイント
- 前提としてモデリングチームはデプロイしてAPIを提供するところまで実施？
- master に対して機械学習コードの Pull Requet が走る。
  - 試行錯誤がなされる過程も全部 Pull Request に反映？
  - 試行錯誤のログがSageMakerの学習ジョブとプルリクに残る
- 評価が定量評価のみで自動化→これがベストだけどそうじゃないパターンも多い


## 手順
- Code Build のプロジェクトを作成する
  - Webhook の設定で イベントタイプで `PULL_REQUEST_CREATED` を選択   


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

