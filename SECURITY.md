# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub's security-advisory feature for this repository. Do not open a public issue containing credentials, exploit details, private paths, or user data.

Include:

- affected tool and version or commit;
- operating system and Hermes version;
- reproduction steps using non-sensitive test data;
- expected versus observed behavior;
- potential impact.

## Scope

Security-sensitive areas include:

- filesystem writes outside an authorized directory;
- symlink, junction, or path-traversal escapes;
- credential or private-data exposure;
- unsafe command construction;
- unintended network transmission;
- destructive behavior without an explicit approval boundary;
- prompt or content handling that can override trusted instructions.

## User responsibility

Inspect tools before installing them, keep Hermes and dependencies updated, and test unfamiliar tools on a separate Hermes profile before enabling them in a primary environment.
