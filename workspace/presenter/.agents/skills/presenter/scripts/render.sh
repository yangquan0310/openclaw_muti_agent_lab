#!/usr/bin/env bash
# Quarto PPT 渲染小工具
# 用法：
#   render.sh deck.qmd pptx           # 渲染为 pptx
#   render.sh deck.qmd revealjs       # 渲染为 revealjs
#   render.sh deck.qmd both           # 同时输出
#   render.sh deck.qmd pptx --preview # 渲染并预览
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "用法: $0 <deck.qmd> <pptx|revealjs|both> [--preview]"
  exit 1
fi

DECK="$1"
TARGET="$2"
PREVIEW="false"

if [[ "${3:-}" == "--preview" ]]; then
  PREVIEW="true"
fi

case "$TARGET" in
  pptx)
    if [[ "$PREVIEW" == "true" ]]; then
      quarto preview "$DECK" --to pptx
    else
      quarto render "$DECK" --to pptx
    fi
    ;;
  revealjs)
    if [[ "$PREVIEW" == "true" ]]; then
      quarto preview "$DECK" --to revealjs
    else
      quarto render "$DECK" --to revealjs
    fi
    ;;
  both)
    quarto render "$DECK"
    ;;
  *)
    echo "未知目标: $TARGET（仅支持 pptx / revealjs / both）"
    exit 2
    ;;
esac
