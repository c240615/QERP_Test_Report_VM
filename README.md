# 建置 VM

## 如何使用

### 取得專案

```bash
git clone ......
```

### 確認是否已安裝 Python，並確認更新至最新版本的 pip

```bash
python --version
python -m pip install --upgrade pip
```

### Windows : 啟動虛擬環境 / 關閉虛擬環境

```bash
# 啟動虛擬環境
.\env\Scripts\activate
# 關閉虛擬環境
deactivate
```

### 在 requirements.txt 新增需要的套件版本

```bash
# 例
selenium==4.26.1
```

### 從 requirements.txt 安裝套件

```bash
# 查看已安裝套件
pip freeze
# 從 requirements.txt 安裝套件
pip install -r requirements.txt
```
