# EP08 — Docker 與 DevOps 實戰

> **系列定位**：你會寫程式，但每次部署都是一場災難。本篇從零開始，
> 帶你掌握 Docker 容器化、Git 版本控制、CI/CD 自動化，以及完整的 DevOps 工作流程。

---

## 目錄

1. [為什麼需要 Docker](#1-為什麼需要-docker)
2. [Docker 基本指令](#2-docker-基本指令)
3. [Dockerfile 完全攻略](#3-dockerfile-完全攻略)
4. [Docker Compose](#4-docker-compose)
5. [Docker Volume 與資料持久化](#5-docker-volume-與資料持久化)
6. [Docker Network](#6-docker-network)
7. [Git 完全攻略](#7-git-完全攻略)
8. [CI/CD 概念與實戰](#8-cicd-概念與實戰)
9. [環境管理](#9-環境管理)
10. [Linux 基本指令（開發者必備）](#10-linux-基本指令開發者必備)
11. [雲端部署概覽](#11-雲端部署概覽)
12. [完整 DevOps 流程範例](#12-完整-devops-流程範例)

---

## 1. 為什麼需要 Docker

### 1.1 "It Works on My Machine" 問題

你一定遇過這種情境：

```
開發者 A：「我這邊跑得好好的啊？」
開發者 B：「我裝了相同的套件，但就是跑不起來。」
測試工程師：「部署到測試機後整個爛掉了。」
```

**根本原因**：每台電腦的作業系統版本、程式語言版本、系統函式庫、環境變數都不同。
即使「看起來一樣」，微小的差異就足以讓程式崩潰。

Docker 的解決方案：**把程式 + 所有依賴 + 作業系統環境，全部打包成一個標準化的容器**。
不管在哪台機器上跑，環境完全相同。

### 1.2 虛擬機 vs 容器

```
┌─────────────────────────────────────────────────────────┐
│                   傳統虛擬機 (VM)                         │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  App A   │  │  App B   │  │  App C   │              │
│  │  Libs    │  │  Libs    │  │  Libs    │              │
│  │ Guest OS │  │ Guest OS │  │ Guest OS │  ← 每個 VM   │
│  │ (2-3 GB) │  │ (2-3 GB) │  │ (2-3 GB) │    一整個 OS │
│  └──────────┘  └──────────┘  └──────────┘              │
│  ┌─────────────────────────────────────────┐            │
│  │          Hypervisor (VMware/VirtualBox)  │            │
│  └─────────────────────────────────────────┘            │
│  ┌─────────────────────────────────────────┐            │
│  │            Host OS (主機系統)             │            │
│  └─────────────────────────────────────────┘            │
│  ┌─────────────────────────────────────────┐            │
│  │               硬體 (Hardware)            │            │
│  └─────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Docker 容器                           │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  App A   │  │  App B   │  │  App C   │              │
│  │  Libs    │  │  Libs    │  │  Libs    │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│  ┌─────────────────────────────────────────┐            │
│  │          Docker Engine                   │ ← 共用     │
│  └─────────────────────────────────────────┘   主機核心  │
│  ┌─────────────────────────────────────────┐            │
│  │            Host OS (主機系統)             │            │
│  └─────────────────────────────────────────┘            │
│  ┌─────────────────────────────────────────┐            │
│  │               硬體 (Hardware)            │            │
│  └─────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

| 比較項目       | 虛擬機 (VM)          | 容器 (Container)       |
|--------------|---------------------|----------------------|
| 啟動時間       | 分鐘級               | 秒級                  |
| 映像檔大小     | GB 等級              | MB 等級               |
| 資源消耗       | 高（完整 OS）         | 低（共用核心）          |
| 隔離程度       | 完全隔離              | 程序級隔離             |
| 適用場景       | 需要不同 OS           | 相同 OS 下跑多服務      |

### 1.3 Docker 核心概念

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Dockerfile ──(build)──> Image ──(run)──> Container │
│       │                     │                   │    │
│    建置藍圖              唯讀模板           執行中實例  │
│    （原始碼）           （安裝好的光碟）     （開機的電腦）│
│                            │                         │
│                      Registry (Docker Hub)           │
│                     （光碟倉庫，可上傳/下載）           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

- **Image（映像檔）**：唯讀的模板，包含 OS + 程式 + 依賴。像是一張安裝好的光碟。
- **Container（容器）**：Image 的執行實例。像是用那張光碟開機的電腦，可以有多台。
- **Dockerfile**：建置 Image 的腳本。寫好步驟，Docker 自動幫你打包。
- **Registry**：存放 Image 的倉庫。Docker Hub 是最大的公開 Registry。

### 1.4 安裝 Docker

```bash
# === macOS ===
# 方法 1：官網下載 Docker Desktop
# https://www.docker.com/products/docker-desktop
# 下載後拖到 Applications 即可

# 方法 2：用 Homebrew
brew install --cask docker

# === Ubuntu / Debian ===
# 移除舊版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 設定 Docker 官方 repository
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安裝 Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 讓當前使用者免 sudo 使用 docker
sudo usermod -aG docker $USER
newgrp docker

# === 驗證安裝 ===
docker --version
# Docker version 27.x.x, build xxxxxxx

docker run hello-world
# 看到 "Hello from Docker!" 表示安裝成功
```

---

## 2. Docker 基本指令

### 2.1 docker run — 建立並啟動容器

```bash
# 基本語法
docker run [選項] <映像檔名稱> [指令]

# --- 範例 1：最簡單的 run ---
docker run hello-world
# Input:   hello-world 映像檔（如果本地沒有，自動從 Docker Hub 下載）
# Process: 建立容器 → 執行預設指令 → 印出歡迎訊息
# Output:  Hello from Docker! 訊息，然後容器自動停止

# --- 範例 2：互動式執行 Ubuntu ---
docker run -it ubuntu bash
# -i : interactive（保持 STDIN 開啟）
# -t : tty（分配一個終端機）
# Input:   ubuntu 映像檔
# Process: 啟動 Ubuntu 容器，開啟 bash shell
# Output:  你會進入 Ubuntu 的命令列，可以執行 Linux 指令
# 離開方式：輸入 exit

# --- 範例 3：背景執行 Nginx 網頁伺服器 ---
docker run -d -p 8080:80 --name my-nginx nginx
# -d         : detach（背景執行）
# -p 8080:80 : 把主機的 8080 port 對應到容器的 80 port
# --name     : 幫容器取名字（不取的話 Docker 會隨機命名）
# Input:   nginx 映像檔
# Process: 在背景啟動 Nginx 容器
# Output:  印出容器 ID，瀏覽 http://localhost:8080 可看到 Nginx 預設頁面

# --- 範例 4：設定環境變數 ---
docker run -d \
  -p 3306:3306 \
  --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -e MYSQL_DATABASE=myapp \
  mysql:8.0
# -e : 設定環境變數
# Input:   mysql:8.0 映像檔（指定版本 8.0）
# Process: 啟動 MySQL，用環境變數設定 root 密碼和預設資料庫
# Output:  MySQL 容器在背景執行

# --- 範例 5：掛載本地目錄 ---
docker run -d \
  -p 8080:80 \
  --name my-web \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx
# -v : volume 掛載（主機路徑:容器路徑:權限）
# :ro = read-only（容器只能讀，不能寫）
# Input:   當前目錄下的 html 資料夾
# Process: 把本地的 html 資料夾掛載到 Nginx 的網頁目錄
# Output:  Nginx 會提供你的 html 檔案

# --- 範例 6：一次性執行後自動刪除 ---
docker run --rm python:3.12 python -c "print('Hello Docker!')"
# --rm : 容器停止後自動刪除
# Input:   python:3.12 映像檔
# Process: 執行一行 Python 指令
# Output:  印出 Hello Docker!，容器隨即被刪除
```

### 2.2 docker ps — 查看容器

```bash
# 查看正在執行的容器
docker ps
# CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
# a1b2c3d4e5f6   nginx   ...       2 min     Up 2m    80/tcp  my-nginx

# 查看所有容器（包含已停止的）
docker ps -a
# 會多出 STATUS 為 Exited 的容器

# 只顯示容器 ID
docker ps -q
# a1b2c3d4e5f6

# 格式化輸出
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
# ID             NAMES      STATUS    PORTS
# a1b2c3d4e5f6   my-nginx   Up 2m     0.0.0.0:8080->80/tcp
```

### 2.3 docker images — 查看映像檔

```bash
# 列出所有本地映像檔
docker images
# REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
# nginx        latest    a1b2c3d4e5f6   2 days ago    187MB
# python       3.12      b2c3d4e5f6a7   3 days ago    1.02GB
# ubuntu       latest    c3d4e5f6a7b8   5 days ago    77.8MB

# 篩選特定映像檔
docker images python
# 只顯示 python 相關的映像檔

# 查看映像檔詳細資訊
docker inspect nginx
# 輸出完整的 JSON 格式映像檔資訊
```

### 2.4 docker stop / docker rm / docker rmi — 停止與刪除

```bash
# --- 停止容器 ---
docker stop my-nginx
# Input:   容器名稱或 ID
# Process: 發送 SIGTERM 信號，等 10 秒後強制 SIGKILL
# Output:  容器停止（STATUS 變成 Exited）

# 停止所有執行中的容器
docker stop $(docker ps -q)

# --- 刪除容器 ---
docker rm my-nginx
# Input:   已停止的容器名稱或 ID
# Process: 刪除容器（必須先 stop）
# Output:  容器被移除

# 強制刪除（不用先 stop）
docker rm -f my-nginx

# 刪除所有已停止的容器
docker container prune
# 會問你 "Are you sure?" 輸入 y 確認

# --- 刪除映像檔 ---
docker rmi nginx
# Input:   映像檔名稱或 ID
# Process: 刪除本地映像檔（不影響 Docker Hub 上的）
# Output:  映像檔被移除，釋放硬碟空間

# 刪除所有未使用的映像檔
docker image prune -a
```

### 2.5 docker exec — 進入執行中的容器

```bash
# 進入正在執行的容器的 bash
docker exec -it my-nginx bash
# -i : interactive
# -t : tty
# Input:   容器名稱 + 要執行的指令
# Process: 在容器內開啟一個 bash session
# Output:  你進入容器內部，可以執行指令

# 不進入容器，直接執行一個指令
docker exec my-nginx cat /etc/nginx/nginx.conf
# Input:   容器名稱 + 指令
# Process: 在容器內執行 cat，讀取 Nginx 設定檔
# Output:  印出檔案內容到你的終端機

# 以 root 身份進入
docker exec -it -u root my-nginx bash
```

### 2.6 docker logs — 查看容器日誌

```bash
# 查看容器的全部日誌
docker logs my-nginx
# Input:   容器名稱
# Output:  該容器的所有 stdout/stderr 輸出

# 即時追蹤日誌（類似 tail -f）
docker logs -f my-nginx
# -f : follow，持續輸出新日誌
# 按 Ctrl+C 停止追蹤

# 只看最後 50 行
docker logs --tail 50 my-nginx

# 顯示時間戳記
docker logs -t my-nginx

# 看特定時間之後的日誌
docker logs --since "2024-01-01T00:00:00" my-nginx
```

---

## 3. Dockerfile 完全攻略

### 3.1 Dockerfile 指令詳解

```dockerfile
# ======================================
# FROM — 指定基礎映像檔（必須是第一行）
# ======================================
FROM python:3.12-slim
# 使用 Python 3.12 的精簡版（只有基本功能，映像檔較小）
# 常見選擇：
#   python:3.12        完整版（約 1 GB）
#   python:3.12-slim   精簡版（約 150 MB）
#   python:3.12-alpine Alpine Linux 版（約 50 MB，但可能缺套件）

# ======================================
# WORKDIR — 設定工作目錄
# ======================================
WORKDIR /app
# 之後的指令都在 /app 目錄下執行
# 如果目錄不存在，會自動建立

# ======================================
# COPY — 複製檔案到映像檔內
# ======================================
COPY requirements.txt .
# 把本地的 requirements.txt 複製到容器的 /app/requirements.txt
# "." 代表當前 WORKDIR

COPY . .
# 把本地當前目錄的所有檔案複製到容器的 /app/

# ======================================
# ADD — 類似 COPY，但功能更多
# ======================================
ADD archive.tar.gz /app/
# ADD 會自動解壓縮 tar/gz/bz2 檔案
# ADD 也可以從 URL 下載檔案
# 建議：一般情況用 COPY，需要解壓才用 ADD

# ======================================
# RUN — 在建置時期執行指令
# ======================================
RUN pip install --no-cache-dir -r requirements.txt
# 建置映像檔時執行 pip install
# --no-cache-dir 不保留 pip 快取，減少映像檔大小
# 每個 RUN 會建立一個新的層（layer）

# 合併多個指令（減少層數，映像檔更小）
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# ======================================
# ENV — 設定環境變數
# ======================================
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
# 這些變數在容器執行時也會存在

# ======================================
# EXPOSE — 宣告容器要使用的 port
# ======================================
EXPOSE 5000
# 只是文件用途，告訴使用者此容器監聽 5000 port
# 實際開放 port 還是要在 docker run -p 指定

# ======================================
# CMD — 容器啟動時的預設指令
# ======================================
CMD ["python", "app.py"]
# exec 格式（推薦）：直接執行，接收系統信號
# 也可以用 shell 格式：CMD python app.py
# 一個 Dockerfile 只能有一個 CMD，後面的會覆蓋前面的
# docker run 時可以覆蓋 CMD

# ======================================
# ENTRYPOINT — 容器的進入點指令
# ======================================
ENTRYPOINT ["python"]
CMD ["app.py"]
# ENTRYPOINT 不會被 docker run 的指令覆蓋
# CMD 會成為 ENTRYPOINT 的預設參數
# docker run my-image          → 執行 python app.py
# docker run my-image test.py  → 執行 python test.py（CMD 被覆蓋）
```

### 3.2 .dockerignore

```
# .dockerignore — 告訴 Docker 建置時忽略哪些檔案

# 版本控制
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.venv
venv
env

# Node.js
node_modules
npm-debug.log

# IDE
.vscode
.idea
*.swp

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose.yml

# 測試與文件
tests/
docs/
README.md

# 環境檔
.env
.env.local
```

### 3.3 Python Flask 專案 Dockerfile（完整）

```dockerfile
# ============================================
# Python Flask App — 完整 Dockerfile
# ============================================

# 階段 1：建置階段
FROM python:3.12-slim AS builder

# 設定環境變數，避免 Python 產生 .pyc 和 buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（編譯某些 Python 套件需要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 先複製 requirements.txt（利用 Docker 層快取）
COPY requirements.txt .

# 安裝 Python 依賴到 /app/dependencies
RUN pip install --no-cache-dir --prefix=/app/dependencies -r requirements.txt

# 階段 2：執行階段
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安裝執行時需要的系統函式庫（不需要 gcc）
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# 建立非 root 使用者（安全性最佳實踐）
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 從 builder 階段複製已安裝的 Python 套件
COPY --from=builder /app/dependencies /usr/local

# 複製應用程式原始碼
COPY . .

# 設定檔案權限
RUN chown -R appuser:appuser /app

# 切換到非 root 使用者
USER appuser

# 宣告監聽 port
EXPOSE 5000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 啟動應用程式（使用 gunicorn 作為 production server）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

對應的 Flask 應用程式 `app.py`：

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello from Dockerized Flask!"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

對應的 `requirements.txt`：

```
flask==3.1.0
gunicorn==23.0.0
psycopg2-binary==2.9.10
```

建置與執行：

```bash
# 建置映像檔
docker build -t my-flask-app .
# -t : 為映像檔取名（tag）

# 執行容器
docker run -d -p 5000:5000 --name flask-server my-flask-app

# 測試
curl http://localhost:5000
# {"message": "Hello from Dockerized Flask!"}
```

### 3.4 Node.js Express 專案 Dockerfile（完整）

```dockerfile
# ============================================
# Node.js Express App — 完整 Dockerfile
# ============================================

# 階段 1：安裝依賴
FROM node:20-slim AS dependencies

WORKDIR /app

# 先複製 package 檔案（利用 Docker 層快取）
COPY package.json package-lock.json ./

# 只安裝 production 依賴
RUN npm ci --only=production

# 階段 2：建置階段（如果有 TypeScript 或需要 build）
FROM node:20-slim AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# 複製原始碼並建置
COPY . .
RUN npm run build

# 階段 3：執行階段
FROM node:20-slim

# 安裝 dumb-init（正確處理 PID 1 信號）
RUN apt-get update && \
    apt-get install -y --no-install-recommends dumb-init curl && \
    rm -rf /var/lib/apt/lists/*

# 設定環境變數
ENV NODE_ENV=production
ENV PORT=3000

# 建立非 root 使用者
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 從 dependencies 階段複製 node_modules
COPY --from=dependencies /app/node_modules ./node_modules

# 從 builder 階段複製建置產出
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# 設定權限
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# 使用 dumb-init 作為 PID 1
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

### 3.5 C++ 專案 Dockerfile（多階段建置）

```dockerfile
# ============================================
# C++ 應用程式 — 多階段建置 Dockerfile
# ============================================

# 階段 1：建置階段（包含完整的編譯工具鏈）
FROM ubuntu:24.04 AS builder

# 安裝 C++ 建置工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libboost-all-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 複製原始碼
COPY CMakeLists.txt .
COPY src/ ./src/
COPY include/ ./include/

# 建置專案
RUN mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc)

# 階段 2：執行階段（只需要最小的執行環境）
FROM ubuntu:24.04

# 只安裝執行時需要的函式庫
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libboost-system1.83.0 \
        libboost-filesystem1.83.0 \
    && rm -rf /var/lib/apt/lists/*

# 建立非 root 使用者
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 從 builder 階段只複製編譯好的執行檔
COPY --from=builder /app/build/my_app .

RUN chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["./my_app"]

# 注意映像檔大小比較：
# builder 階段：約 1.5 GB（包含 gcc, cmake, header files...）
# 最終映像檔：約 100 MB（只有執行檔 + 必要的 .so 檔）
```

### 3.6 Go 專案 Dockerfile（超小映像檔）

```dockerfile
# ============================================
# Go 應用程式 — 超小 Docker Image
# ============================================

# 階段 1：建置階段
FROM golang:1.23-alpine AS builder

WORKDIR /app

# 先複製 go.mod/go.sum（利用層快取）
COPY go.mod go.sum ./
RUN go mod download

# 複製原始碼
COPY . .

# 靜態編譯（不依賴系統 C 函式庫）
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o server ./cmd/server

# 階段 2：使用 scratch（完全空白的映像檔）
FROM scratch

# 複製 SSL 憑證（如果需要 HTTPS 請求）
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# 複製執行檔
COPY --from=builder /app/server /server

EXPOSE 8080

ENTRYPOINT ["/server"]

# 最終映像檔大小：可能只有 5-15 MB
# 因為 scratch 是完全空的，只有我們放進去的執行檔
# Go 靜態編譯不需要任何系統函式庫
```

---

## 4. Docker Compose

### 4.1 什麼是 Docker Compose

當你的應用需要多個服務（Web server + Database + Cache），
用 `docker run` 一個一個啟動太麻煩。Docker Compose 讓你用一個 YAML 檔案定義所有服務，
一個指令全部啟動。

### 4.2 docker-compose.yml 語法完整解說

```yaml
# docker-compose.yml 完整語法範例

# 版本聲明（Compose V2 可省略，建議保留）
version: "3.9"

# ========================================
# services：定義所有服務（容器）
# ========================================
services:

  # --- 服務名稱 ---
  web:
    # 建置設定
    build:
      context: .                    # Dockerfile 所在目錄
      dockerfile: Dockerfile        # Dockerfile 檔名
      args:                         # 建置時的引數
        NODE_ENV: production

    # 或者直接用現有映像檔
    # image: nginx:latest

    # 容器名稱
    container_name: my-web-app

    # Port 對應（主機:容器）
    ports:
      - "8080:3000"                 # 主機 8080 → 容器 3000
      - "8443:3443"                 # 可以對應多個 port

    # 環境變數
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379

    # 或者從檔案讀取環境變數
    env_file:
      - .env

    # Volume 掛載
    volumes:
      - ./src:/app/src              # bind mount：本地目錄掛載
      - app-data:/app/data          # named volume：資料持久化
      - /app/node_modules           # anonymous volume：排除此目錄

    # 網路
    networks:
      - frontend
      - backend

    # 啟動依賴
    depends_on:
      db:
        condition: service_healthy  # 等 db 健康檢查通過才啟動
      cache:
        condition: service_started  # 等 cache 啟動即可

    # 重啟策略
    restart: unless-stopped
    # no          : 不自動重啟
    # always      : 總是重啟
    # on-failure  : 只在失敗時重啟
    # unless-stopped : 除非手動停止，否則都重啟

    # 健康檢查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s                 # 每 30 秒檢查一次
      timeout: 10s                  # 逾時 10 秒算失敗
      retries: 3                    # 連續 3 次失敗才標記為 unhealthy
      start_period: 40s             # 啟動後 40 秒才開始檢查

    # 資源限制
    deploy:
      resources:
        limits:
          cpus: "0.50"              # 最多用 50% CPU
          memory: 512M              # 最多用 512 MB 記憶體

# ========================================
# volumes：命名 volume
# ========================================
volumes:
  app-data:                         # 宣告一個 named volume
    driver: local                   # 使用本地驅動程式

# ========================================
# networks：自訂網路
# ========================================
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### 4.3 完整範例：Web App + Database + Redis

```yaml
# docker-compose.yml
# 完整的三服務架構：Flask App + PostgreSQL + Redis

version: "3.9"

services:
  # ============ Web 應用程式 ============
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: flask-web
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://appuser:secretpass@db:5432/appdb
      - REDIS_URL=redis://cache:6379/0
      - SECRET_KEY=my-super-secret-key-change-in-production
    volumes:
      - ./uploads:/app/uploads      # 使用者上傳的檔案
    networks:
      - backend
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s

  # ============ PostgreSQL 資料庫 ============
  db:
    image: postgres:16-alpine
    container_name: flask-db
    environment:
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=secretpass
      - POSTGRES_DB=appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data   # 資料持久化
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # 初始化 SQL
    networks:
      - backend
    ports:
      - "5432:5432"                 # 開發時方便用工具連線
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  # ============ Redis 快取 ============
  cache:
    image: redis:7-alpine
    container_name: flask-cache
    command: redis-server --requirepass redispass --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    networks:
      - backend
    ports:
      - "6379:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "redispass", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local

networks:
  backend:
    driver: bridge
```

### 4.4 Docker Compose 常用指令

```bash
# 啟動所有服務（背景執行）
docker compose up -d

# 啟動並強制重建映像檔
docker compose up -d --build

# 查看服務狀態
docker compose ps

# 查看所有服務的日誌
docker compose logs

# 追蹤特定服務的日誌
docker compose logs -f web

# 停止所有服務
docker compose down

# 停止並刪除 volume（資料也會被刪除，小心使用）
docker compose down -v

# 重啟特定服務
docker compose restart web

# 進入特定服務的 shell
docker compose exec web bash

# 執行一次性指令
docker compose run --rm web python manage.py migrate
```

---

## 5. Docker Volume 與資料持久化

### 5.1 為什麼需要 Volume

容器是短暫的（ephemeral）：當容器被刪除，裡面的資料也跟著消失。
Volume 讓資料可以「活」在容器之外，即使容器被刪除重建，資料依然保留。

### 5.2 Named Volume vs Bind Mount

```
┌─────────────────────────────────────────────────────┐
│                  Volume 類型比較                      │
├──────────────┬──────────────────┬───────────────────┤
│              │  Named Volume    │  Bind Mount       │
├──────────────┼──────────────────┼───────────────────┤
│ 儲存位置     │ Docker 管理的路徑 │ 主機的任意路徑     │
│ 建立方式     │ docker volume    │ 指定主機路徑       │
│ 適用場景     │ 資料庫資料       │ 開發時程式碼同步    │
│ 可攜性       │ 高（Docker 管理） │ 低（綁定主機路徑） │
│ 效能         │ 較好             │ macOS/Windows 較慢 │
│ 備份         │ docker 指令      │ 直接複製檔案       │
└──────────────┴──────────────────┴───────────────────┘
```

### 5.3 實際範例

```bash
# === Named Volume ===

# 建立 named volume
docker volume create my-data

# 使用 named volume 啟動容器
docker run -d \
  --name postgres-db \
  -v my-data:/var/lib/postgresql/data \
  postgres:16

# 列出所有 volume
docker volume ls

# 查看 volume 詳細資訊
docker volume inspect my-data
# 會顯示實際儲存路徑（通常在 /var/lib/docker/volumes/...）

# 刪除 volume
docker volume rm my-data

# 清理未使用的 volume
docker volume prune

# === Bind Mount ===

# 把本地目錄掛載到容器內（開發用）
docker run -d \
  --name dev-server \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/config:/app/config:ro \
  -p 3000:3000 \
  my-dev-image

# :ro = read-only（容器不能修改）
# 沒加 :ro = read-write（預設）

# === Anonymous Volume ===

# 排除特定目錄（常用於 node_modules）
docker run -d \
  -v $(pwd):/app \
  -v /app/node_modules \
  node:20
# 第一個 -v 把本地目錄掛載到 /app
# 第二個 -v 建立匿名 volume 給 node_modules
# 這樣容器內的 node_modules 不會被本地目錄覆蓋
```

---

## 6. Docker Network

### 6.1 網路驅動程式類型

```
┌──────────────────────────────────────────────────────┐
│  bridge（預設）                                       │
│  ├── 容器之間透過虛擬網路互相通訊                       │
│  ├── 容器與外部透過 port mapping (-p) 通訊             │
│  └── 最常用的模式                                     │
│                                                      │
│  host                                                │
│  ├── 容器直接使用主機的網路                             │
│  ├── 不需要 port mapping                              │
│  └── 效能最好，但失去網路隔離                           │
│                                                      │
│  none                                                │
│  ├── 容器完全沒有網路                                  │
│  └── 用於安全性要求極高的場景                           │
└──────────────────────────────────────────────────────┘
```

### 6.2 容器間通訊

```bash
# 建立自訂網路
docker network create my-network

# 啟動容器並加入網路
docker run -d --name web --network my-network nginx
docker run -d --name api --network my-network node:20

# 在同一個網路中，容器可以用「容器名稱」互相存取
# 例如在 web 容器中：
docker exec web curl http://api:3000
# "api" 就是容器名稱，Docker 的內建 DNS 會解析

# 列出所有網路
docker network ls

# 查看網路詳細資訊（包含哪些容器連接了）
docker network inspect my-network

# 把執行中的容器連到網路
docker network connect my-network existing-container

# 把容器從網路斷開
docker network disconnect my-network existing-container

# 刪除網路
docker network rm my-network
```

---

## 7. Git 完全攻略

### 7.1 Git 基礎指令

```bash
# ======================================
# 初始化與設定
# ======================================

# 初始化 Git 儲存庫
git init
# 在當前目錄建立 .git 資料夾，開始版本控制

# 設定使用者資訊
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 查看設定
git config --list

# ======================================
# 基本工作流程：add → commit → push
# ======================================

# 查看目前狀態
git status
# 顯示哪些檔案被修改、哪些是新增的、哪些已 staged

# 把檔案加入暫存區（staging area）
git add app.py                 # 加入特定檔案
git add src/                   # 加入整個目錄
git add .                      # 加入所有變更（小心使用）
git add -p                     # 互動式選擇要加入的部分

# 提交暫存區的變更
git commit -m "feat: add user authentication"
# -m : 提交訊息（簡短描述這次變更）

# 提交訊息最佳實踐（Conventional Commits）
# feat:     新功能
# fix:      修 bug
# docs:     文件更新
# style:    格式調整（不影響程式邏輯）
# refactor: 重構
# test:     測試相關
# chore:    雜務（建置工具、設定檔等）

# 推送到遠端
git push origin main
# origin : 遠端名稱（預設）
# main   : 分支名稱

# 從遠端拉取最新版本
git pull origin main
# 等於 git fetch + git merge

# 複製遠端儲存庫
git clone https://github.com/username/repo.git
git clone git@github.com:username/repo.git  # SSH 方式
```

### 7.2 Branch（分支）操作

```bash
# 查看所有分支
git branch            # 本地分支
git branch -r         # 遠端分支
git branch -a         # 所有分支

# 建立新分支
git branch feature/login

# 切換分支
git checkout feature/login
# 或者用較新的指令
git switch feature/login

# 建立並切換（一步到位）
git checkout -b feature/login
git switch -c feature/login

# 刪除分支（已合併的）
git branch -d feature/login

# 強制刪除分支（未合併的）
git branch -D feature/login

# 推送新分支到遠端
git push -u origin feature/login
# -u : 設定上游追蹤（之後只要 git push 即可）
```

### 7.3 Merge vs Rebase（圖解）

```
# === Merge（合併）===
# 保留完整的分支歷史，建立一個合併提交

# 合併前：
#        A---B---C  (feature)
#       /
#  D---E---F---G  (main)

git checkout main
git merge feature

# 合併後：
#        A---B---C
#       /         \
#  D---E---F---G---H  (main，H 是合併提交)

# === Rebase（變基）===
# 把分支的提交「接」到目標分支的最新提交後面

# Rebase 前：
#        A---B---C  (feature)
#       /
#  D---E---F---G  (main)

git checkout feature
git rebase main

# Rebase 後：
#                  A'--B'--C'  (feature)
#                 /
#  D---E---F---G  (main)

# 然後 fast-forward merge：
git checkout main
git merge feature

# 最終結果：
#  D---E---F---G---A'--B'--C'  (main) ← 漂亮的直線歷史
```

**何時用 Merge，何時用 Rebase？**

| 情境                      | 建議      |
|--------------------------|---------|
| 合併 feature 到 main       | Merge   |
| 更新 feature 到 main 的最新  | Rebase  |
| 已推送到遠端的分支            | Merge   |
| 只有自己在用的本地分支          | Rebase  |
| 需要保留完整歷史              | Merge   |
| 想要乾淨的線性歷史            | Rebase  |

### 7.4 Git Stash（暫存）

```bash
# 場景：你正在寫 feature，但突然要切到 main 修 bug
# 問題：你的 feature 改到一半，不想 commit 半成品

# 把目前的修改暫存起來
git stash
# 工作目錄會恢復到最後一次 commit 的狀態

# 加上訊息（方便識別）
git stash push -m "login feature: halfway done with validation"

# 查看所有暫存
git stash list
# stash@{0}: On feature/login: login feature: halfway done with validation
# stash@{1}: WIP on main: abc1234 fix typo

# 恢復最近一次暫存（並從 stash list 中移除）
git stash pop

# 恢復特定暫存
git stash pop stash@{1}

# 恢復但保留在 stash list 中
git stash apply

# 刪除特定暫存
git stash drop stash@{0}

# 清除所有暫存
git stash clear
```

### 7.5 Git Log（查看歷史）

```bash
# 基本 log
git log

# 精簡版（最常用）
git log --oneline
# abc1234 feat: add login page
# def5678 fix: resolve database connection issue
# ghi9012 docs: update README

# 圖形化分支歷史（超實用）
git log --oneline --graph --all
# * abc1234 (HEAD -> main) Merge branch 'feature/login'
# |\
# | * def5678 (feature/login) feat: add login validation
# | * ghi9012 feat: add login page
# |/
# * jkl3456 fix: resolve database issue

# 自訂格式
git log --pretty=format:"%h - %an, %ar : %s" -10
# abc1234 - William, 2 hours ago : feat: add login page

# 搜尋提交訊息
git log --grep="fix"

# 查看特定檔案的歷史
git log --follow -- src/app.py
```

### 7.6 .gitignore 範例

```gitignore
# ============================================
# .gitignore — 通用開發專案範本
# ============================================

# === 作業系統 ===
.DS_Store
Thumbs.db
Desktop.ini

# === IDE / 編輯器 ===
.vscode/
.idea/
*.swp
*.swo
*~

# === Python ===
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
dist/
build/
.venv/
venv/
env/
.eggs/
*.egg

# === Node.js ===
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# === C/C++ ===
*.o
*.obj
*.exe
*.out
*.so
*.dylib
build/
cmake-build-*/

# === Go ===
/vendor/
*.exe

# === 環境與機密 ===
.env
.env.local
.env.production
*.pem
*.key
credentials.json
secrets.yaml

# === 日誌與暫存 ===
*.log
logs/
tmp/
temp/

# === Docker ===
docker-compose.override.yml

# === 測試覆蓋率 ===
coverage/
.coverage
htmlcov/
.pytest_cache/

# === 資料與模型（大檔案）===
*.csv
*.h5
*.pkl
*.model
data/
```

### 7.7 Git Flow 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Git Flow 工作流程                      │
│                                                         │
│  main (production)                                      │
│  ──●────────────────●──────────────────●──> (穩定版本)   │
│    │                ↑                  ↑                │
│    │         merge  │           merge  │                │
│    ↓                │                  │                │
│  develop                                                │
│  ──●──●──●──●──●──●──●──●──●──●──●──●──●──> (開發主線)   │
│    │     ↑     │        ↑     │        ↑               │
│    ↓     │     ↓        │     ↓        │               │
│  feature/A   feature/B      feature/C                   │
│  ──●──●──┘   ──●──●──●──┘   ──●──●──●──┘               │
│                                                         │
│  hotfix（緊急修復，從 main 分出，合併回 main 和 develop）  │
│  main ──●────────────●──>                               │
│          ↓          ↑                                   │
│        hotfix ──●──●┘                                   │
└─────────────────────────────────────────────────────────┘
```

```bash
# Git Flow 實際操作

# 1. 開始新功能
git checkout develop
git pull origin develop
git checkout -b feature/user-profile

# 2. 在 feature 分支上開發
git add .
git commit -m "feat: add user profile page"
git commit -m "feat: add avatar upload"

# 3. 完成功能，合併回 develop
git checkout develop
git pull origin develop
git merge --no-ff feature/user-profile
# --no-ff : 強制建立合併提交（保留分支歷史）
git push origin develop
git branch -d feature/user-profile

# 4. 準備發版
git checkout -b release/v1.2.0 develop
# 在 release 分支上做最後的測試、修 bug
git commit -m "chore: bump version to 1.2.0"

# 5. 發版
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# 同時合併回 develop
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop
git branch -d release/v1.2.0

# 6. 緊急修復（hotfix）
git checkout -b hotfix/critical-bug main
git commit -m "fix: resolve critical security issue"

git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git push origin main --tags

git checkout develop
git merge --no-ff hotfix/critical-bug
git push origin develop
git branch -d hotfix/critical-bug
```

---

## 8. CI/CD 概念與實戰

### 8.1 什麼是 CI/CD

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  CI (Continuous Integration) — 持續整合                  │
│  ├── 開發者頻繁地把程式碼合併到主分支                      │
│  ├── 每次合併自動執行：編譯、測試、程式碼品質檢查            │
│  └── 目標：盡早發現問題                                  │
│                                                         │
│  CD (Continuous Delivery) — 持續交付                     │
│  ├── CI 通過後，自動準備好可部署的版本                     │
│  ├── 部署到 staging 環境進行最終驗證                      │
│  └── 按下按鈕即可部署到 production                       │
│                                                         │
│  CD (Continuous Deployment) — 持續部署                   │
│  ├── 比 Delivery 更進一步                               │
│  ├── CI 通過後自動部署到 production                      │
│  └── 完全自動化，不需要人工介入                           │
│                                                         │
│  流程圖：                                                │
│  程式碼 → Push → CI 測試 → 建置 → [手動核准] → 部署      │
│                                     ↑                   │
│                            Delivery 在這裡停             │
│                            Deployment 直接過             │
└─────────────────────────────────────────────────────────┘
```

### 8.2 GitHub Actions：Python 測試 + Lint

```yaml
# .github/workflows/python-ci.yml
# Python 專案的完整 CI 流程

name: Python CI

# 觸發條件
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# 環境變數
env:
  PYTHON_VERSION: "3.12"

jobs:
  # ============ 程式碼品質檢查 ============
  lint:
    name: Code Quality Check
    runs-on: ubuntu-latest

    steps:
      # 1. 取出程式碼
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. 設定 Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      # 3. 快取 pip 套件（加速後續執行）
      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements-dev.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      # 4. 安裝開發依賴
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      # 5. 執行 Ruff（超快的 Python linter）
      - name: Run Ruff linter
        run: ruff check .

      # 6. 執行 Ruff formatter 檢查
      - name: Run Ruff format check
        run: ruff format --check .

      # 7. 執行 mypy 型別檢查
      - name: Run mypy type check
        run: mypy src/

  # ============ 測試 ============
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint  # lint 通過才跑測試

    # 測試需要的服務（資料庫等）
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=xml \
            --cov-report=html \
            --junitxml=test-results.xml \
            -v

      # 上傳測試報告
      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: htmlcov/

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: test-results.xml
```

### 8.3 GitHub Actions：Node.js 建置 + 部署

```yaml
# .github/workflows/node-ci-cd.yml
# Node.js 專案的 CI/CD 流程

name: Node.js CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: "20"

jobs:
  # ============ 建置與測試 ============
  build-and-test:
    name: Build & Test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      # 把建置產出存起來，給後續 job 使用
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/

  # ============ 部署到 Staging ============
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-and-test
    if: github.ref == 'refs/heads/main'

    environment:
      name: staging
      url: https://staging.myapp.com

    steps:
      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Deploy to staging server
        env:
          SSH_PRIVATE_KEY: ${{ secrets.STAGING_SSH_KEY }}
          STAGING_HOST: ${{ secrets.STAGING_HOST }}
          STAGING_USER: ${{ secrets.STAGING_USER }}
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H "$STAGING_HOST" >> ~/.ssh/known_hosts

          rsync -avz --delete \
            dist/ \
            "$STAGING_USER@$STAGING_HOST:/var/www/staging/"

  # ============ 部署到 Production（需手動核准）============
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'

    environment:
      name: production
      url: https://myapp.com

    steps:
      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Deploy to production server
        env:
          SSH_PRIVATE_KEY: ${{ secrets.PROD_SSH_KEY }}
          PROD_HOST: ${{ secrets.PROD_HOST }}
          PROD_USER: ${{ secrets.PROD_USER }}
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H "$PROD_HOST" >> ~/.ssh/known_hosts

          rsync -avz --delete \
            dist/ \
            "$PROD_USER@$PROD_HOST:/var/www/production/"
```

### 8.4 GitHub Actions：Docker Build + Push

```yaml
# .github/workflows/docker-publish.yml
# 建置 Docker 映像檔並推送到 Docker Hub / GitHub Container Registry

name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ["v*"]           # 推送 tag 時也觸發
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write       # 推送到 GitHub Container Registry 需要

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # 設定 Docker Buildx（支援多平台建置）
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 登入 GitHub Container Registry
      - name: Login to GitHub Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # 產生映像檔標籤與標記
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      # 建置並推送
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha      # 使用 GitHub Actions 快取
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64  # 多平台支援
```

---

## 9. 環境管理

### 9.1 開發 vs 測試 vs 生產

```
┌──────────────────────────────────────────────────────┐
│              三種環境的差異                             │
├──────────┬─────────────┬────────────┬────────────────┤
│          │ Development │   Staging  │   Production   │
├──────────┼─────────────┼────────────┼────────────────┤
│ 目的     │ 開發與除錯   │ 測試與驗證  │ 面向使用者      │
│ Debug    │ 開啟        │ 開啟       │ 關閉           │
│ 日誌等級  │ DEBUG       │ INFO       │ WARNING        │
│ 資料庫   │ 本地/SQLite │ 複製的真資料 │ 真正的資料庫    │
│ HTTPS    │ 不需要      │ 需要       │ 必須           │
│ 效能     │ 不重要      │ 接近生產    │ 最高優先        │
│ 誰能存取  │ 開發者      │ 測試團隊    │ 所有使用者      │
└──────────┴─────────────┴────────────┴────────────────┘
```

### 9.2 環境變數管理

```bash
# === 方法 1：直接設定環境變數 ===
export DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"
export SECRET_KEY="my-secret-key"
export DEBUG="true"

# 在 Python 中讀取
# import os
# db_url = os.environ.get("DATABASE_URL")

# === 方法 2：.env 檔案 ===
# 建立 .env 檔案（不要提交到 Git！）
```

`.env` 檔案範例：

```bash
# .env — 開發環境
DATABASE_URL=postgresql://devuser:devpass@localhost:5432/devdb
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-not-for-production
DEBUG=true
LOG_LEVEL=DEBUG
ALLOWED_HOSTS=localhost,127.0.0.1
SMTP_HOST=localhost
SMTP_PORT=1025
```

```bash
# .env.production — 生產環境（範本）
DATABASE_URL=postgresql://produser:STRONG_PASSWORD@db.example.com:5432/proddb
REDIS_URL=redis://cache.example.com:6379/0
SECRET_KEY=CHANGE_ME_TO_A_RANDOM_STRING
DEBUG=false
LOG_LEVEL=WARNING
ALLOWED_HOSTS=myapp.com,www.myapp.com
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
```

Docker Compose 中使用 `.env`：

```yaml
# docker-compose.yml
services:
  web:
    build: .
    env_file:
      - .env            # 載入 .env 檔案
    environment:
      - OVERRIDE_VAR=this-overrides-env-file  # 會覆蓋 .env 中的同名變數
```

### 9.3 Docker Secrets（生產環境機密管理）

```bash
# Docker Secrets 用於 Docker Swarm 模式下管理敏感資訊
# 比環境變數更安全（不會出現在 docker inspect 中）

# 建立 secret
echo "my-super-secret-password" | docker secret create db_password -

# 在 docker-compose.yml 中使用 secrets
```

```yaml
# docker-compose.yml (Swarm mode)
version: "3.9"

services:
  web:
    image: my-web-app
    secrets:
      - db_password
      - api_key
    environment:
      # 應用程式從檔案讀取 secret
      - DB_PASSWORD_FILE=/run/secrets/db_password

  db:
    image: postgres:16
    secrets:
      - db_password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt    # 從檔案讀取
  api_key:
    external: true                      # 已經用 docker secret create 建立
```

```python
# Python 中讀取 Docker Secret 的方式
import os

def get_secret(secret_name: str) -> str:
    """從 Docker Secret 或環境變數讀取機密"""
    # 先嘗試從 Docker Secret 檔案讀取
    secret_file = f"/run/secrets/{secret_name}"
    if os.path.exists(secret_file):
        with open(secret_file, "r") as f:
            return f.read().strip()

    # 退回到環境變數
    env_var = secret_name.upper()
    value = os.environ.get(env_var)
    if value is None:
        raise ValueError(f"Secret '{secret_name}' not found")
    return value

# 使用
db_password = get_secret("db_password")
```

---

## 10. Linux 基本指令（開發者必備）

### 10.1 檔案操作

```bash
# === ls — 列出檔案 ===
ls                    # 列出當前目錄
ls -l                 # 長格式（權限、大小、日期）
ls -la                # 包含隱藏檔案（以 . 開頭的）
ls -lh                # 人類可讀的檔案大小（KB, MB, GB）
ls -lt                # 按修改時間排序

# === cd — 切換目錄 ===
cd /home/user         # 切到絕對路徑
cd ..                 # 上一層
cd ~                  # 回到家目錄
cd -                  # 回到上一次的目錄

# === pwd — 顯示當前目錄 ===
pwd
# /home/user/projects/my-app

# === mkdir — 建立目錄 ===
mkdir mydir           # 建立目錄
mkdir -p a/b/c        # 建立巢狀目錄（自動建立不存在的父目錄）

# === cp — 複製 ===
cp file.txt backup.txt         # 複製檔案
cp -r src/ src_backup/         # 複製目錄（-r = recursive）

# === mv — 移動/重新命名 ===
mv old.txt new.txt             # 重新命名
mv file.txt /tmp/              # 移動到其他目錄

# === rm — 刪除 ===
rm file.txt                    # 刪除檔案
rm -r mydir/                   # 刪除目錄及其內容
rm -rf mydir/                  # 強制刪除（不詢問確認，小心使用）

# === 其他實用指令 ===
touch newfile.txt              # 建立空檔案（或更新修改時間）
ln -s /path/to/target link     # 建立符號連結（symbolic link）
find . -name "*.py"            # 搜尋檔案
du -sh *                       # 顯示各檔案/目錄的大小
df -h                          # 顯示磁碟使用量
```

### 10.2 文字處理

```bash
# === cat — 顯示檔案內容 ===
cat file.txt                   # 印出整個檔案
cat -n file.txt                # 顯示行號

# === grep — 搜尋文字 ===
grep "error" logfile.txt       # 搜尋包含 "error" 的行
grep -i "error" logfile.txt    # 不分大小寫
grep -r "TODO" src/            # 遞迴搜尋目錄
grep -n "error" logfile.txt    # 顯示行號
grep -c "error" logfile.txt    # 只顯示匹配的行數
grep -v "debug" logfile.txt    # 反向搜尋（不包含 "debug" 的行）

# === awk — 欄位處理 ===
# 印出第 1 和第 3 欄（以空白分隔）
awk '{print $1, $3}' data.txt

# 指定分隔符號（例如逗號）
awk -F',' '{print $1, $2}' data.csv

# 條件篩選
awk '$3 > 100 {print $1, $3}' data.txt

# === sed — 串流編輯器 ===
# 取代文字（第一個匹配）
sed 's/old/new/' file.txt

# 取代所有匹配
sed 's/old/new/g' file.txt

# 直接修改檔案（原地編輯）
sed -i 's/old/new/g' file.txt

# 刪除特定行
sed '3d' file.txt              # 刪除第 3 行
sed '/pattern/d' file.txt      # 刪除匹配的行

# === wc — 字數統計 ===
wc file.txt                    # 行數 字數 位元組數
wc -l file.txt                 # 只顯示行數
wc -w file.txt                 # 只顯示字數

# === 其他文字工具 ===
head -20 file.txt              # 顯示前 20 行
tail -20 file.txt              # 顯示後 20 行
tail -f logfile.txt            # 即時追蹤檔案（看 log 很實用）
sort file.txt                  # 排序
sort -u file.txt               # 排序並去重
uniq -c sorted.txt             # 統計重複行數
diff file1.txt file2.txt       # 比較兩個檔案的差異
```

### 10.3 程序管理

```bash
# === ps — 查看程序 ===
ps aux                         # 顯示所有程序
ps aux | grep python           # 篩選 Python 程序

# === top / htop — 即時監控 ===
top                            # 即時顯示系統資源使用（按 q 離開）
htop                           # top 的增強版（需要安裝）

# === kill — 結束程序 ===
kill 1234                      # 發送 SIGTERM（正常結束）
kill -9 1234                   # 發送 SIGKILL（強制結束）
killall python                 # 結束所有名為 python 的程序

# === nohup — 背景執行 ===
nohup python server.py &
# nohup : 即使終端關閉，程序也不會停止
# &     : 在背景執行
# 輸出會被寫入 nohup.out

# 更推薦的方式：使用 screen 或 tmux
```

### 10.4 網路指令

```bash
# === curl — 發送 HTTP 請求 ===
curl https://api.example.com              # GET 請求
curl -X POST https://api.example.com \
     -H "Content-Type: application/json" \
     -d '{"name":"test"}'                 # POST 請求
curl -o file.zip https://example.com/file.zip  # 下載檔案
curl -I https://example.com              # 只看 response headers
curl -v https://example.com              # 詳細輸出（debug 用）

# === wget — 下載檔案 ===
wget https://example.com/file.zip
wget -O output.zip https://example.com/file.zip  # 指定檔名
wget -r https://example.com/docs/         # 遞迴下載整個目錄

# === ping — 測試連線 ===
ping google.com                           # 測試網路是否通
ping -c 5 google.com                      # 只 ping 5 次

# === netstat / ss — 查看網路連線 ===
netstat -tlnp                             # 查看監聽的 port
ss -tlnp                                  # 更現代的 netstat 替代品
# -t : TCP
# -l : listening（監聽中）
# -n : 顯示數字（不解析 DNS）
# -p : 顯示程序名稱
```

### 10.5 權限管理

```bash
# === chmod — 修改權限 ===
# 權限格式：rwx = read(4) + write(2) + execute(1)
# 三組：擁有者 / 群組 / 其他人

chmod 755 script.sh            # rwxr-xr-x（擁有者可讀寫執行，其他人可讀執行）
chmod 644 file.txt             # rw-r--r--（擁有者可讀寫，其他人只讀）
chmod +x script.sh             # 加上執行權限
chmod -w file.txt              # 移除寫入權限
chmod -R 755 mydir/            # 遞迴修改目錄內所有檔案

# === chown — 修改擁有者 ===
chown user:group file.txt      # 修改擁有者和群組
chown -R user:group mydir/     # 遞迴修改
```

### 10.6 SSH 基礎

```bash
# === SSH 連線 ===
ssh user@hostname              # 基本連線
ssh -p 2222 user@hostname      # 指定 port
ssh -i ~/.ssh/my_key user@hostname  # 指定私鑰

# === SSH 金鑰產生 ===
ssh-keygen -t ed25519 -C "your_email@example.com"
# 產生公鑰（~/.ssh/id_ed25519.pub）和私鑰（~/.ssh/id_ed25519）

# 複製公鑰到遠端伺服器
ssh-copy-id user@hostname
# 之後就可以免密碼登入

# === SCP — 透過 SSH 傳檔案 ===
scp file.txt user@hostname:/remote/path/     # 上傳
scp user@hostname:/remote/file.txt ./        # 下載
scp -r mydir/ user@hostname:/remote/path/    # 傳整個目錄

# === SSH Config ===
# 在 ~/.ssh/config 設定常用連線
```

`~/.ssh/config` 範例：

```
Host myserver
    HostName 192.168.1.100
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host staging
    HostName staging.example.com
    User admin
    Port 2222
    IdentityFile ~/.ssh/staging_key
```

```bash
# 設定好後，直接用名稱連線
ssh myserver       # 等於 ssh -i ~/.ssh/id_ed25519 deploy@192.168.1.100
ssh staging        # 等於 ssh -i ~/.ssh/staging_key -p 2222 admin@staging.example.com
```

---

## 11. 雲端部署概覽

### 11.1 三大雲端平台

```
┌──────────────────────────────────────────────────────────┐
│               三大雲端平台對照表                            │
├───────────────┬──────────┬──────────────┬────────────────┤
│   服務類別     │   AWS    │     GCP      │    Azure       │
├───────────────┼──────────┼──────────────┼────────────────┤
│ 虛擬機器      │ EC2      │ Compute      │ Virtual        │
│              │          │ Engine       │ Machines       │
├───────────────┼──────────┼──────────────┼────────────────┤
│ 容器服務      │ ECS/EKS  │ GKE/Cloud    │ AKS/Container  │
│              │          │ Run          │ Instances      │
├───────────────┼──────────┼──────────────┼────────────────┤
│ 物件儲存      │ S3       │ Cloud        │ Blob Storage   │
│              │          │ Storage      │                │
├───────────────┼──────────┼──────────────┼────────────────┤
│ 資料庫        │ RDS      │ Cloud SQL    │ SQL Database   │
├───────────────┼──────────┼──────────────┼────────────────┤
│ 無伺服器函式  │ Lambda   │ Cloud        │ Azure          │
│              │          │ Functions    │ Functions      │
├───────────────┼──────────┼──────────────┼────────────────┤
│ 容器映像      │ ECR      │ Artifact     │ Container      │
│ 倉庫         │          │ Registry     │ Registry       │
└───────────────┴──────────┴──────────────┴────────────────┘
```

### 11.2 EC2 / Compute Engine（虛擬機器）

```bash
# === AWS EC2 基本操作（使用 AWS CLI）===

# 安裝 AWS CLI
pip install awscli
aws configure
# 輸入 Access Key ID, Secret Access Key, Region

# 啟動一個 EC2 實例
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-903004f8

# 列出所有實例
aws ec2 describe-instances

# SSH 連線到 EC2
ssh -i "my-key-pair.pem" ec2-user@ec2-xx-xx-xx-xx.compute-1.amazonaws.com

# === GCP Compute Engine 基本操作（使用 gcloud CLI）===

# 安裝 gcloud CLI 後
gcloud init

# 建立虛擬機
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud

# SSH 連線
gcloud compute ssh my-vm --zone=us-central1-a
```

### 11.3 S3 / Cloud Storage（物件儲存）

```bash
# === AWS S3 ===

# 建立 bucket
aws s3 mb s3://my-unique-bucket-name

# 上傳檔案
aws s3 cp myfile.txt s3://my-bucket/path/
aws s3 cp --recursive mydir/ s3://my-bucket/mydir/

# 下載檔案
aws s3 cp s3://my-bucket/path/myfile.txt ./

# 列出 bucket 內容
aws s3 ls s3://my-bucket/

# 同步本地目錄到 S3
aws s3 sync ./build/ s3://my-bucket/ --delete

# === GCP Cloud Storage ===

# 建立 bucket
gsutil mb gs://my-unique-bucket-name

# 上傳
gsutil cp myfile.txt gs://my-bucket/path/
gsutil -m cp -r mydir/ gs://my-bucket/mydir/

# 下載
gsutil cp gs://my-bucket/path/myfile.txt ./

# 同步
gsutil -m rsync -d -r ./build/ gs://my-bucket/
```

### 11.4 Docker on Cloud

```bash
# === 方案 1：在 EC2 上跑 Docker ===
# SSH 進入 EC2 後
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -aG docker ec2-user

# 拉取並執行映像檔
docker pull my-registry/my-app:latest
docker run -d -p 80:5000 my-registry/my-app:latest

# === 方案 2：AWS ECS（Elastic Container Service）===
# 使用 AWS 管理的容器服務，不需要自己管理伺服器

# === 方案 3：GCP Cloud Run（最簡單）===
# 直接把 Docker 映像檔部署為無伺服器服務

# 建置並推送映像檔到 GCP
gcloud builds submit --tag gcr.io/my-project/my-app

# 部署到 Cloud Run
gcloud run deploy my-app \
  --image gcr.io/my-project/my-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000 \
  --memory 512Mi \
  --cpu 1

# 部署完成後會給你一個 HTTPS URL
# https://my-app-xxxx-uc.a.run.app
```

---

## 12. 完整 DevOps 流程範例

### 一個完整的開發到部署流程

```
步驟 1: 寫程式
    ↓
步驟 2: Git push
    ↓
步驟 3: CI 自動測試
    ↓
步驟 4: Docker build
    ↓
步驟 5: 部署
```

以下是每一步的具體操作：

### 步驟 1：寫程式

```python
# app.py — 一個簡單的 Flask API
from flask import Flask, jsonify, request
import os
import redis

app = Flask(__name__)

# 連接 Redis
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
cache = redis.from_url(redis_url)

@app.route("/")
def home():
    return jsonify({
        "service": "my-api",
        "version": "1.0.0",
        "status": "running"
    })

@app.route("/health")
def health():
    try:
        cache.ping()
        return jsonify({"status": "healthy", "redis": "connected"}), 200
    except redis.ConnectionError:
        return jsonify({"status": "unhealthy", "redis": "disconnected"}), 503

@app.route("/counter", methods=["GET"])
def get_counter():
    count = cache.get("visit_count")
    return jsonify({"count": int(count) if count else 0})

@app.route("/counter", methods=["POST"])
def increment_counter():
    count = cache.incr("visit_count")
    return jsonify({"count": count})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

```python
# tests/test_app.py — 測試
import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    data = response.get_json()
    assert response.status_code == 200
    assert data["service"] == "my-api"
    assert data["version"] == "1.0.0"

@patch("app.cache")
def test_health_healthy(mock_cache, client):
    mock_cache.ping.return_value = True
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

@patch("app.cache")
def test_health_unhealthy(mock_cache, client):
    import redis
    mock_cache.ping.side_effect = redis.ConnectionError()
    response = client.get("/health")
    assert response.status_code == 503

@patch("app.cache")
def test_get_counter(mock_cache, client):
    mock_cache.get.return_value = b"42"
    response = client.get("/counter")
    assert response.get_json()["count"] == 42

@patch("app.cache")
def test_increment_counter(mock_cache, client):
    mock_cache.incr.return_value = 1
    response = client.post("/counter")
    assert response.get_json()["count"] == 1
```

```
# requirements.txt
flask==3.1.0
gunicorn==23.0.0
redis==5.2.1

# requirements-dev.txt
pytest==8.3.4
pytest-cov==6.0.0
ruff==0.8.6
mypy==1.14.1
```

```dockerfile
# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      cache:
        condition: service_healthy
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
```

### 步驟 2：Git Push

```bash
# 初始化 Git 並推送
git init
git add .
git commit -m "feat: initial project setup with Flask API, tests, and Docker"

# 在 GitHub 建立 repository 後
git remote add origin git@github.com:username/my-api.git
git push -u origin main

# --- 日常開發流程 ---

# 建立 feature 分支
git checkout -b feature/add-user-endpoint

# 開發完成後
git add src/users.py tests/test_users.py
git commit -m "feat: add user CRUD endpoints"
git push -u origin feature/add-user-endpoint

# 在 GitHub 上建立 Pull Request
# 等 CI 通過 + Code Review 後 merge
```

### 步驟 3：CI 自動測試

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Lint & Test
    runs-on: ubuntu-latest

    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with Ruff
        run: ruff check .

      - name: Run tests
        env:
          REDIS_URL: redis://localhost:6379/0
        run: pytest tests/ --cov=. --cov-report=xml -v

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.xml
```

### 步驟 4：Docker Build

```yaml
# .github/workflows/docker.yml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  docker:
    name: Build & Push
    runs-on: ubuntu-latest
    needs: test  # CI 測試通過才建置

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 步驟 5：部署

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_run:
    workflows: ["Docker Build & Push"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    environment:
      name: production
      url: https://myapp.example.com

    steps:
      - name: Deploy to server via SSH
        env:
          SSH_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
          HOST: ${{ secrets.DEPLOY_HOST }}
          USER: ${{ secrets.DEPLOY_USER }}
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H "$HOST" >> ~/.ssh/known_hosts

          ssh $USER@$HOST << 'DEPLOY_SCRIPT'
            cd /opt/my-api

            # 拉取最新映像檔
            docker pull ghcr.io/username/my-api:latest

            # 停止舊容器
            docker compose down

            # 啟動新容器
            docker compose up -d

            # 等待健康檢查
            echo "Waiting for health check..."
            sleep 10
            curl -f http://localhost:5000/health || exit 1

            # 清理舊映像檔
            docker image prune -f

            echo "Deployment successful!"
          DEPLOY_SCRIPT

      - name: Notify on failure
        if: failure()
        run: |
          echo "Deployment failed! Check the logs."
          # 這裡可以加上 Slack/Discord 通知
```

### 完整流程總結

```
┌─────────────────────────────────────────────────────────┐
│              完整 DevOps 流程                            │
│                                                         │
│  開發者                                                  │
│    │                                                    │
│    ├── 1. 寫程式碼                                       │
│    │     └── app.py, tests/, Dockerfile                 │
│    │                                                    │
│    ├── 2. git push                                      │
│    │     └── 推送到 GitHub                               │
│    │                                                    │
│    │  ┌─── GitHub Actions（自動觸發）──────────────┐     │
│    │  │                                           │     │
│    │  │  3. CI 自動測試                            │     │
│    │  │     ├── ruff check（程式碼品質）            │     │
│    │  │     ├── pytest（單元測試）                  │     │
│    │  │     └── coverage（覆蓋率報告）              │     │
│    │  │           │                               │     │
│    │  │           ↓ 測試通過                       │     │
│    │  │                                           │     │
│    │  │  4. Docker Build                          │     │
│    │  │     ├── docker build（建置映像檔）          │     │
│    │  │     └── docker push（推送到 Registry）     │     │
│    │  │           │                               │     │
│    │  │           ↓ 建置成功                       │     │
│    │  │                                           │     │
│    │  │  5. 部署                                   │     │
│    │  │     ├── SSH 到伺服器                       │     │
│    │  │     ├── docker pull（拉取新映像檔）         │     │
│    │  │     ├── docker compose up -d（啟動）       │     │
│    │  │     └── 健康檢查通過 → 部署完成              │     │
│    │  │                                           │     │
│    │  └───────────────────────────────────────────┘     │
│    │                                                    │
│    └── 使用者可以存取更新後的服務                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

每一步出錯時的處理：

| 步驟              | 如果失敗...                            |
|------------------|--------------------------------------|
| CI 測試           | PR 無法 merge，開發者修正後重新 push      |
| Docker Build     | 檢查 Dockerfile，通常是依賴安裝問題       |
| 部署              | 自動回滾到上一個版本，通知開發者           |
| 健康檢查          | 保留舊容器，新容器不接收流量              |

---

## 附錄：常用 Docker 指令速查表

```bash
# === 容器生命週期 ===
docker run          # 建立並啟動容器
docker start        # 啟動已停止的容器
docker stop         # 停止容器
docker restart      # 重啟容器
docker rm           # 刪除容器
docker kill         # 強制停止容器

# === 容器資訊 ===
docker ps           # 列出執行中的容器
docker ps -a        # 列出所有容器
docker logs         # 查看容器日誌
docker inspect      # 查看容器詳細資訊
docker stats        # 即時資源使用統計
docker top          # 查看容器內的程序

# === 映像檔 ===
docker build        # 從 Dockerfile 建置映像檔
docker images       # 列出本地映像檔
docker pull         # 從 Registry 拉取映像檔
docker push         # 推送映像檔到 Registry
docker rmi          # 刪除映像檔
docker tag          # 為映像檔加標籤

# === 系統清理 ===
docker system prune           # 清理所有未使用的資源
docker system prune -a        # 清理所有未使用的資源（含映像檔）
docker system df              # 查看 Docker 磁碟使用量

# === Docker Compose ===
docker compose up -d          # 啟動所有服務
docker compose down           # 停止所有服務
docker compose ps             # 查看服務狀態
docker compose logs -f        # 追蹤日誌
docker compose exec web bash  # 進入服務的 shell
docker compose build          # 重新建置
```

---

> **下一步學習建議**：
> - Kubernetes（K8s）：當你的服務規模成長，需要更強大的容器編排工具。
> - Terraform / Pulumi：用程式碼管理雲端基礎設施（Infrastructure as Code）。
> - Prometheus + Grafana：監控與可視化你的服務狀態。
> - ArgoCD / Flux：GitOps 風格的 Kubernetes 部署工具。
