
html:
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

all: html pdf epub

pdf:
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-pdf \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

epub:
	docker run -it -u $(id -u):$(id -g) -v `pwd`:/documents/ asciidoctor/docker-asciidoctor asciidoctor-epub3 \
	   --destination-dir /documents/output \
	   --verbose \
	   --doctype book \
	   src/index.adoc

pull:
	docker pull asciidoctor/docker-asciidoctor
