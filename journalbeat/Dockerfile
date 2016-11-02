FROM golang:1.7
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

RUN apt-get update \
    && apt-get install patch libsystemd-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY 0001-Add-Path-in-config-to-let-NewJournalReader-select-journal-dir.patch /tmp/0001.patch
COPY 0002-Add-config-option-to-specify-journal-path.patch /tmp/0002.patch

RUN mkdir -p /go/src/github.com/mheese/journalbeat \\
    && cd /go/src/github.com/mheese/journalbeat \
    # Clone journalbeat
    && git clone --depth 1 https://github.com/mheese/journalbeat.git . \
    # Download dependencies
    && go get -d -v ./... \
    # Apply first patch: Add `Path` to `JournalReaderConfig`
    && (cd vendor/github.com/mheese/go-systemd && patch -p1 < /tmp/0001.patch) \
    # Apply second patch: Expose `Path` in Journalbeat config
    && patch -p1 < /tmp/0002.patch \
    # Build the binary
    && go build . \
    # Move the binary
    && chmod +x journalbeat \
    && mv journalbeat /go/bin/journalbeat \
    # Cleanup
    && rm -rf /go/src/github.com

WORKDIR /go
CMD ["journalbeat", "-help"]

