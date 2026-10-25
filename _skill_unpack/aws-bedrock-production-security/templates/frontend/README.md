# Next.js連携方針

- 推奨: Cognito/OIDC Authorization Code + PKCE とBFFパターン。ブラウザからBedrockやAWS SDKを直接呼ばない。
- BFFでセッションをHttpOnly/Secure/SameSite Cookieに保存する場合、CSRF対策とセッション失効を実装する。
- FastAPIへはサーバー側から検証済みアクセストークンを渡す。IDトークンをAPI認証に流用しない。
- tenant_idやroleをブラウザの入力から信頼せず、サーバー側のDBと認証主体から解決する。
- CORS許可元は本番の固定オリジンに限定する。
- このフォルダは設計ガイドであり、Next.js認証実装そのものは利用IdP・ホスティング構成確定後に生成する。
