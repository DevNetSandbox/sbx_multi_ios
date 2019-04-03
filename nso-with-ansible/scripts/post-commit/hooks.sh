#!/bin/bash
set -e

if [ $# -gt 0 ]; then
    case "$1" in
        --post-commit)
            cat << EOF
begin post-commit
end
EOF
            exit 0
            ;;
        *)
            echo
            echo "Usage: $0 [--post-commit]"
            echo
            echo "  --post-commit Mandatory for post-commit scripts"
            exit 1
            ;;
    esac
else
  mkdir -p logs/post_commit
  log=$(echo "logs/post_commit/post_commit_$(date).log" | sed -e 's/ /_/g')
  echo "Peforming Post-Commit hooks..." > $log
  exit 0
fi
