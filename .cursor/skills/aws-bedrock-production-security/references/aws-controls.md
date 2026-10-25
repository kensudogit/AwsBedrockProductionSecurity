# AWS側セキュリティ実装ガイド

- Cognito User Poolsまたは適切なOIDC IdPを使用。ブラウザにはAuthorization Code + PKCE、必要に応じBFFのHttpOnly Secure SameSite Cookieを検討。CSRF対策を実装。
- FastAPIはアクセストークンのみ受理。CognitoではJWTの `client_id` と `token_use=access` を検証し、IDトークンをAPI認証に使わない。
- IAM実行ロールはBedrock `bedrock:InvokeModel` 等を必要なモデルARNに限定。ワイルドカード権限を避け、クロスリージョン推論プロファイル使用時は対象ARNを検証。
- AWS Secrets Manager / SSM Parameter Store、KMS、VPCエンドポイント、S3 Block Public Access、RDS暗号化、バックアップを用途に応じて設定。
- CloudTrail、CloudWatch、AWS Config、Security Hub、GuardDutyを運用要件に応じて設定。Bedrockの呼び出し記録はサービス固有のログ仕様を確認。
- WAF/レート制限/クォータ/タイムアウト/予算アラートを設定。アプリ側にも利用者別上限を設ける。
- RAGの文書ACLは取り込み時に正規化し、検索APIのサーバー側フィルタと後段の認可を両方実施。
- モデルへの入力・出力にPIIが含まれる可能性を評価し、保持・削除・監査要件を契約/運用で定義する。
- 権限変更はIaCでレビューし、CloudTrailと変更管理を整備する。

公式参照: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html
https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html
