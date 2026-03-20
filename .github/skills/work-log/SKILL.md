---
name: work-log
description: Copilotエージェントが実装・変更作業を完了した後に必ず使う作業ログ記録スキル。ファイルの作成・編集・削除・コマンドの実行・テストの実行など、何らかのコード変更や実装を行ったときは毎回このスキルでdocs/work-logsにログを残すこと。「ログを残して」「作業記録して」「ログ取って」「作業履歴を残して」「変更記録して」と言われた場合も必ずこのスキルを使用する。単なる質問への回答のみで終わった場合（コードや設定ファイルを一切変更していない場合）は使用しない。
---

# 作業ログ記録スキル

## 目的

このスキルは、エージェントが何らかの実装・変更作業を完了した後に呼び出し、作業内容を **Markdown（人間可読）** と **JSON（機械可読）** の2形式で `docs/work-logs/` ディレクトリに記録する。

なぜこのログが重要か：コードレビュー・障害調査・監査で「誰が・何を・なぜ・どう変えたか」を後から追跡できるようになる。特に各ファイル変更の「変更理由（what/why/impact）」を記録することで、変更の意図が未来の開発者に伝わる。

---

## 手順

### 0. スキル読み込み直後に開始時刻を記録する（最初にやること）

スキルを読み込んだら**他の作業より先に**以下のコマンドで現在時刻を取得し、`timestamp_start` として記録しておく。

```powershell
# Windows (PowerShell)
Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
```
```bash
# Unix/macOS
date -u +"%Y-%m-%dT%H:%M:%S+00:00"
```

### 1. セッション情報を確定する

- **session_id**: 8文字のランダム英数字（例: `a3f8b2c1`）を生成する
- **timestamp_start**: 手順 0 で取得した値を使用する
- **model_version**: 使用中のモデル名（例: `claude-sonnet-4.6`）
- **user**: 以下のコマンドで取得する
  ```powershell
  # Windows
  $env:USERNAME
  ```
  ```bash
  # Unix/macOS
  whoami
  ```

### 2. 会話履歴を振り返り、作業内容を整理する

会話履歴・ツール呼び出し履歴から以下を整理する。

#### トリガー情報
- ユーザーの指示（プロンプト原文、または長い場合は要約）
- 対象リポジトリ名・ブランチ名（以下のコマンドで取得する）
  ```bash
  git rev-parse --abbrev-ref HEAD     # ブランチ名
  git remote get-url origin           # リポジトリ名（取得できない場合はディレクトリ名を使用）
  ```

#### 推論・アプローチ
- タスクサマリー（エージェントが理解した作業内容を1〜2文で）
- 採用したアプローチの説明
- 前提条件・仮定したこと（あれば）
- このセッションで使用したスキル（あれば）

#### アクション（最重要部分）

**変更ファイルごとに「変更理由（what/why/impact）」を記録する：**
- `what`: 何を変更したか（変更内容の説明）
- `why`: なぜ変更が必要だったか（ユーザー要求・バグ修正・リファクタリング等）
- `impact`: この変更が他のコンポーネントに与える影響

**実行したコマンドを全て記録する：**
- コマンド文字列・終了コード・出力の要約

**呼び出したスキルも記録する：**
- スキル名・目的・結果（成功/失敗）

### 3. テスト結果を記録する（テストを実行した場合のみ）

pytest 等のテスト実行結果を記録する：
- passed / failed / skipped の件数と実行時間

### 4. ログファイルを2つ生成する

**ログ生成の直前に**以下のコマンドで終了時刻を取得し、`timestamp_end` として記録する。

```powershell
# Windows (PowerShell)
Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
```
```bash
# Unix/macOS
date -u +"%Y-%m-%dT%H:%M:%S+00:00"
```

**ディレクトリ**: `docs/agent/work-logs/`（存在しない場合は作成する）

**ファイル名**: `YYYY-MM-DD_<session-id>` をベースに：
- `docs/agent/work-logs/YYYY-MM-DD_<session-id>.md` — Markdownログ
- `docs/agent/work-logs/YYYY-MM-DD_<session-id>.json` — JSONログ

フォーマットは下記のテンプレートに従う。

### 5. 完了を通知する

生成した2ファイルのパスをユーザーに伝える。

---

## Markdownログのフォーマット

```markdown
# 作業ログ: {YYYY-MM-DD HH:MM JST}

## セッション情報

| 項目 | 値 |
|------|-----|
| セッションID | {session_id} |
| エージェント | copilot-agent |
| モデル | {model_version} |
| ユーザー | {user または "不明"} |
| 開始 | {timestamp_start} |
| 終了 | {timestamp_end} |

## タスク概要

**プロンプト**: {ユーザーの指示}

**アプローチ**: {採用したアプローチの説明}

**前提条件**:
- {assumption_1}

## 実行したアクション

### 変更ファイル

| ファイル | 操作 | 変更行数 | 変更理由 |
|---------|------|---------|---------|
| `{path}` | {新規作成/編集/削除} | {+N / -N} | {why の要約} |

### 実行コマンド

```bash
# {コマンドの説明}
{command}
# 結果: exit_code={N}, {出力の要約}
```

### 呼び出したスキル

| スキル | 目的 | 結果 |
|--------|------|------|
| `{skill_name}` | {purpose} | ✅ 成功 / ❌ 失敗 |

## テスト結果

| 項目 | 値 |
|------|-----|
| passed | {N}件 |
| failed | {N}件 |
| skipped | {N}件 |
| 実行時間 | {N}秒 |

## 結果サマリー

- **ステータス**: ✅ 成功 / ⚠️ 部分成功 / ❌ 失敗
- **エラー**: {エラー内容 または "なし"}
- **警告**: {警告内容 または "なし"}
- **次のステップ**: {推奨される次のアクション（あれば）}
```

---

## JSONログのフォーマット

```json
{
  "log_version": "1.0",
  "session": {
    "id": "{session_id}",
    "agent_name": "copilot-agent",
    "model_version": "{model_version}",
    "user": "{user}",
    "timestamp_start": "{ISO8601}",
    "timestamp_end": "{ISO8601}",
    "duration_seconds": 0
  },
  "trigger": {
    "type": "prompt",
    "repository": "{repo_name}",
    "branch": "{branch_name}",
    "prompt": "{ユーザーの指示}"
  },
  "reasoning": {
    "task_summary": "{タスクの要約}",
    "approach": "{採用したアプローチ}",
    "assumptions": ["{assumption_1}"],
    "skills_used": ["{skill_name}"]
  },
  "files": {
    "modified": [
      {
        "path": "{file_path}",
        "lines_added": 0,
        "lines_removed": 0,
        "change_reason": {
          "what": "{何を変更したか}",
          "why": "{なぜ変更が必要だったか}",
          "impact": "{他コンポーネントへの影響}"
        }
      }
    ],
    "created": [],
    "deleted": []
  },
  "commands": [
    {
      "command": "{実行コマンド}",
      "exit_code": 0,
      "output_summary": "{出力の要約}"
    }
  ],
  "skills_invoked": [
    {
      "name": "{skill_name}",
      "purpose": "{呼び出し目的}",
      "result": "success"
    }
  ],
  "outcome": {
    "status": "success",
    "test_results": {
      "passed": 0,
      "failed": 0,
      "skipped": 0,
      "duration_seconds": 0
    },
    "errors": [],
    "warnings": [],
    "summary": "{作業結果の要約}"
  },
  "git": {
    "diff_stat": null,
    "commit_sha": null,
    "pr_url": null
  }
}
```

---

## 注意事項

- APIキー・パスワード・トークンなどの**機密情報はログに含めない**（発見した場合は `[REDACTED]` に置換する）
- プロンプトに個人情報が含まれる場合は要約に留める
- ログファイルはGitにコミットして問題ない内容にする
- テンプレートのプレースホルダー（`{...}`）は全て実際の値に置き換えること
- テストを実行していない場合はテスト結果セクション（JSONの `test_results`）を省略してよい
