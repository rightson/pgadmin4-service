#!/bin/bash

__DIR__=$(cd $(dirname $BASH_SOURC[0]) && pwd)

venv=${VENV-"venv"}

function execho() {
    echo $@
    $@
}

function get_site_packages_root() {
    local x=$(python3 --version | cut -d ' ' -f2 | cut -d'.' -f2)
    local site_packages=$(ls --color=none -d $venv/lib/python3.$x/site-packages)
    echo $site_packages
}

function get_pgadmin4_root() {
    echo $(get_site_packages_root)/pgadmin4
}

function patch_sqlalchemy() {
    local pysqlite_dialects=$(get_site_packages_root)/sqlalchemy/dialects/sqlite/pysqlite.py
    echo "Patching $pysqlite_dialects..."
    sed -i 's|import sqlite3|import pysqlite3|g' $pysqlite_dialects
    sed -i 's|from sqlite3 import|from pysqlite3 import|g' $pysqlite_dialects
}

function patch_config_local() {
    local config_local=$(get_pgadmin4_root)/config_local.py
    if [ ! -f $config_local ]; then
        execho cp -l $__DIR__/config_local.py $config_local
    fi
}

function init() {
    if [ ! -d ./$venv ]; then
        execho python3 -m $venv $venv;
        $venv/bin/pip3 install -U pip3
    fi

    source $venv/bin/activate

    if [ ! -f $venv/bin/gunicorn ]; then
        $venv/bin/pip3 install -U pip3
        execho $venv/bin/pip3 install -r requirements.txt
        patch_sqlalchemy
    fi

    local config_local=$(get_pgadmin4_root)/config_local.py
    if [ ! -f $config_local ]; then
        execho cp -l $__DIR__/config_local.py $config_local
    fi
}


function start() {
    local ip=${IP-"0.0.0.0"}
    local port=${PORT-"5050"}

    if [ ! -f $venv/bin/gunicorn ]; then
        init
    else
        source $venv/bin/activate
    fi

    export BASE_DIR=${__DIR__}
    cmd="gunicorn --bind $ip:$port --workers=1 --threads=4 --chdir $(get_pgadmin4_root) pgAdmin4:app $*"
    echo $BASE_DIR
    echo $cmd
    BASE_DIR=$__DIR__ $cmd
}

function install_systemd() {
    set -x
    local service=pgadmin4.service
    local target=/etc/systemd/system/$service

    # Always update service file
    CWD="$(pwd)"
    sed -e "s|\$CWD|$CWD|g" \
        -e "s|\$USER|$USER|g" etc/systemd/system/$service | \
        sudo tee "$target"

    sudo systemctl daemon-reload

    if systemctl is-enabled --quiet "$service"; then
        if systemctl is-active --quiet "$service"; then
            if ! sudo systemctl reload "$service"; then
                sudo systemctl restart "$service"
            fi
        else
            sudo systemctl start "$service"
        fi
    else
        sudo systemctl enable "$service"
        sudo systemctl start "$service"
    fi

    sudo systemctl status "$service"
}

function print_usage() {
    echo "Usage: $0 init|start [--daemon]|patch|patch_sqlalchemy|patch_config_local|install_systemd"
    exit
}

if [ $# -eq 0 ]; then
    print_usage
fi

while [ $# -ne 0 ]; do
    case $1 in
        init)
            init
            ;;
        patch)
            patch_sqlalchemy
            patch_config_local
            ;;
        patch_sqlalchemy)
            patch_sqlalchemy
            ;;
        patch_config_local)
            patch_config_local
            ;;
        start)
            shift
            start $*
            ;;
        install_systemd)
            install_systemd
            ;;
        *)
            print_usage
            ;;
    esac
    shift
done
