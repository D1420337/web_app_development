# 二手書交換平台系統 - 路由與頁面規劃文件 (Routes Design)

## 1. 路由總覽表格

| 功能模組 | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Auth** | 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| **Auth** | 處理註冊 | POST | `/auth/register` | — | 接收表單，寫入 User，重導向至登入 |
| **Auth** | 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| **Auth** | 處理登入 | POST | `/auth/login` | — | 驗證帳密，設定 Session，重導向至首頁 |
| **Auth** | 登出 | GET | `/auth/logout` | — | 清除 Session，重導向至首頁 |
| **Book** | 首頁/書籍列表 | GET | `/` | `templates/book/index.html` | 顯示所有上架書籍列表，支援搜尋與分類 |
| **Book** | 新增書籍頁面 | GET | `/book/create` | `templates/book/create.html` | 顯示上架二手書表單 |
| **Book** | 建立書籍 | POST | `/book/create` | — | 接收表單，寫入 Book，重導向至個人書櫃 |
| **Book** | 書籍詳情 | GET | `/book/<id>` | `templates/book/detail.html` | 顯示單筆書籍詳細資訊與公開留言 |
| **Book** | 編輯書籍頁面 | GET | `/book/<id>/edit` | `templates/book/edit.html` | 顯示編輯表單 (僅限擁有者) |
| **Book** | 更新書籍 | POST | `/book/<id>/update` | — | 更新 Book 資訊，重導向至書籍詳情 |
| **Book** | 刪除書籍 | POST | `/book/<id>/delete` | — | 刪除 Book，重導向至個人書櫃 |
| **User** | 個人書櫃(Dashboard) | GET | `/user/dashboard` | `templates/user/dashboard.html` | 顯示我的上架、預約狀態 |
| **Request** | 發送預約請求 | POST | `/book/<id>/request` | — | 買家點擊預約，寫入 Request |
| **Request** | 處理預約請求 | POST | `/request/<id>/action` | — | 賣家接受或拒絕，更新 Request 狀態 |
| **Message**| 新增留言 | POST | `/book/<id>/message` | — | 寫入公開留言 |
| **Message**| 私訊對話頁面 | GET | `/message/<user_id>` | `templates/user/messages.html` | 顯示與特定使用者的私訊紀錄 |
| **Message**| 傳送私訊 | POST | `/message/<user_id>/send` | — | 寫入私訊，重導向回對話頁面 |

## 2. 每個路由的詳細說明

*(這裡簡述幾個核心路由的邏輯，詳細可參考程式碼註解)*

### `/book/create` (POST)
- **輸入**：表單欄位 (`title`, `author`, `course_name`, `department`, `condition`, `price`)
- **處理邏輯**：
  1. 檢查使用者是否已登入 (Session)。
  2. 驗證必填欄位。
  3. 呼叫 `Book.create()` 寫入資料庫。
- **輸出**：`flash` 成功訊息，`redirect` 到 `/user/dashboard`。
- **錯誤處理**：資料驗證失敗則 `flash` 錯誤，重新 `render_template` `book/create.html` 並保留輸入值。

### `/book/<id>` (GET)
- **輸入**：URL 參數 `book_id`
- **處理邏輯**：
  1. 呼叫 `Book.get_by_id()`。
  2. 呼叫 `Message.get_by_book()` 取得該書留言。
  3. 呼叫 `User.get_by_id()` 取得賣家資訊。
- **輸出**：`render_template` `book/detail.html` 並傳遞變數。
- **錯誤處理**：若書本不存在，回傳 404 頁面。

### `/request/<id>/action` (POST)
- **輸入**：表單隱藏欄位 `action` (accept 或 reject)
- **處理邏輯**：
  1. 檢查目前登入者是否為該書的賣家。
  2. 呼叫 `Request.update_status()` 更新狀態。
  3. 若為 accept，同步更新書本狀態 (`Book.update_status()`) 為 reserved/sold。
- **輸出**：`redirect` 到 `/user/dashboard`。

## 3. Jinja2 模板清單

所有的模板都將繼承自 `base.html`，以保持網站 Navbar 與 Footer 一致。

- `templates/base.html`: 共用版型。
- `templates/auth/login.html`: 登入畫面。
- `templates/auth/register.html`: 註冊畫面。
- `templates/book/index.html`: 首頁，展示書籍卡片。
- `templates/book/detail.html`: 書籍專屬頁面，包含留言區與預約按鈕。
- `templates/book/create.html`: 上架書籍表單。
- `templates/book/edit.html`: 編輯書籍表單。
- `templates/user/dashboard.html`: 個人書櫃，使用頁籤 (Tabs) 切換「我的上架」、「我的預約」。
- `templates/user/messages.html`: 私訊聊天室介面。
