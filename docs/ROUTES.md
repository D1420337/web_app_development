# 路由設計文件 (Route Design)

本文件定義「食譜收藏夾系統」的 API 路由與頁面規劃，包含使用者認證、食譜主要功能及管理員功能。

## 1. 路由總覽表格

| 模組 | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|---|
| 認證 | 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 認證 | 處理註冊 | POST | `/auth/register` | — | 接收表單存入DB，成功則重導向至登入頁 |
| 認證 | 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 認證 | 處理登入 | POST | `/auth/login` | — | 驗證帳密，成功設session重導向至首頁 |
| 認證 | 登出 | GET | `/auth/logout` | — | 清除session，重導向至首頁 |
| 食譜 | 首頁/食譜清單 | GET | `/` 或 `/recipes` | `index.html` | 顯示所有食譜縮圖或列表清單 |
| 食譜 | 搜尋食譜 | GET | `/recipes/search` | `index.html` | 依據 `?q=` 參數過濾並回傳食譜清單 |
| 食譜 | 新增食譜頁面 | GET | `/recipes/new` | `form.html` | 呈現空白的食譜輸入表單 |
| 食譜 | 處理新增 | POST | `/recipes/new` | — | 將表單資料存入DB，成功則重導向詳情頁 |
| 食譜 | 食譜詳細頁面 | GET | `/recipes/<id>` | `detail.html` | 呈現單一食譜畫面的詳細資料 |
| 食譜 | 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `form.html` | 呈現帶有原始資料的編輯表單 |
| 食譜 | 處理編輯 | POST | `/recipes/<id>/edit` | — | 更新特定食譜，成功重導向詳情頁 |
| 食譜 | 處理刪除 | POST | `/recipes/<id>/delete`| — | 刪除紀錄，成功重導向至首頁 |
| 管理 | 後台首頁 | GET | `/admin/` | `admin/dashboard.html` | (Nice-to-have) 呈現系統數據或首頁 |
| 管理 | 使用者管理 | GET | `/admin/users` | `admin/users.html` | (Nice-to-have) 管理平台上所有用戶 |

## 2. 每個路由的詳細說明

### 認證 (`app/routes/auth.py`)
- **GET `/auth/register`**：不需要輸入，無參數。直接渲染 `auth/register.html`。
- **POST `/auth/register`**：輸入為表單欄位 `username`, `password`。將呼叫 `User.create`。成功後重導向至登入頁。若失敗 (如帳號重複)，閃現(flash)錯誤訊息。
- **GET `/auth/login`**：不需要輸入。直接渲染 `auth/login.html`。
- **POST `/auth/login`**：輸入為 `username`, `password`。驗證 hash 後寫入 session。成功重導向首頁，失敗則閃現錯誤訊息。
- **GET `/auth/logout`**：呼叫 `session.clear()` 登出，並導回首頁。

### 食譜 (`app/routes/recipe.py`)
- **GET `/` 及 `/recipes`**：查詢並呼叫 `Recipe.get_all()`。輸出內容傳遞至 `index.html` 渲染。
- **GET `/recipes/search`**：接收 URL 參數 `q`。呼叫 `Recipe.search(q)`。回傳到 `index.html` 渲染搜尋結果。
- **GET `/recipes/new`**：需要登入。渲染 `form.html` (此表單沒有預先填值)。
- **POST `/recipes/new`**：需要登入。接收表單欄位 `title`, `description`, `ingredients`, `steps`, `image_url`。儲存至資料庫後將重新導向至 `/recipes/<id>`。
- **GET `/recipes/<id>`**：接收 `<int:id>` 參數。如果資料庫找不到，返回 HTTP 404 錯誤頁面。否則回傳帶有資料的 `detail.html`。
- **GET `/recipes/<id>/edit`**：需要等同於原作者的登入與權限檢查。接收 `<int:id>` 參數。回傳 `form.html` 且表單包含該食譜的所有資料供使用者更改。找不到返回 404 錯誤。
- **POST `/recipes/<id>/edit`**：更新該 ID 對應的資料實體，完成後帶出成功訊息並導回該食譜詳細頁面。
- **POST `/recipes/<id>/delete`**：自資料庫刪除紀錄並重導向首頁，執行前需確認權限與驗證使用者登入。

### 管理 (`app/routes/admin.py`) 
- **GET `/admin/` 與 `/admin/users`**：此功能模組需要自訂裝飾器驗證用戶是否已登入且有最高管理員權限 (例如檢查 `session` 與 `role == 'admin'`)。若無權限則回傳 HTTP 403 拒絕存取。

## 3. Jinja2 模板規劃清單

共用母版：
- `base.html`: 負責引入共用的 CSS / JS 外觀元件，包含網站導覽列 (Navbar) 選單、頁尾註腳 (Footer) 和錯誤訊息的呈現框 (Flash area)。

所有其他頁面皆透過 Jinja2 繼承 `base.html`，以達到一致性的呈現：
- `index.html` (適用於首頁、食譜分類列表、搜尋結果頁)
- `detail.html` (食譜詳細作法與食材的展示頁)
- `form.html` (共用於新增與編輯同一套輸入表單格式)
- `auth/login.html` (登入畫面專屬頁面)
- `auth/register.html` (註冊帳號專屬頁面)
- `admin/dashboard.html` (後台首頁 - 此為未來擴充預留)
- `admin/users.html` (後台會員名單頁 - 此為未來擴充預留)
