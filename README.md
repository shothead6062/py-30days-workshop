## 30 天 Python 專案工坊：環境、結構、測試到部署全打通

這個倉庫是系列文章「30 天 Python 專案工坊」的範例專案。從 Day 1 的工程化動機、Day 2～7 的環境與依賴策略、到 Day 8 的一鍵化工作流（Hatch scripts × Nox），都在此專案中串接演示。

核心目標：提供一個可直接上手的工程化骨架，讓你與團隊用一致的方式啟動、測試、檢查與打包發佈。

---

### 需求（Requirements）
- Python 3.11～3.12（建議 3.12）
- Hatch 1.14+（環境與腳本管理）

---

### 快速開始（Quick Start）
1) 進入開發環境（第一次會自動建立虛擬環境並安裝依賴）
```
hatch shell
```

2) 執行範例應用（會印出 Hello World 並回傳 0）
```
hatch run start
```

3) 常用一鍵指令（Hatch scripts）
- 測試：`hatch run test`
- Lint：`hatch run lint`
- 格式化：`hatch run format`
- 型別檢查：`hatch run typecheck`
- 總檢（black --check → ruff check → mypy → pytest）：`hatch run check-all`
- CI 一鍵（Nox）：`hatch run ci`

---

### 實際執行指南（How to Run）
- 進入環境：`hatch shell`
- 執行應用：`hatch run start`
- 單元測試：`hatch run test`
- 風格自動修正：`hatch run fmt`
- 僅檢查（CI 友好）：`hatch run check`
- 型別檢查（Pyright + mypy）：`hatch run typecheck`
- 契約測試（Pydantic 邊界）：`hatch run contracts`
- 一鍵 CI（Nox 全部 session）：`hatch run ci`

常見情境
- 只跑合約測試：`pytest -q tests/contracts`
- 只跑 3.12 測試：`nox -s tests-3.12`（或 `hatch run ci` 跑全部）
- 本地全自動修：`nox -s fmt`（Ruff 修正 → Black 排版）

---

### Nox 工作流（Day 8–10）
Nox 負責把測試與檢查流程編排成可重複執行的任務：
- `tests-3.11`、`tests-3.12`：執行測試（目前設定為重用 Hatch 環境，方便在無網路時執行）
- `lint`：`black --check`、`ruff check .`、`mypy src/`
- `typecheck`（Day 10）：`pyright .`、`mypy .`
- `contracts`（Day 10）：`pytest -q tests/contracts`

執行全部 session：
```
hatch run ci
```

如需真正跨 Python 版本矩陣測試，可將 noxfile.py 改為建立獨立 venv 並指定 `python=["3.11", "3.12"]`，同時在系統安裝對應直譯器（例如透過 pyenv）。

---

### 型別檢查與資料契約（Day 10）
本機與 CI 一致的型別與契約檢查：

- 本機（Hatch）
  - `hatch run typecheck`（pyright + mypy）
  - `hatch run test`（包含 contracts 測試 `tests/contracts/`）
- Nox（CI）
  - `hatch run ci` 會一併執行 `typecheck` 與 `contracts` sessions

---

### pre-commit（程式碼風格與型別把關）
已內建於 dev 依賴，並透過本機 hooks 直接呼叫 Hatch scripts：

`.pre-commit-config.yaml` 會執行：
- `hatch run fmt`（black .、ruff check --fix .）
- `hatch run check`（black --check .、ruff check .）
- `hatch run typecheck`（basedpyright .、mypy .）

啟用方式：
```
hatch run pre-commit-install
hatch run pre-commit-run   # 對所有檔案跑一次
```

之後每次 `git commit`，pre-commit 都會在你的 Hatch 環境中自動檢查與修正。

---

### 專案結構（Project Structure）
```
./
├─ pyproject.toml            # 專案設定、依賴、Hatch scripts
├─ noxfile.py                # Nox 工作流（fmt/style/lint/typecheck/contracts/tests-3.11/3.12）
├─ src/
│  └─ demo_app/
│     ├─ __about__.py        # 動態版本來源 __version__
│     ├─ __init__.py
│     ├─ main.py             # 範例主程式（hatch run start）
│     ├─ contracts.py        # Pydantic v2 契約（User/PasswordPair、validate_user）
│     ├─ cli_args.py         # CLI 參數解析 → Pydantic 驗證
│     └─ settings.py         # pydantic-settings：讀取 APP_* 環境變數
└─ tests/
   ├─ __init__.py
   ├─ test_main.py           # 測試 main() 回傳 0
   └─ contracts/             # 契約與邊界測試
      ├─ test_contracts.py   # User 驗證成功/失敗案例
      ├─ test_cli_args.py    # CLI 參數邊界驗證
      ├─ test_settings.py    # 環境變數設定驗證
      └─ test_typeadapter.py # TypeAdapter 範例
```

---

### 打包與發佈（Build & Publish）
使用 Hatchling 打包，Wheel packages 來源為 `src/demo_app`：
```
hatch build
```
產物會輸出至 `dist/`。若要發佈至 PyPI，可另行配置發布流程。

---

### 疑難排解（Troubleshooting）
- `hatch shell` 失敗：
  - 確認 Python 版本符合 `>=3.11,<3.13`
  - 移除舊環境後重試：`hatch env remove default && hatch shell`
- Nox 找不到 Python 版本：
  - 目前範例已改為重用 Hatch 環境（`venv_backend="none"`），避免安裝流程受網路影響。
  - 若改回多版本矩陣，需安裝對應直譯器並確保可安裝依賴。
- IDE 顯示「無法解析匯入」：
  - 讓 IDE Interpreter 指向 `hatch run python -c "import sys; print(sys.executable)"` 的路徑。
  - 或改在 CLI 驗證：`hatch run pyright .`、`hatch run mypy src/`。

---

### 授權（License）
本專案以 MIT 授權條款釋出，詳見 `LICENSE.txt`。
