# windows-wol
UV 管理的局域网WOL唤醒工具，用于远程唤醒 Windows P3784，配套探测主机在线状态、等待 Windows-MCP 服务端口就绪。

## ✨ 功能简介
1. `wake`：发送 WOL 魔术包唤醒局域网Windows主机，仅需要MAC地址
2. `status`：Ping探测主机在线状态，依赖IP地址
3. `wait`：循环等待，直到主机ping通 + 8090（Windows-MCP）端口开放

> 原理说明：WOL依靠MAC广播魔术包实现开机；IP仅用于ping连通性检测与端口探测，主机关机状态下IP无法访问。

## 📋 环境依赖
- 系统：Ubuntu / Debian Linux
- Python >= 3.10
- uv 包管理器

## 📁 项目目录结构
```

windows-wol/
├── pyproject.toml
├── README.md
├── src/
│   └── windows_wol/
│       └── **init**.py
├── .env（可选，存放默认 MAC/IP 配置）
└── dist/        # uv build 打包输出目录

```

## 🔨 构建 & 安装
### 1. 初始化项目虚拟环境
```bash
uv sync
```

### 2. 打包生成 whl /sdist 安装包

```
uv build
```

打包产物输出到 `dist/` 文件夹。

### 3. 全局安装（推荐，任意目录直接调用命令）

```
uv tool install dist/windows_wol-0.1.0-py3-none-any.whl
```

## 🚀 使用方法

>
> 两种使用模式：命令行传参（推荐，无需`.env`）；读取`.env`配置，不传参自动加载

### 唤醒主机

```
windows-wol wake --mac BC:38:98:A5:F0:00
```

### 检测主机在线状态

```
windows-wol status --ip 192.168.1.100
```

### 等待 Windows-MCP 8090 端口就绪

```
windows-wol wait --ip 192.168.1.100
```

### 一键唤醒并等待 MCP 服务就绪

```
windows-wol wake --mac BC:38:98:A5:F0:00 && windows-wol wait --ip 192.168.1.100
```

### 查看帮助文档

```
windows-wol -h
```

## ⚙️ .env 配置示例（可选）

项目根目录新建 `.env` 文件，不传入命令行参数时自动读取

```
P3_MAC=BC:38:98:A5:F0:00
P3_IP=192.168.1.100
BROADCAST=255.255.255.255
MCP_PORT=8090
```

## 🪟 Windows 主机（P3784）前置要求

1. BIOS/UEFI 开启 WOL 网络唤醒功能
2. Windows 网卡属性：开启「允许此设备唤醒计算机」
3. **关闭 Windows 快速启动**，快速启动会造成 WOL 唤醒失效
4. Windows-MCP 服务启动命令：

```
uvx windows-mcp serve --transport sse --host 0.0.0.0 --port 8090 --auth-key "my-secret-123"
```

5. Windows 防火墙放行 8090 端口

## 🗑️ 卸载

```
uv tool uninstall windows-wol
```

## ❗ 故障排查

1. 发包成功但主机不开机：核对 MAC 地址；检查 BIOS WOL、网卡供电；关闭 Windows 快速启动
2. wait 命令一直超时：可修改代码调大最大等待时长；确认 windows-mcp 监听`0.0.0.0`，防火墙放行 8090 端口
3. 提示命令找不到：使用`uv tool install`全局安装，不要仅安装在项目虚拟环境
4. ping 探测失败：Windows 防火墙拦截 ICMP，或目标主机未开机

## 🔗 完整联动流程

Ubuntu 运行 windows-wol → WOL 魔术包唤醒 P3784 Windows → wait 等待 8090 端口就绪 → MCP 客户端连接 windows-mcp，远程执行 Windows 关机 / 重启操作


### 写入文件命令，直接在终端运行
```bash
cat > ~/windows-wol/README.md << 'EOF'
# windows-wol
UV 管理的局域网WOL唤醒工具，用于远程唤醒 Windows P3784，配套探测主机在线状态、等待 Windows-MCP 服务端口就绪。

## ✨ 功能简介
1. `wake`：发送 WOL 魔术包唤醒局域网Windows主机，仅需要MAC地址
2. `status`：Ping探测主机在线状态，依赖IP地址
3. `wait`：循环等待，直到主机ping通 + 8090（Windows-MCP）端口开放

> 原理说明：WOL依靠MAC广播魔术包实现开机；IP仅用于ping连通性检测与端口探测，主机关机状态下IP无法访问。

## 📋 环境依赖
- 系统：Ubuntu / Debian Linux
- Python >= 3.10
- uv 包管理器

## 📁 项目目录结构

windows-wol/
├── pyproject.toml
├── README.md
├── src/
│   └── windows_wol/
│       └── **init**.py
├── .env（可选，存放默认 MAC/IP 配置）
└── dist/        # uv build 打包输出目录


## 🔨 构建 & 安装
### 1. 初始化项目虚拟环境
```bash
uv sync
```

### 2. 打包生成 whl /sdist 安装包

```
uv build
```

打包产物输出到 `dist/` 文件夹。

### 3. 全局安装（推荐，任意目录直接调用命令）

```
uv tool install dist/windows_wol-0.1.0-py3-none-any.whl
```

## 🚀 使用方法

>
> 两种使用模式：命令行传参（推荐，无需`.env`）；读取`.env`配置，不传参自动加载

### 唤醒主机

```
windows-wol wake --mac BC:38:98:A5:F0:00
```

### 检测主机在线状态

```
windows-wol status --ip 192.168.1.100
```

### 等待 Windows-MCP 8090 端口就绪

```
windows-wol wait --ip 192.168.1.100
```

### 一键唤醒并等待 MCP 服务就绪

```
windows-wol wake --mac BC:38:98:A5:F0:00 && windows-wol wait --ip 192.168.1.100
```

### 查看帮助文档

```
windows-wol -h
```

## ⚙️ .env 配置示例（可选）

项目根目录新建 `.env` 文件，不传入命令行参数时自动读取

```
P3_MAC=BC:38:98:A5:F0:00
P3_IP=192.168.1.100
BROADCAST=255.255.255.255
MCP_PORT=8090
```

## 🪟 Windows 主机（P3784）前置要求

1. BIOS/UEFI 开启 WOL 网络唤醒功能
2. Windows 网卡属性：开启「允许此设备唤醒计算机」
3. **关闭 Windows 快速启动**，快速启动会造成 WOL 唤醒失效
4. Windows-MCP 服务启动命令：

``` bash
uvx windows-mcp serve --transport sse --host 0.0.0.0 --port 8090 --auth-key "my-secret-123"
```

5. Windows 防火墙放行 8090 端口

## 🗑️ 卸载

``` bash
uv tool uninstall windows-wol
```

## ❗ 故障排查

1. 发包成功但主机不开机：核对 MAC 地址；检查 BIOS WOL、网卡供电；关闭 Windows 快速启动
2. wait 命令一直超时：可修改代码调大最大等待时长；确认 windows-mcp 监听`0.0.0.0`，防火墙放行 8090 端口
3. 提示命令找不到：使用`uv tool install`全局安装，不要仅安装在项目虚拟环境
4. ping 探测失败：Windows 防火墙拦截 ICMP，或目标主机未开机

## 🔗 完整联动流程

Ubuntu 运行 windows-wol → WOL 魔术包唤醒 P3784 Windows → wait 等待 8090 端口就绪 → MCP 客户端连接 windows-mcp，远程执行 Windows 关机 / 重启操作



执行上面这条`cat`命令，直接一次性把全部内容写入README.md，写完可以查看：
```bash
cat README.md
```
