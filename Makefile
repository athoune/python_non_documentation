
html: png svg
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc
	cp console_webworker.js output/
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
	   -a scripts=cjk \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc
	pdfcpu pagemode set output/index.pdf UseOutlines
	pdfcpu properties add output/index.pdf 'Author = Mathieu Lecarme'
	pdfcpu viewerpref set output/index.pdf '{"UseOutlines": true}'
	pdfcpu optimize output/index.pdf
	mv output/index.pdf output/python_non_documentation.pdf

book: pdf
	# https://github.com/pdfcpu/pdfcpu
	pdfcpu booklet -- output/book_python_non_documentation.pdf 4 output/python_non_documentation.pdf

epub: png svg
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-epub3 \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc
	mv output/index.epub output/python_non_documentation.epub

pull:
	docker pull asciidoctor/docker-asciidoctor

publish:
	rsync -avz --delete-after output/* $(DEST)

serve:
	python3 -m http.server -b localhost -d output/ 3003
