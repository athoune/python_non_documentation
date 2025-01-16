
html: png svg
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc
	./patch.py
	rm output/index.html
	mv output/index_patched.html output/index.html

output/image:
	mkdir -p output/image

png: output/image
	pngcrush -d output/image src/images/*.png

svg: output/image
	./node_modules/.bin/svgo -rf src/images -o output/image

all: html book epub

pdf: png svg
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-pdf \
	   -a pdf-theme=pied \
	   -a pdf-themesdir=resources/themes \
	   -a pdf-fontsdir=resources/fonts \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

book: pdf
	# https://github.com/pdfcpu/pdfcpu
	pdfcpu booklet -- output/book.pdf 4 output/index.pdf

epub: png svg
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-epub3 \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

pull:
	docker pull asciidoctor/docker-asciidoctor

publish:
	rsync -avz --delete-after output/* $(DEST)
