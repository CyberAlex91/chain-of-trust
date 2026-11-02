# Chain of Trust — Training Lab

Controlled supply-chain security exercise.

The local utils-lib package demonstrates build-time code execution by
creating a harmless pwned.txt marker in the current user's home directory.
Do not install it outside a disposable training environment.

The dependency workflow checks an explicit package allowlist before
installing local, hash-pinned wheels. This is a targeted policy check,
not a general malware detector.

No real credentials or secrets are included.
