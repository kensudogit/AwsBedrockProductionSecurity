---
name: aws-bedrock-production-security
description: >
  Claude CodeでAmazon Bedrock・RAG・AIエージェントの本番向け認証認可、マルチテナント分離、IAM、監査、秘密管理、運用セキュリティを設計・実装・検証する。FastAPI、Next.js、AWS Cognito/OIDC、JWT、RAG権限フィルタ、エージェント承認フローに対応。既存aws-generative-ai-developer-proと併用する。
---
# AWS Bedrock Production Security

## 起動条件
ユーザーが「本番認証を実装」「Bedrockを安全に公開」「RAGの権限管理」「AIエージェントの承認」「IAM最小権限」「セキュリティレビュー」を依頼した場合に使用する。

## 必須ワークフロー
1. 既存の認証基盤（Cognito/他OIDC）、トークン形式、利用者/組織/ロール、AWSリージョン、データ分類、通信経路を確認。未確定事項は仮定として列挙し、秘密情報を要求しない。
2. `references/threat-model.md` を読み、脅威モデル・認証境界・テナント境界・外部副作用を設計する。
3. `references/aws-controls.md` に従いAWS側のIAM・ネットワーク・暗号化・監査・ログ・予算を設計する。
4. `templates/backend/` を基にJWTの署名/iss/aud/exp/token_use/scopeを検証し、リソース単位の認可を追加する。未認証は401、権限不足は403。トークン本文を信用する前に署名検証。
5. RAG検索時は検索側でtenant_idと文書ACLを必ず強制する。モデルへのプロンプトだけでアクセス制御しない。文書取り込み時のACLと検索側フィルタの整合性を確認する。
6. エージェントの外部書き込み・削除・送信・支払は、実行前のサーバー側認可・明示的承認・冪等性・監査を必須にする。
7. `references/verification.md` に沿って拒否系テスト、依存関係チェック、脆弱性チェック、負荷/障害時挙動を検証する。
8. 出力は変更ファイル、設計根拠、残余リスク、テスト結果、ロールバック、未完了事項を明示する。AWSへの実デプロイ・権限変更・課金操作はユーザーの明示確認を得る。

## 禁止事項
- APIキーやAWSアクセスキーをブラウザ、Git、ログに埋め込まない。
- JWTのverify_signature=False、固定共有シークレット、algorithmsをトークンから無制限採用しない。
- CORSワイルドカード+資格情報、デフォルト全許可、クライアント指定tenant_idでの認可をしない。
- Bedrockに送信する前のテナント分離を省略しない。
- PII/機密プロンプト全文のログ出力をデフォルトで行わない。
- 実装サンプルを監査済み・本番認証完成と宣言しない。

## 既存Skillとの併用
`aws-generative-ai-developer-pro` がある場合、Bedrock/RAG/Agentの機能実装を担当させ、本Skillで認証・認可・監査・セキュリティゲートを担当する。

## 依頼例
- 「aws-bedrock-production-securityを使いCognitoのアクセストークン認証をFastAPIに実装」
- 「RAGのテナント間情報漏洩を防ぐ検索フィルタを設計」
- 「Next.jsから安全にFastAPIへ接続する認証方式を比較」
- 「AIエージェントの外部メール送信に承認フローを追加」
- 「本番リリース前にセキュリティレビューして」
