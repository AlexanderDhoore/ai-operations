#!/usr/bin/env bash
# Small teaching launcher. Run from the game's primary checkout on the server.
set -euo pipefail
usage() { echo 'Usage: bash scripts/worker.sh start ID TASK.md | status ID | result ID' >&2; exit 1; }
fail() { echo "$*" >&2; exit 1; }
[[ $# -ge 2 ]] || usage
action=$1
id=$2
[[ $id =~ ^[a-z0-9][a-z0-9-]{0,39}$ ]] || fail 'Use a short lowercase job ID with letters, digits and hyphens.'
repo=$(git rev-parse --show-toplevel)
[[ -d "$repo/.git" ]] || fail 'Run this in the primary checkout, not a worker worktree.'
job="$repo/.workers/$id"
tree="${repo}-workers/$id"

case "$action" in
  start)
    [[ $# == 3 ]] || usage
    command -v pi >/dev/null
    command -v screen >/dev/null
    task=$(realpath "$3")
    [[ -s "$task" ]] || fail 'Task file is missing or empty.'
    [[ -f "$repo/scripts/worker-role.md" ]] || fail 'Missing scripts/worker-role.md.'
    [[ -z $(git -C "$repo" status --porcelain) ]] || fail 'Review and commit the project before starting workers.'
    git -C "$repo" check-ignore -q .workers/probe || fail 'Add /.workers/ to .gitignore first.'
    [[ ! -e "$job" && ! -e "$tree" ]] || fail 'Job already exists. Inspect it and use a new ID for new work.'
    base=$(git -C "$repo" rev-parse HEAD)
    git -C "$repo" worktree add -b "worker/$id" "$tree" "$base"
    mkdir -p "$job/sessions"
    cp "$task" "$job/task.md"
    cp "$repo/scripts/worker-role.md" "$job/role.md"
    printf '%s\n' "$base" > "$job/base"
    printf '%s\n' "$tree" > "$job/worktree"
    # Include a repository identifier so identical job names in different games do not collide.
    session="aiops-$(printf '%s' "$repo" | cksum | cut -d ' ' -f 1)-$id"
    printf '%s\n' "$session" > "$job/screen"
    cat > "$job/run.sh" <<'RUN'
#!/usr/bin/env bash
set -uo pipefail
job=$1
tree=$2
printf 'running\n' > "$job/status"
cd "$tree" || { printf 'failed: cannot enter worktree\n' > "$job/status"; exit 1; }
# --approve trusts this reviewed project's resources for this invocation.
# --print executes one assignment and exits. It does not disable editing tools.
pi --provider vives --model qwen3.8-27b --thinking medium \
  --approve --print --session-dir "$job/sessions" \
  --append-system-prompt "$job/role.md" \
  "@$job/task.md" > "$job/output.log" 2>&1
code=$?
printf '%s\n' "$code" > "$job/exit-code"
if [[ $code == 0 ]]; then
  printf 'finished: review required\n' > "$job/status"
else
  printf 'failed: Pi exit code %s\n' "$code" > "$job/status"
fi
RUN
    printf 'starting\n' > "$job/status"
    screen -dmS "$session" bash "$job/run.sh" "$job" "$tree" || {
      printf 'failed: Screen launch\n' > "$job/status"
      fail "Screen could not launch. Inspect $job."
    }
    printf 'Started %s\nBranch: worker/%s\nWorktree: %s\nRecords: %s\n' "$id" "$id" "$tree" "$job"
    ;;
  status)
    [[ $# == 2 && -f "$job/status" ]] || fail 'Unknown job.'
    printf '%s: %s\n' "$id" "$(cat "$job/status")"
    printf 'Worktree: %s\nScreen: %s\n' "$(cat "$job/worktree")" "$(cat "$job/screen")"
    ;;
  result)
    [[ $# == 2 && -f "$job/status" ]] || fail 'Unknown job.'
    cat "$job/status"
    if [[ -f "$job/output.log" ]]; then cat "$job/output.log"; fi
    ;;
  *) usage ;;
esac
