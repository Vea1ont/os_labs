#!/usr/bin/env bash
# collect-info.sh — сбор диагностики для технической поддержки

set -uo pipefail

OUT="sysinfo-$(hostname)-$(date +%F-%H%M).txt"
: >"$OUT"   # создать пустой файл отчёта

# Прогресс для клиента: только на экран (stderr), в файл не попадает.
say() { printf '%s\n' "$*" >&2; }

# Выполнить команду с таймаутом и записать вывод в отчёт.
# Использование: run "Заголовок" секунды 'команда с аргументами'
run() {
    local title=$1 tmo=$2 cmd=$3 rc
    printf '\n===== %s =====\n' "$title" >>"$OUT"

    if ! command -v "${cmd%% *}" >/dev/null 2>&1; then
        printf '(команда %s недоступна)\n' "${cmd%% *}" >>"$OUT"
        return 0
    fi

    timeout "$tmo" bash -c "$cmd" >>"$OUT" 2>&1
    rc=$?
    if [ "$rc" -eq 124 ]; then
        printf '(команда не уложилась в %s с — таймаут)\n' "$tmo" >>"$OUT"
    elif [ "$rc" -ne 0 ]; then
        printf '(команда завершилась с кодом %s)\n' "$rc" >>"$OUT"
    fi
    return 0
}

main() {
    say "Собираю общие сведения..."
    run "Система"   5 'uname -a'
    run "Аптайм"    5 'uptime'
    run "ОС"        5 'cat /etc/os-release'
    run "Процессор" 5 'lscpu'

    say "Снимаю замеры нагрузки..."
    run "Нагрузка за 5 секунд" 10 'vmstat 1 5'
    run "Топ по памяти" 5 'ps -eo pid,user,%mem,%cpu,comm --sort=-%mem | head -11'
    run "Топ по процессору" 5 'ps -eo pid,user,%mem,%cpu,comm --sort=-%cpu | head -11'

    say "Снимаю замеры дисков..."
    run "Диски (свободное место)" 5 'df -h'
    run "Диски (свободные inode)" 5 'df -i'

    printf '%s\n' "$PWD/$OUT"
}

main "$@"