INSTALL ?= install
PREFIX ?= /usr/local/

all: hello

hello: hello.o
	$(CC) -o $@ $<

install: all
	$(INSTALL) -D -m755 hello $(PREFIX)/bin/hello
