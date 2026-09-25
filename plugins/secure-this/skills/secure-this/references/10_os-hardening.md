---
last_verified: 2026-08-23
scope: macOS, for a machine running Claude Code
---

# OS-level hardening

Everything in `04_config-recipes.md` sits at the Claude Code layer. This file is the layer
underneath: the host itself. A sandbox rule that stops the agent reading a file is worth
much less if every other process on the machine can read it anyway.

**Rule this file enforces:** never report G1 (secrets out of reach) as PASS on Claude Code
config alone. Check the file's permissions and its physical location first.

The commands below are macOS. On Linux the same questions apply (disk encryption, file
modes, umask, synced directories, admin rights, outbound filtering); swap in the local
equivalents.

In the snippets, `KEYFILE` stands for your key file (whatever JSON or env file your scripts
read API keys from) and `SECRETS_DIR` for a local, non-synced directory you choose for it.

---

## Baseline audit commands

Run these first. They take ten seconds and set what everything else is worth.

```bash
sw_vers                                                          # OS version
fdesetup status                                                  # FileVault (disk encryption)
csrutil status                                                   # System Integrity Protection
spctl --status                                                   # Gatekeeper
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate  # firewall
id -Gn | grep -qw admin && echo "admin" || echo "standard"       # is this an admin account
dscl . list /Users UniqueID | awk '$2>=500 && $1!~/^_/ {print $1}' # other human accounts
umask                                                            # default perms on new files
```

Then the credential surface:

```bash
for f in "$KEYFILE" ~/.claude/settings.json ~/.claude.json \
         ~/.claude/*token*.json ~/.ssh ~/.aws/credentials; do
  [ -e "$f" ] && stat -f "%Sp  %Su:%Sg  %N" "$f"
done

# THE ONE PEOPLE MISS: is the config directory synced to a cloud?
ls -ld ~/.claude; readlink ~/.claude
```

---

## Finding 1: the config directory syncing to a cloud

**Common finding.** `~/.claude` (or the folder holding your key file) is a symlink into a
cloud-synced folder such as iCloud Drive, Dropbox or OneDrive, for example:

```
~/.claude -> ~/Library/Mobile Documents/com~apple~CloudDocs/.claude
```

Which means your key file, every OAuth token, and `settings.json` are all syncing to the
cloud. File permissions of `600` are irrelevant to this: the file is `600` on the local
disk **and also in the provider's data centre and on every device signed into that account.**

The blast radius stops being "someone with access to this machine" and becomes "someone with
the cloud account."

For iCloud, two Apple facts decide how bad it is:
- Without **Advanced Data Protection**, Apple holds keys that can access iCloud Drive contents
- With it on, they do not. Check System Settings > Apple Account > iCloud > Advanced Data Protection

**Immediate fix**, keeps the skills and settings syncing but takes the secrets out:

```bash
mkdir -p "$SECRETS_DIR" && chmod 700 "$SECRETS_DIR"           # a real local path, not synced
mv "$KEYFILE" "$SECRETS_DIR/"
mv ~/.claude/*token*.json "$SECRETS_DIR/" 2>/dev/null
chmod 600 "$SECRETS_DIR"/*
ln -s "$SECRETS_DIR/$(basename "$KEYFILE")" "$KEYFILE"        # scripts keep working
```

**Checked 2026-08-23 on iCloud Drive:** it does not follow symlinks. It stores the link itself
as a link, with its path intact, and never uploads the target. So the symlink syncs as a
harmless string while the secret stops leaving the machine, and every path in every script
still resolves. On another device the link simply dangles, which is correct behaviour.
Verify this for any other sync provider before relying on it.

**Verify it worked:**
```bash
readlink "$KEYFILE"    # should point into SECRETS_DIR
ls <synced copy of the config dir> | grep -i "key\|token"  # should be empty or symlinks only
```

---

## Finding 2: world-readable credential files

**Common finding.** An OAuth token file is `-rw-r--r--`, meaning a refresh token (often for
mail and file storage) is readable by any process running as this user.

```bash
chmod 600 ~/.claude/*token*.json "$KEYFILE"
chmod 700 ~/.ssh && chmod 600 ~/.ssh/*
find ~ -maxdepth 3 -name "*token*.json" -o -name "*credential*.json" 2>/dev/null \
  | xargs -I{} stat -f "%Sp %N" {}      # sweep for the ones you forgot
```

**Root cause:** `umask 022`, so every new file is created `644`. The token was not made
readable, it was born readable. Anything that writes a new token will do it again.

Fix it where tokens are written rather than globally, because a global `umask 077`
surprises other tooling:

```bash
( umask 077; python3 refresh_token.py )    # subshell, only this write is tight
```

---

## Finding 3: secrets in a plaintext file at all

A JSON file of keys is readable by **any process running as you, with no authentication**.
The Keychain is a different security model, not just a better file: on Apple Silicon it is
backed by the Secure Enclave.

**Minimal migration** for a single JSON store of many keys. One item, one helper, every
script fixed at once:

```bash
# store (omit the value after -w so it prompts, keeping it out of shell history)
security add-generic-password -a "$USER" -s claude-api-keys -U -w
# paste the whole JSON at the prompt, then press enter

# read
security find-generic-password -a "$USER" -s claude-api-keys -w
```

Python helper to replace every `open(KEYFILE)`:

```python
import json, subprocess
def keys():
    out = subprocess.run(
        ["security","find-generic-password","-a",__import__("os").environ["USER"],
         "-s","claude-api-keys","-w"],
        capture_output=True, text=True, check=True).stdout.strip()
    return json.loads(out)
```

Notes that matter:
- `-U` updates in place. Without it, re-adding the same service fails as a duplicate
- Never put the secret after `-w` on the command line: it lands in shell history and is
  briefly visible in the process list
- Per-key items are tidier but mean N migrations. One blob is the pragmatic move
- **Add `-T /usr/bin/security`** when creating the item, or scripts calling `security` get an
  interactive prompt instead of the value. `-A` allows every application and should not be used
- **A half-done migration looks finished.** Any script still reading the file keeps working
  perfectly, so nothing fails to tell you. Sweep for it:
  `grep -rl "$(basename "$KEYFILE")" ~/.claude/skills <your project dirs> 2>/dev/null`

---

## Finding 4: no outbound filtering

**Common finding.** Firewall disabled.

The important accuracy point: **macOS's built-in firewall is inbound only.** Turning it on
is worth doing, and it gives you no egress control at all.

```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on
```

For actual outbound control you need a third-party layer: **LuLu** (free, open source,
Objective-See) or **Little Snitch** (paid). Without one, Claude Code's egress allowlist
covers sandboxed Bash and nothing else on the machine.

---

## Finding 5: one admin account doing everything

**Common finding.** Single user, admin, running the agents.

The strongest containment available on a Mac, and the least used: **a separate standard
(non-admin) macOS user for agent work.** Different home directory, different keychain,
no admin rights, and process memory isolation between them enforced by the kernel.

Cost is real: separate logins, separate app setup, and switching accounts to work. Worth
it when an agent runs unattended against untrusted content; overkill for an interactive
session you are watching.

---

## Finding 6: what already has everything

Check **System Settings > Privacy & Security > Full Disk Access**.

If Terminal, your editor, or an automation tool is in that list, it can read every file on
the machine regardless of permissions, including other apps' data. A sandbox rule that
blocks the agent while the terminal it runs in holds Full Disk Access is a rule working
around a door that is already open.

Same page, check **Automation** for anything that can drive other apps.

---

## Good baseline, worth confirming rather than assuming

These are often already correct. Confirm each by running the command, never assume:

| Check | Expected |
|---|---|
| FileVault | On. Disk encrypted at rest |
| System Integrity Protection | Enabled |
| Gatekeeper | Assessments enabled |
| Key file permissions | `600` |
| `~/.claude.json` permissions | `600` |

FileVault matters more than it looks here: without it, every permission above is bypassed
by removing the drive.

---

## Moving a secret out does not undo the exposure

Once a credential has synced to a cloud, moving the file stops **future** exposure and changes
nothing about the past. Copies exist in the provider's storage and on every device that ever
synced, and deletion propagation is not the same as deletion.

If the exposure window was long or the account is high value, the honest fix is to **rotate the
key**, not to relocate the file. Relocate first because it is instant, then rotate on whatever
schedule the value of the key justifies.

## Priority order

1. **Secrets out of cloud sync.** Changes who can reach them, not just what can
2. **`chmod 600` every credential file**, then fix the umask at the write site
3. **Keychain migration.** The real fix for plaintext, and the prerequisite for masking
4. **Firewall on**, plus LuLu if egress control actually matters
5. **Full Disk Access review.** Free, and it can invalidate everything above
6. **Separate user account.** Strongest, most expensive, only for unattended work

---

## How this feeds the sweep

- **L4 the process** now also asks: what identity does this run as, is it admin, and does
  the terminal it runs in hold Full Disk Access
- **L5 the host** now also asks: are credentials `600`, are they in a synced directory, is
  FileVault on, and is anything filtering outbound
- **L7 the credential** now also asks: is this in a file or the Keychain, and if a file,
  what created it and with what umask
