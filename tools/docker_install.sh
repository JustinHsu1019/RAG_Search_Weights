# 更新 apt package index
sudo apt-get update

# 安裝 Docker 的必要套件
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg

# 新增 Docker 的官方 GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 設定 Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新 apt package index，並安裝 Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 啟動 Docker 並設定開機自動啟動
sudo systemctl start docker
sudo systemctl enable docker

# 下載 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 賦予可執行權限
sudo chmod +x /usr/local/bin/docker-compose

# 確認安裝是否成功
docker-compose --version
