#!/bin/bash

# CanCong-Toys 服务管理脚本

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${PROJECT_DIR}/backend"

show_menu() {
    echo "=========================================="
    echo "    CanCong-Toys 服务管理脚本"
    echo "=========================================="
    echo
    echo "请选择操作:"
    echo "1. 启动服务"
    echo "2. 停止服务"
    echo "3. 重启服务"
    echo "4. 查看服务状态"
    echo "5. 后台启动服务"
    echo "6. 开发模式启动"
    echo "7. 退出"
    echo
}

start_service() {
    echo
    echo "正在启动 CanCong-Toys 服务..."
    cd "$BACKEND_DIR"
    python cli.py start
}

stop_service() {
    echo
    echo "正在停止 CanCong-Toys 服务..."
    cd "$BACKEND_DIR"
    python cli.py stop
}

restart_service() {
    echo
    echo "正在重启 CanCong-Toys 服务..."
    cd "$BACKEND_DIR"
    python cli.py restart
}

check_status() {
    echo
    echo "正在检查 CanCong-Toys 服务状态..."
    cd "$BACKEND_DIR"
    python cli.py status
}

background_start() {
    echo
    echo "正在后台启动 CanCong-Toys 服务..."
    cd "$BACKEND_DIR"
    python cli.py start --daemon
}

dev_mode() {
    echo
    echo "以开发模式启动 CanCong-Toys 服务..."
    cd "$BACKEND_DIR"
    python cli.py dev
}

main() {
    while true; do
        show_menu
        read -p "请输入选项 (1-7): " choice
        case $choice in
            1) start_service ;;
            2) stop_service ;;
            3) restart_service ;;
            4) check_status ;;
            5) background_start ;;
            6) dev_mode ;;
            7) echo; echo "感谢使用 CanCong-Toys 服务管理器！"; exit 0 ;;
            *) echo; echo "无效选项，请重新选择"; echo ;;
        esac
        echo
        read -p "按回车键继续..."
        clear
    done
}

# 运行主函数
main