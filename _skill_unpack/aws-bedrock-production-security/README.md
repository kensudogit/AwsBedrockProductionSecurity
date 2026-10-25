# AWS Bedrock Production Security Skill

Claude Code向け追加Skill。元の `aws-generative-ai-developer-pro` と併用可能です。

## インストール（Windows PowerShell）
解凍した `aws-bedrock-production-security` フォルダを `%USERPROFILE%\.claude\skills\` に配置してください。

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force '.\aws-bedrock-production-security' "$env:USERPROFILE\.claude\skills\"
```

Claude Codeを再起動し、`/aws-bedrock-production-security` または「aws-bedrock-production-securityを使って認証認可を実装して」と入力します。

## サンプルAPIの起動

```bash
cd templates/backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windowsではコピーコマンドを適宜変更
# .env の実際のCognito User Pool ID、App Client ID、リージョンを設定
uvicorn app:app --reload
```

サンプルは **署名検証・期限・発行者・Cognito access token のclient_id・token_use・scope・role** をチェックします。AWSやCognitoが未設定の状態ではアクセスを拒否します。実際のテナント権限はユーザープロファイルDBで管理する設計に置き換えてください。

## 本番導入時の必須作業
- Cognitoまたは既存OIDCとの連携を確定し、トークン発行/更新/ログアウトを実装
- API Gateway/WAF/ALBなどでTLS、レート制限、DDoS対策
- ユーザー・テナント・文書ACLを永続DBで管理し、検索時にも強制
- IAMロール、CloudTrail、CloudWatch、KMS、Secrets Manager、バックアップを環境別に設定
- 監査ログのPII対策、保持期限、インシデント対応、鍵ローテーション
- CI/CDでSAST、依存関係・コンテナスキャン、認可拒否系テスト

このリポジトリは **セキュアな実装雛形** であり、単体で本番完成品ではありません。
