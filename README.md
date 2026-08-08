# Job Search Automation

A personal, self-hosted tool to track my job applications and stay on top of new postings, built as part of my transition into IT/Systems Business Analyst and AI Workflow Automation roles.

## Why I built this

Job hunting at volume is hard to track by memory — which applications are where, what stage, what each role even was. Job hunting is also challenging timing wise: knowing about a new opening quickly can matter as much as the application itself. This tool tracks the status of my applications and stay up to date with new matching postings, using content found in email to update status automatically. It's also a way to strengthen my hands-on AI/automation skills and build a demonstrable project.

## How it works (planned)

- Reads my Gmail inbox (read-only) to detect application-related emails
- Uses an LLM to classify each email (applied / interview / rejection) and extract key dates
- Searches Sweden's public JobTech API for new matching postings
- Tracks everything in one place

## Status

Early build — environment and repo being set up, features not yet built.

## Why this repo is public

This is a personal, self-hosted tool — not a multi-user product, built against my own Gmail account. It's public as a demonstration of how I approach building software: scoping requirements, shipping incrementally, and documenting decisions along the way.