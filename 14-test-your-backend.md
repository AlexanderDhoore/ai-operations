# 14 — Test your backend

<img src="assets/moods/14-test-bench.svg" alt="A stack of modules under a magnifying glass" align="right" width="112">

In [Assignment 13](13-automate-your-deployment.md), a green deployment told you
that your game was running. Would it still be green if a player action changed
the wrong person's state? Probably. This time you will make the **whole backend**
easier to change and build a test suite that tells you when its behavior changes.

## Start on a Git branch

Open **your game repository on your development server** in VS Code. The
server is where you work. A **Git branch** is where Git records your new
commits without moving `main`. That matters because pushing to `main` already
deploys your game.

In the game repository's terminal, run `git status`. If you have uncommitted
work, review it with your agent before switching branches. From a clean
working tree, run:

```bash
git switch main
git pull --ff-only
git switch -c assignment-14-backend-tests
git branch --show-current
```

This updates your local `main`, then `git switch -c` creates a branch from
that commit and switches to it. The last command should print
`assignment-14-backend-tests`. When resuming the assignment, use
`git switch assignment-14-backend-tests` without `-c` to return to the
existing branch. None of these commands pushes or deploys anything.

Leave production and its data alone. Keep your language and framework. You
do not need a new container setup or an Actions workflow for this assignment.

## Understand the test pyramid

![Four levels of the test pyramid, from calling one module directly to using a real browser](assets/14-test-pyramid.svg)

Suppose your backend is meant to reject an action and leave the game state
unchanged. You could open a browser and try every invalid input by hand. But
if the state changes, where is the mistake? Did the rule allow the action?
Did another module ignore the rejection? Or did the screen change even though
the server rejected the request? Each layer of the pyramid lets you ask a
different question about the same behavior.

**Unit tests: does this module make the right decision?** A unit is a piece of
code with one responsibility and an interface you can call. It need not be
one function or one class. In a unit test, call that interface directly with
a known input and assert the result you expect. For a rule with a limit, try
inputs below, at and above the limit. You can run all three cases without
starting the game, opening a database or calling an LLM. That makes these
tests fast, and a failure points you to a specific decision. It does not tell
you whether the rest of the backend uses that decision correctly.

**Integration tests: do the parts work together?** Now exercise the real
modules on both sides of an internal interface. For instance, call the code
that handles an action, let it consult the real rule, and read back the state
afterwards. The rule might correctly return a rejection while its caller
writes the proposed state anyway. Neither module's isolated tests necessarily
catch that disagreement. No HTTP server or browser is needed to test that
interaction. If the interaction you care about is with a database, use a
disposable test database so the real read and write code runs.

**API tests: does the running backend keep its promise to a client?** Start a
test instance and use the same public protocol as your frontend. Send an HTTP
request or a WebSocket message and inspect the reply or event. For a rejected
action, also read back the state through the API. A rejection message alone
does not prove that nothing changed. This crosses boundaries a direct module
call skips: the backend must decode the message, route it and deliver the
right result. It still tells you nothing about what the browser displays.

**Browser tests: does the user see the promised behavior?** Drive the real
page as a player would and assert something visible. Does a rejected action
leave the screen in the right state and explain what happened? This can catch
a frontend that treats an error response as success even when every backend
test passes. Browser automation is optional here. It is useful for checking
the complete interaction, not for repeating every boundary case in the UI.

The [test pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
is wide at the base because lots of small tests can cover variations cheaply.
Higher up, more parts have to be started, coordinated and reset, and there
are more places to look when a test fails. Use fewer broad tests to cover
risks that the narrow ones miss. **The width is not a quota, and the names
are not universal.** An API test can be a *system test* of the whole backend.
“API” tells you where the test enters, not whether the database or LLM is
real. When explaining your suite, say what you called, what actually ran and
what failure the test would catch.

## Map the backend before moving code

Your goal is to **refactor your backend into modules you can test separately**.
Refactoring means changing how the code is organized while keeping the behavior
its callers rely on. A module groups code that has one clear responsibility and
offers an interface: the functions or methods other code can call without
knowing how the module does its work.

Think back to the rejected action in the pyramid. If the rule that decides
whether to accept an action is buried in a request handler, you may have to
start the server just to try the rule with a different input. Give that
decision its own interface and both the handler and a unit test can call it.
The unit test can now check the decision directly. An API test still checks
that the running backend acts on it. That is the benefit you are looking for,
not a larger number of files.

![A client calls the public API. Inside one backend, modules call each other through internal interfaces.](assets/14-backend-boundaries.svg)

The diagram shows the distinction between the interface your frontend uses
and those inside the backend. The letters are not a layout to copy. To find
useful boundaries in **your** game, first map what the backend does today:

> Inspect our backend and the frontend code that calls it. List our public
> operations, who calls them and what each is supposed to do. Show me where
> those decisions live in the code today. Identify responsibilities that are
> mixed together and propose module boundaries. Point out ambiguous behavior
> for me to decide. Do not change files yet.

Compare the inventory with your game. Include the less visible operations,
such as chat and game tools where present. Decide what callers **should** be
able to rely on. Do not let the current implementation, or the agent that
wrote it, become the only authority on the expected result.

Before moving code, capture important existing behavior with API tests on
development. Give them their own backend instance and test state. This gives
you an outside view that should keep passing while the internals change.

Now use your map to refactor in small steps. Separate one responsibility,
run the tests that protect its existing behavior, then move on. Keep
boundaries that already work. A module might be a Python package, a
JavaScript module or a set of related classes. Your backend can still run
as a single application.

## Test each module and its collaborations

A **test runner** is the program you start to find and run your tests. You
write the checks, called *assertions*, that say what should happen. If a check
fails, the runner tells you which test failed and where. This is different
from the GitHub Actions runner in Assignment 13: that runner executes a job
on a machine. A test runner can run right here in your development terminal.

If your project already has a test command, use it. Otherwise, choose **one**
tool for your backend. Here are three options:

| Backend | Test runner | Command from the project root |
| --- | --- | --- |
| Python | [pytest](https://docs.pytest.org/en/stable/how-to/usage.html) lets you write test functions with ordinary `assert` statements. Install it in your development environment. | `python -m pytest` |
| Python | [unittest](https://docs.python.org/3/library/unittest.html) comes with Python. Write test methods in a `TestCase` class. | `python -m unittest discover` |
| Node.js | The built-in [node:test](https://nodejs.org/api/test.html) runner can run JavaScript tests without an extra package. | `node --test` |

Use the naming convention for your runner so it can find your files. On your
first run, check that the test you just wrote actually appears in the results.

For **each backend module**, write unit tests through its interface. A useful test reads like three short
statements: **given** a known starting state, **when** I perform this action,
**then** I expect this observable result. Cover ordinary behavior and relevant
boundaries or rejections. For a rejection, what must remain unchanged?

Name tests after the promise they check. Prefer an assertion about the result
over an assertion that three private helpers ran in a particular order. That
way the test still protects you after the next refactor. Google’s
[note on testing behavior](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
illustrates this distinction.

Keep unit tests quick and independent. For instance, pass a small stand-in for
an LLM client that returns a chosen reply or raises a timeout. You can then
exercise your application's handling of both outcomes without a key or a
network call. Do not replace the application logic you are trying to verify.

Look for interactions that unit tests miss. Where two real modules must agree
on a format, a state transition or an error, exercise them together in a focused
integration test. There is no benefit in duplicating every unit case at this
level. Choose a mistake that could survive both modules' unit tests.

## Test the complete public API

Return to your inventory. Cover **every public operation** through the actual
backend protocol, whether that means HTTP routes, WebSocket messages or another
interface. Do not call the handler directly and count it as a network test.
Assert what the client receives **and** what the operation promises to change.
A successful status or an open socket alone proves little.

For shared behavior, use separate clients where that distinction matters. Read
the state through the API after an action, or check which client received the
event and what it contained. Exercise relevant failure paths too. Compare the
tests with your inventory to spot operations that nobody has tested.

**Real software does not require production data.** A fresh instance of your
usual database, seeded with test records, is a real database. Never point
tests at the production database, game URL or saved files. Give tests a known
starting state and clean up after them, including after failure.

At this level you may use the real school inference service when the question
is whether your backend actually works with it. Use test inputs and supply the
key privately at runtime, never in Git, chat or logs. Check the promised
behavior, not an exact generated sentence. Keep live checks separately
selectable so a cluster outage does not prevent you from testing your own
logic. Document what is real, what is substituted and why.

## Optional: test through the browser

An API test starts on the server side of the screen. It can prove that the
backend returns the right result, but it cannot tell you whether clicking a
button sends the right request or whether the page displays the reply. A
**browser test** opens your actual frontend, performs an action as a player
would and checks what appears on screen. Automating this layer is optional.

To try it, pick one interaction from your own game that you normally check
by hand. Write down the starting state, what the player does and what they
should see afterwards. Then ask your agent to automate those steps:

1. Start your local test game with known test data and open it in a fresh
   browser session. Use your development test URL, not the public game.
2. Perform the interaction through the page. Find a control by its visible
   label or its role and name rather than by a CSS class that might change
   when you restyle it.
3. Assert the visible outcome you predicted. Wait for that outcome rather
   than sleeping for a fixed time. A successful click or HTTP response is
   not enough if the player still sees the old state.

[Playwright](https://github.com/microsoft/playwright) is an open-source tool that can
drive a real browser locally, even without a desktop window. Its
[testing guide](https://playwright.dev/docs/best-practices) shows how to find
controls and use assertions that retry while the page updates. Keep the many
variations of each game rule in your faster backend tests. Use the browser
where seeing the result is part of the promise.

## Make a change and leave the suite green

Pick one useful change to your own application. Agree on its intended effect
before asking the agent to implement it. Add or update the tests for that
effect. If an older test fails, decide whether the agreement really changed
or the code is wrong. Do not weaken an assertion just to make it pass.

Provide **one documented command** that runs the routine unit, integration
and API tests on development. It should prepare the isolated test backend,
wait until it is ready, run the checks and clean up. A failed assertion must
give the command a nonzero exit code. Run it twice: both runs should pass
without manual resets or reliance on a previous test's data. Finish with
working code and passing tests, not a broken commit for the next assignment.

## Explain your architecture

Put an **Architecture** section in your game's top-level README, or link from
there to a document in the repository. Include a **vector diagram** of your
actual backend. Use the real module names and label the arrows with what is
called or exchanged. A reader should be able to follow a frontend interaction
through the public API, into the responsible modules and back to the browser.

Alongside the diagram, explain each module's responsibility and interface.
Document the public operations, including requests or messages, responses and
relevant errors. Link to the tests that verify those contracts. Include the
local test command, any prerequisites and how to select live checks. Explain
how the frontend works even if you do not automate its tests.

Review the diff and the diagram against the code with your agent. Commit the
reviewed work to your project branch and update project memory.

At the oral defense, use your diagram to explain **how your backend fits
together and how you know it works**. Describe what the main modules are
responsible for and how they work together. Use an example from your test
suite to explain what you checked at the module level and what you verified
through the API. The focus is on your design and testing choices, not on
remembering implementation details.
