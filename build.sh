#!/bin/sh
# Full build of main.tex: bibliography, glossaries, and cross-references.
set -e
cd "$(dirname "$0")"

pdflatex -interaction=nonstopmode -halt-on-error main
bibtex main
makeglossaries main
pdflatex -interaction=nonstopmode -halt-on-error main
pdflatex -interaction=nonstopmode -halt-on-error main

# Only reached on success (set -e), so main.log is kept when a build fails.
rm -f main.aux main.log main.bbl main.blg main.toc main.lof main.lot main.out \
      main.glo main.gls main.glg main.acn main.acr main.alg main.ist main.xdy \
      main.fls main.fdb_latexmk main.synctex.gz

echo "Done: main.pdf"
