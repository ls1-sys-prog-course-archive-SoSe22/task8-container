# Set you prefererred C compiler here,
# on github actions gcc-7 till gcc-10 are pre-installed
CC ?= gcc-10
CFLAGS ?= -g -Wall -O2
CXX ?= g++-10
CXXFLAGS ?= -g -Wall -O2
CARGO ?= cargo
RUSTFLAGS ?= -g

# this target should build all executables for all tests
all:
	@echo "Please set a concrete build command here"
	false

# C example:
#all:
#	$(CC) $(CFLAGS) -o task-name task-name.c

# C++ example:
#all:
#	$(CXX) $(CXXFLAGS) -o task-name task-name.cpp

# Rust example:
#all:
#	$(CARGO) build --release

# Usually there is no need to modify this
check: all
	$(MAKE) -C tests check
