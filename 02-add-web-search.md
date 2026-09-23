# 02 — Add web search to your AI assistant

> This assignment is a draft. The setup below has been checked; the first live
> search with our Qwen model will be added after it has been tested.

Your assistant can help you build the game, but it should not guess when you
need current information. Give VS Code Chat a web-search tool so you can look
up documentation and check what it finds. This adds search to your **coding
assistant**, not to the game you are building.

## Install the VS Code extension

In the VS Code window where you use the Mechatronics model, open **Extensions**
and search for **Web Search for Copilot**.

[![Search for Web Search for Copilot in VS Code Extensions](assets/02-extension-search.png)](assets/02-extension-search.png)

Check that the extension is published by **Microsoft**, then install it.
You can also open its [VS Code Marketplace page](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-websearchforcopilot).

[![The Web Search for Copilot extension by Microsoft](assets/02-extension-listing.png)](assets/02-extension-listing.png)

## Create a free Tavily account

The extension uses [Tavily](https://www.tavily.com/pricing) to search the web.
Tavily is a separate service from the Mechatronics LLM cluster, so it needs
its own account and API key. Create a Tavily account and continue through its
welcome screens.

[![Tavily welcome screen](assets/02-tavily-welcome.png)](assets/02-tavily-welcome.png)

When asked to choose a plan, select **Continue on Free**. No credit card was
requested during our walkthrough. The free-credit amount and appearance of
this page may change, so use the current options rather than treating the
screenshot as a pricing promise. You do not need a paid plan for this exercise.

[![Tavily plan selection with Continue on Free](assets/02-tavily-free-plan.png)](assets/02-tavily-free-plan.png)

## Find your Tavily API key

Once you reach Tavily's **Getting started** page, use **Manage keys** to find
your API key. This is *not* your Mechatronics LLM key. Keep both keys private:
do not paste them into a chat message, a screenshot, or your game project.

[![Tavily Getting started page with Manage keys](assets/02-tavily-getting-started.png)](assets/02-tavily-getting-started.png)

You can ignore Tavily's generic **Copy prompt** step. We are connecting search
through the VS Code extension, not asking the coding assistant to install it.

<!-- Add the key-entry and live-search steps after verifying them with Qwen in VS Code Chat. -->
