#!/usr/bin/env python3
"""Backward-compatible entry point — delegates to metrics.__main__."""

from metrics.__main__ import main

if __name__ == "__main__":
    main()
