
html:
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc
	mkdir -p output/image
	cp image/*.png output/image/

all: html book epub

pdf:
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-pdf \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

book: pdf
	# https://github.com/pdfcpu/pdfcpu
	pdfcpu booklet -- output/book.pdf 4 output/index.pdf

epub:
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-epub3 \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

pull:
	docker pull asciidoctor/docker-asciidoctor

publish:
	rsync -avz --delete-after output/* $(DEST)
