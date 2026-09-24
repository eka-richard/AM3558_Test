# Makefile
TARGETS=testApp

all: $(TARGETS)

# c-program: c-program.c
# 	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@ 

cpp-program: testApp.cpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGETS)