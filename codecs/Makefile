CC = gcc
CFLAGS =
INSTALL_PREFIX = /usr/local/lib
HEADER = rtpsbc.h

ifndef PLATFORM
	PLATFORM = mmx
endif

OBJS = rtpsbc.o sbc.o sbc_primitives.o sbc_primitives_$(PLATFORM).o

TARGET = librtpsbc.so

%.o: %.c
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) -shared $(OBJS) -o $(TARGET)

.PHONY: all clean

all: $(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	cp $(TARGET) $(INSTALL_PREFIX)
	cp $(basename $(TARGET)).pc $(INSTALL_PREFIX)/pkgconfig
	cp $(HEADER) /usr/local/include
	ldconfig
