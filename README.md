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

### Nox 工作流（Day 8）
Nox 負責把測試與檢查流程編排成可重複執行的任務：
- `tests-3.11`、`tests-3.12`：執行測試（目前設定為重用 Hatch 環境，方便在無網路時執行）
- `lint`：`black --check`、`ruff check .`、`mypy src/`

執行全部 session：
```
hatch run ci
```

如需真正跨 Python 版本矩陣測試，可將 noxfile.py 改為建立獨立 venv 並指定 `python=["3.11", "3.12"]`，同時在系統安裝對應直譯器（例如透過 pyenv）。

---

### pre-commit（程式碼風格把關）
已內建於 dev 依賴，並透過本機 hooks 直接呼叫 Hatch scripts：

`.pre-commit-config.yaml` 會執行：
- `hatch run fmt`（black .、ruff check --fix .）
- `hatch run check`（black --check .、ruff check .）

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
├─ noxfile.py                # Nox 工作流（tests-3.11 / tests-3.12 / lint）
├─ src/
│  └─ demo_app/
│     ├─ __about__.py        # 動態版本來源 __version__
│     ├─ __init__.py
│     └─ main.py             # 範例主程式（hatch run start）
└─ tests/
   ├─ __init__.py
   └─ test_main.py           # 測試 main() 回傳 0
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

---

### 授權（License）
本專案以 MIT 授權條款釋出，詳見 `LICENSE.txt`。
