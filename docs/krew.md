# kubectl plugin without Python (standalone binary and krew)

Every release ships a standalone `kubectl-sift` for Linux (amd64, arm64), macOS (Intel, Apple silicon) and
Windows (amd64). No Python needed. Put it on your `PATH` and kubectl finds it as `kubectl sift`.

| | |
|---|---|
| Includes | every CLI command (`diagnose`, `explain`, `changes`, `lint`, `preflight`, `upgrade-check`, `cost`, `drill`, ...) and AI explanations with Ollama, OpenAI-compatible endpoints or Anthropic |
| Not included | `serve` (web dashboard) and `mcp` (AI assistants): install with `pip install "kubesift[all]"` or use the Helm chart |
| Linux | glibc 2.28 or newer: RHEL/Rocky 8+, Amazon Linux 2 and 2023, Ubuntu 20.04+, Debian 10+ (not Alpine/musl: use pip or the image) |

## Install with one line

```bash
# Linux and macOS (installs to ~/.local/share/kubesift, links kubectl-sift and kubesift into your PATH)
curl -sSfL https://raw.githubusercontent.com/OpeyemiAdeniji/KubeSift/main/scripts/install.sh | sh
```

```powershell
# Windows
irm https://raw.githubusercontent.com/OpeyemiAdeniji/KubeSift/main/scripts/install.ps1 | iex
```

Both check the download against the release's SHA-256 before installing. `KUBESIFT_VERSION=v2.1.7` pins a
version. Read the script first if you prefer: it is short.

## Install from a release by hand

```bash
# Linux amd64 (other files: kubectl-sift_linux_arm64.tar.gz, _darwin_amd64, _darwin_arm64, _windows_amd64.zip)
curl -sSLO https://github.com/OpeyemiAdeniji/KubeSift/releases/latest/download/kubectl-sift_linux_amd64.tar.gz
tar -xzf kubectl-sift_linux_amd64.tar.gz            # creates ./kubectl-sift/
sudo mv kubectl-sift /opt/kubectl-sift && sudo ln -s /opt/kubectl-sift/kubectl-sift /usr/local/bin/kubectl-sift
kubectl sift diagnose
```

Check the download against its `.sha256` file from the same release. On macOS, a file downloaded with a browser is
quarantined by Gatekeeper; `curl` downloads (and krew) are not. If you used a browser:
`xattr -dr com.apple.quarantine kubectl-sift`.

## Install with krew

KubeSift has its own krew index (this repository), so krew installs and upgrades it like any other plugin:

```bash
kubectl krew index add kubesift https://github.com/OpeyemiAdeniji/KubeSift.git
kubectl krew install kubesift/sift
kubectl sift diagnose
```

krew prints a notice that plugins from custom indexes are not reviewed by the krew team; that is expected for
any index other than the central one. Each release's archives are checksummed in the manifest, and krew checks them.
`kubectl krew upgrade` then picks up new releases. To remove it: `kubectl krew uninstall sift` and
`kubectl krew index remove kubesift`.

Any single release can also be installed straight from its manifest, without adding the index:

```bash
kubectl krew install --manifest-url=https://github.com/OpeyemiAdeniji/KubeSift/releases/latest/download/sift.yaml
```

## Maintainers: how the index is kept up to date

A krew index is a git repository with a `plugins/` folder; krew reads it from the default branch. The release
workflow builds `sift.yaml` (each archive's URL and SHA-256), attaches it to the GitHub release and copies it to
`plugins/sift.yaml` on `main`, so the index always points at the newest release. It never moves backwards: releasing
an older patch line leaves the index alone.

`tests/test_krew_manifest.py` checks that `plugins/sift.yaml` keeps krew's rules (a tagline of 50 characters or
fewer, no usage text in the description or caveats, all five platforms).

KubeSift is not in the central krew index (kubernetes-sigs/krew-index); it uses its own index as above.
