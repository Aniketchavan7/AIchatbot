# API Rate Limiting Architecture

## Overview
- Distributed Redis token bucket limiter (60 requests/minute/IP)
- Tiered API key allowances for authenticated enterprise users
- Exponential backoff retry-after response headers
