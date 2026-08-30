# Job Search Automation

A personal, self-hosted tool to track my job applications and stay on top of new postings, built as part of my transition into IT/Systems Business Analyst and AI Workflow Automation roles.

## Why I built this

Job hunting at volume is hard to track by memory — which applications are where, what stage, what each role even was. Job hunting is also challenging timing wise: knowing about a new opening quickly can matter as much as the application itself. This tool tracks the status of my applications and stay up to date with new matching postings, using content found in email to update status automatically. It's also a way to strengthen my hands-on AI/automation skills and build a demonstrable project.

## How it works

- Reads my Gmail inbox (read-only) to detect application-related emails, with automatic re-authorization if the access token expires
- Uses an LLM to classify each email (applied / interview / rejection) and extract key details (company, role, date)
- Searches Sweden's public JobTech API (Arbetsförmedlingen) for new matching postings
- Tracks everything across two linked views: applied jobs and job opportunities. If an opportunity is applied to, it's automatically removed from the opportunities list

## Status

- Gmail inbox integration complete, including automatic token reauthorization if expired
- LLM email classification complete
- JobTech API (Arbetsförmedlingen) search integration complete
- Two-table database in place, linking applied jobs and opportunities so applying to a job removes it from the opportunities list
- Next: building the dashboard/frontend

## Why this repo is public

This is a personal, self-hosted tool — not a multi-user product, built against my own Gmail account. It's public as a demonstration of how I approach building software: scoping requirements, shipping incrementally, and documenting decisions along the way.