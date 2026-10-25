# 脅威モデル

| 脅威 | 必須対策 | 検証 |
|---|---|---|
| なりすまし | OIDC/JWT署名、iss、aud/client_id、exp、token_use | 偽署名/期限切れ/異issuerを401 |
| 権限昇格 | RBAC/ABACをサーバーで評価 | viewerの管理APIを403 |
| テナント越境 | DB RLSまたはtenant_idの強制クエリ + 文書ACL | 別tenantのIDを指定しても不取得 |
| プロンプトインジェクション | 取得文書を命令扱いしない、ツール実行許可リスト | 悪意ある文書で外部送信不可 |
| 情報漏洩 | ログ削減、暗号化、DLP、Guardrails | ログにトークン/本文なし |
| 過剰課金 | per-user quota、rate limit、timeout、予算アラーム | 429/上限超過の拒否 |
| エージェント誤操作 | human-in-the-loop、冪等キー、監査 | 承認なしの書き込み拒否 |

設計時に利用者・管理者・サービスアカウントの権限マトリクスを作る。
