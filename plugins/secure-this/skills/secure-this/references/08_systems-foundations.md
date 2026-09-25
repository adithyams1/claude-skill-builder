---
captured: 2026-08-19
type: primer (foundations notes, not a control catalogue)
purpose: shared vocabulary. When explaining a finding, pitch at this level and
  reuse these exact terms. Consistency with this mental model is worth more than
  precision gains.
---

# Systems & Security Foundations

A plain-language primer on OS and security fundamentals, written by the skill's author
while learning them. Kept in the author's words.

---

## 1. CPU

The CPU executes instructions.

A computer has many physical components - CPU, RAM, SSD, motherboard, etc. The CPU is
specifically the execution machinery.

**Core:** an individual execution unit inside the CPU. If you have 8 cores, roughly 8
runnable threads can execute simultaneously.

## 2. Operating System

The OS manages the computer's resources and provides services to applications. It sits
between applications and the hardware.

Major responsibilities: process management, memory management, file/storage management,
device/I/O management, networking, users and permissions, security, resource allocation.

## 3. Kernel

The kernel is the privileged core of the OS.

Applications normally run in **user mode**. When an application needs a privileged
operation, it makes a **system call**, which enters **kernel mode**.

```
Application
    |
System call
    |
Kernel
    |
Hardware/resource
```

**Kernel mode** is not a separate program. It is a privileged CPU execution mode that
allows kernel code to perform operations ordinary user-mode code cannot.

---

# Processes

## 4. Program vs Process

A **program** is code stored somewhere, such as `research.py`.

Running it creates a **process**: `python research.py`

A process has: PID, memory, environment variables, working directory, user identity,
permissions, file descriptors, threads.

## 5. Working Directory

The working directory is the process's current directory. Relative paths are interpreted
from there.

```
working directory: /project
open("data/results.txt")   ->   /project/data/results.txt
```

It does NOT mean the process is physically restricted to that directory. **Sandboxing is
what can impose that kind of restriction.**

## 6. Environment Variables

Environment variables are values provided to a process's environment.

```
API_KEY=abc123
```

A child process can generally inherit the parent's environment.

**Important:** environment variables are not automatically a security boundary. If a
process has the environment containing an API key, that key is available to that process.

## 7. Process Memory Isolation

Each process normally has its own virtual address space.

```
Process A -> Memory A
Process B -> Memory B
```

B cannot simply reach into A's memory. Even if A = Alice and B = Alice, they still have
separate process memory.

**Same user does not mean shared memory.**

However, sufficiently privileged processes can sometimes inspect or interfere with other
processes.

---

# Processes Working Together

## 8. Parent and Child Processes

A process can create another process.

```
Claude Code
    |
    +-- Python child process
```

The child commonly inherits: user identity, environment, working directory, some open
file descriptors. **But memory remains isolated.**

## 9. IPC - Inter-Process Communication

Processes can't normally reach into each other's memory. They communicate through pipes,
sockets, shared memory, message queues, pub/sub systems.

```
Process A -> communication mechanism -> Process B
```

If the communication mechanism is compromised or improperly secured, information flowing
through it can potentially be exposed.

## 10. Pipes

A traditional pipe is commonly used for local process-to-process communication.

```
A ---------> B
```

A writes; B reads. Pipes are typically local, and a classic Unix pipe is one-way. Two-way
communication can be constructed using multiple pipes or other mechanisms.

## 11. Shared Memory

Two processes can be given access to the same memory region. Extremely fast, but
introduces synchronization problems.

If A and B modify the same data simultaneously, you can get **race conditions**. Hence
locks, mutexes, semaphores.

```
A --+
    +-- Shared memory
B --+
```

---

# Threads & CPU

## 12. Threads

A process can contain multiple threads. Threads within the same process **share the
process's memory**.

```
Claude Code
+-- Thread A
+-- Thread B
+-- Thread C
```

## 13. CPU Scheduling

12 runnable threads, 8 CPU cores: only roughly 8 execute simultaneously. The rest wait
for CPU time.

But not every thread needs a CPU at every moment. A thread might be computing, waiting for
network data, waiting for disk I/O, waiting for another process, or sleeping.

**50 tasks does not equal 50 CPU-heavy tasks.**

## 14. Context Switching

The OS scheduler can switch the CPU from one thread to another.

```
Thread A -> save state -> load Thread B state -> Thread B executes
```

The OS preserves enough state for A to continue later. Context switching has some
overhead, but it is fundamental to multitasking.

---

# I/O

## 15. I/O - Input/Output

I/O means communicating with something outside the CPU: reading a file, writing a file,
network requests, keyboard input, storage operations.

```
Python -> "Read this file" -> Kernel -> SSD
```

While Python waits for the SSD or network, the CPU can work on another thread.

**CPU-bound:** "I need CPU time to calculate."
**I/O-bound:** "I'm mostly waiting for something else."

Extremely relevant to Claude Code, because many agent operations involve network/API
waiting.

---

# Memory

## 16. Virtual Memory

Virtual memory gives each process its own virtual address space. The OS and the CPU's
memory-management hardware map virtual addresses to physical memory. This is one of the
mechanisms behind process memory isolation.

## 17. RAM vs Swap

RAM is physical memory. If memory becomes constrained, macOS can move some inactive
memory to SSD storage. That is **swap**, and it is much slower than RAM.

High memory pressure + substantial swap + noticeable slowdown = memory bottleneck.

---

# Permissions & Security

## 18. User Identity

Processes run under an identity.

```
Alice
+-- Claude Code
+-- Python
```

If Python is launched by Claude Code and nothing changes its identity, Python generally
runs with Alice's permissions.

## 19. Permissions

Permissions determine what that identity can access.

```
Alice
+-- project files          OK
+-- Documents              OK
+-- another user's files   NO
```

Same user -> potentially similar filesystem access.
Same user -> does NOT mean shared process memory.

## 20. Sandboxing

Sandboxing adds restrictions around a process **beyond** its normal user permissions.

```
Alice's normal permissions
        |
Claude Code sandbox
        +-- /project     OK
        +-- /tmp         OK
        +-- /Secrets     NO
        +-- Documents    NO
```

The process can try to access a restricted resource. The OS/security mechanism can deny
the operation.

**Key principle:**
- Identity: who are you?
- Permissions: what can you normally access?
- Sandbox: what additional restrictions apply to this process?

---

# Containers

## 21. Containers

Containers provide isolated environments while generally sharing the host kernel.

```
Host kernel
+-- Container A -> App A
+-- Container B -> App B
```

A compromise of Container B should not automatically compromise Container A. The attacker
still needs to cross the isolation boundary.

## 22. Namespaces

Linux namespaces help give containers their own views of the system: what processes can I
see, what network interfaces, what filesystem.

**Namespaces -> what can I see?**

## 23. cgroups

cgroups control resource usage.

```
Container A
+-- CPU       -> 2 cores
+-- RAM       -> 4 GB
+-- Processes -> 100
```

**Namespaces -> isolation/view. cgroups -> resource limits.**

cgroups also help reduce the blast radius of a compromised or runaway workload. They do
not prove that something is an attack; monitoring is needed for that.

---

# Networking

## 24. Sockets

A socket is a communication endpoint. Unlike a traditional pipe, sockets can communicate
two-way, and can work locally or across a network. That is why applications use sockets to
communicate with APIs.

## 25. IP Address + Port

```
10.0.0.5:443
```

`10.0.0.5` -> destination machine/address. `443` -> network port where a service is
listening.

A machine can have many services:

```
10.0.0.5
+-- :22
+-- :443
+-- :5432
+-- :8000
```

A port is just a number; conventions associate certain ports with common services.

## 26. TCP vs UDP

**TCP:** reliable delivery, ordered data, retransmission, flow/congestion control.
**UDP:** sends individual datagrams without TCP's built-in guarantees. Useful when low
latency and simplicity matter more than guaranteed delivery.

## 27. DNS

DNS translates names into IP addresses.

```
api.example.com -> DNS -> 10.0.0.5
```

DNS -> where is it? IP -> which machine? Port -> which service?

---

# HTTPS & TLS

## 28. HTTP

HTTP is a web communication protocol. It defines how clients and servers exchange requests
and responses. Example: `POST /research`

## 29. HTTPS

HTTPS is essentially **HTTP over TLS**.

TLS provides encryption, integrity, and server authentication.

HTTPS is not simply "HTTP + certificate." The certificate is one component of TLS.

## 30. TLS Certificates

```
Client -> Server -> server sends certificate -> client verifies it
```

The certificate helps establish: "this server is authorized for api.example.com."

Your computer checks: domain name, expiration, signature, certificate chain, trusted CA.

## 31. Root Certificate Authority

Your OS/browser has a trust store containing trusted root CA certificates.

```
Trusted Root CA -> Intermediate CA -> api.example.com certificate
```

Your computer trusts the root, which allows it to validate the chain. A CA is like a
cryptographic notary/stamp.

**Important:** a CA saying "this certificate belongs to api.example.com" does NOT mean
"this API is a good or trustworthy application." It authenticates the domain/server
identity according to the CA's validation process.

## 32. TLS vs API Authentication

One of the most important distinctions.

**TLS asks:** "am I talking to the legitimate server?"
**API key asks:** "is this client/account authorized to use my API?"

```
Client
  | TLS
  v
"Are you really api.example.com?"
  |
  v
Secure connection
  | API key
  v
"Who are you / are you authorized?"
```

TLS encrypts the communication in both directions. The API key authenticates the
client/account to the API.

---

# The Big Security Model

```
                     APPLICATION
                          |
                       PROCESS
                          |
             +------------+------------+
             |                         |
          Memory                  User identity
             |                         |
       isolated from             permissions
        other processes               |
                                   sandbox
                                      |
                                  container
                                  +---+---+
                                  |       |
                            namespaces  cgroups
                            what I see  what I use
                                  |
                               NETWORK
                                  |
                         DNS -> IP -> Port
                                  |
                               Socket
                                  |
                             TCP / UDP
                                  |
                                TLS
                                  |
                               HTTPS
                                  |
                              API key
```

The security philosophy tying it all together:

- **Least privilege** - give a component only what it needs
- **Isolation** - keep components from reaching each other unnecessarily
- **Defense in depth** - don't rely on one security boundary
- **Blast-radius reduction** - assume something eventually gets compromised; limit how
  much damage it can cause

---

# Bridge to this skill (added by secure-this, not part of the original notes)

How the foundations above map onto the controls this skill recommends. Use these
crossings when explaining a finding, so the explanation lands on vocabulary the reader already has.

| Foundation concept | Control it explains |
|---|---|
| Kernel mode + system calls (#3) | Why `denyRead` holds. The refusal happens at the syscall, below the program, so no tool choice escapes it |
| Child inherits identity + environment (#8, #18) | Why sandbox rules cover a Python script started by Bash, and everything it starts in turn |
| Environment variables are not a boundary (#6) | Why moving keys to env vars alone changes nothing. Masking is the separate step that matters |
| Working directory is not a restriction (#5) | Why "the skill runs in its own folder" is not containment |
| Sockets + IP/port (#24, #25) | What the egress proxy actually inspects when it allows or refuses a connection |
| TLS provides encryption (#29) | Why `tlsTerminate` is required for credential masking. The proxy must decrypt to substitute the sentinel |
| TLS vs API key (#32) | The cleanest explanation of masking: TLS proves the server, the key proves the client, and only the key needs hiding from the process |
| Blast-radius reduction (philosophy) | The entire grading model. Grade answers how bad; leverage answers what to fix first |
