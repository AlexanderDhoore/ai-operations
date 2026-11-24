# 14 — Test your backend

<img src="assets/moods/14-test-bench.svg" alt="A stack of modules under a magnifying glass" align="right" width="112">

In [Assignment 13](13-automate-your-deployment.md), a green deployment told you
that your game was running. It did not tell you whether a player action
changed the right person's state. In this assignment you will map your
**whole backend** and refactor it into modules. You will test each module
first, then check how the modules work together, and finally test the running
backend as a client. You will use that suite to make a change to your own game.

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

Keep your language and framework. All work stays on development, with
separate test data. No new containers or Actions workflow are needed.

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
test passes. You will test the backend through its API in this assignment.
Automating the browser interaction is optional.

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

Review the inventory yourself. Distinguish what the frontend calls from what
the backend calls internally, such as tools made available to the model.
Decide what each caller **should** be able to rely on. An unexpected result
in today's code is something to discuss, not automatically something to
preserve in a test.

## Start with unit tests

Pick one responsibility from your map, ideally a decision your backend can
make from its inputs alone. If it is buried in a request handler, extract
it into a function or module and have the handler call it. If it already
has a clear interface, leave it where it is. Your first test will call that
code directly. You do not need to start a server.

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

Write a test for the decision you picked: **given** this starting state,
**when** I call the module with this input, **then** I expect this result.
Run it and check that the runner actually found your test. Add a boundary
case or a rejection. For a rejection, what must remain unchanged?

Repeat for **each backend module**, extracting one responsibility at a time
and rerunning the tests as you go. Keep boundaries that already work. A
module might be a Python package, a JavaScript module or a set of related
classes. They can all remain part of one application.

Name tests after the promise they check. Prefer an assertion about the result
over an assertion that three private helpers ran in a particular order. That
way the test still protects you after the next refactor. Google’s
[note on testing behavior](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
illustrates this distinction.

### When should you replace a dependency?

A **dependency** is something a module relies on, such as a clock, a
database or a model service. In a unit test, keep the module itself real.
Replace a dependency when using it would make the test slow or its outcome
hard to control.

A **stub** supplies an outcome: it can report a timeout so you can check
what the player sees without waiting for the model service to fail. A
**mock** lets you check an interaction instead: when a player submits an
empty message, does the backend reject it without calling the service?

## Test how modules work together

A stub can show how one module reacts to an answer. It cannot tell you
whether the real module on the other side gives that answer. Pick an
interaction from your map where a misunderstanding would matter. For
example, if one module rejects an action, does its caller leave the state
alone? Write an integration test that runs both real modules and checks the
outcome. Cover other important interactions without repeating every unit case.

## Test the complete public API

So far, your tests have called backend code directly. Now start the actual
backend and test it from the outside. Use its existing API, not a second API
built for the tests.

Have your test runner manage the server's lifetime. Put the setup and
cleanup in one shared helper (often called a *fixture*):

1. Prepare isolated test state. If the game uses a database, create a
   disposable test database and seed it with known records. For an in-memory
   game, a fresh instance may be enough. Never point tests at production.
2. Start the backend on development, bound to `127.0.0.1` on a free port.
   Pass its address to the test client. Wait for it to accept requests, with
   a timeout that fails the test setup if the server never becomes ready.
3. Give each test a known starting state. When the suite finishes, stop the
   test server and remove its temporary data, even if an assertion failed.

Use your inventory to cover **every public operation** through the same
HTTP routes, WebSocket messages or other protocol your frontend uses.
Assert what the client receives **and** what the operation promises to change.
A successful status or an open socket alone proves little.

For shared behavior, use separate clients where that distinction matters. Read
the state through the API after an action, or check which client received the
event and what it contained. Exercise relevant failure paths too.

At this level you may use the real school inference service when the question
is whether your backend actually works with it. Use test inputs and supply the
key privately at runtime, never in Git, chat or logs. Check the promised
behavior, not an exact generated sentence. Keep live checks separately
selectable so a cluster outage does not prevent you from testing your own
logic. Document what is real, what is substituted and why.

## Optional: test through the browser

Your API tests now act as clients, but none of them clicks a button. A
browser test closes that gap: it drives the real frontend and checks what
the player sees. **Browser automation is optional for this course.** For a
production web application, we strongly recommend it for critical user
interactions that could break even with a green backend suite.

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

[Playwright](https://github.com/microsoft/playwright) is an open-source tool
that can drive a real browser locally, even without a desktop window. Its
[testing guide](https://playwright.dev/docs/best-practices) shows how to find
controls and use assertions that retry while the page updates.

## Make a change and leave the suite green

Pick one useful change to your own application. Agree on its intended effect
before asking the agent to implement it. Add or update the tests for that
effect. If an older test fails, decide whether the agreement really changed
or the code is wrong. Do not weaken an assertion just to make it pass.

Provide **one documented command** that runs the routine unit, integration
and API tests on development, including the API suite's setup and cleanup.
A failed assertion must
give the command a nonzero exit code. Run it twice: both runs should pass
without manual resets or reliance on a previous test's data. Finish with
working code and passing tests, not a broken commit for the next assignment.

<a href="assets/14-pytest-green.png"><img src="assets/screenshots/14-pytest-green.png" alt="Terminal on the development server running .venv-llm/bin/python -m pytest -q tests and reporting 44 passed in 28.26s" width="785"></a>

The instructor's game finished with `44 passed`. Your game will have its own
set of tests.

## Explain your architecture

<a href="assets/14-example-backend.svg"><img src="assets/14-example-backend.svg" alt="Simple example: the instructor's browser game sends chat requests to a backend with separate modules for chat, sessions, tools and documents" align="right" width="340"></a>

Put an **Architecture** section in your game's top-level README, or link from
there to a document in the repository. Include a **vector diagram** of your
actual backend. Use the real module names and label the arrows with what is
called or exchanged. A reader should be able to follow a frontend interaction
through the public API, into the responsible modules and back to the browser.

In the simple example on the right, follow the two arrows out of
`game_tools.py`: a question about the player's score needs session state,
while a question about the rules needs the document catalog. That distinction
explains why those modules are separate. Draw the boundaries that make sense
for **your** application, not the ones in the example.

Alongside the diagram, explain each module's responsibility and interface.
Document the public operations, including requests or messages, responses and
relevant errors. Link to the tests that verify those contracts. Include the
local test command, any prerequisites and how to select live checks. Explain
how the frontend works even if you do not automate its tests.

Review the diff and check the diagram against the code with your agent.
Update project memory and commit the reviewed work to your project branch.

At the oral defense, use your diagram to explain **how your backend fits
together and how you know it works**. Describe what the main modules are
responsible for and how they work together. Use an example from your test
suite to explain what you checked at the module level and what you verified
through the API. The focus is on your design and testing choices, not on
remembering implementation details.
