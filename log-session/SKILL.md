---
name: log-session
description: "Adds the current Claude chat (cloud or VS Code) to Joe's Instances Manager in Notion, or updates its row if it is already there. Use when Joe says 'log this session', 'log this instance', 'add this chat to the instances manager', 'track this session', 'save this session to Notion' or '/log-session', and before Joe closes or deletes a chat."
---

# Log Session

Joe keeps a list of every Claude chat he has running in Notion, on the page called "Instances Manager". On his PC, "refresh the instances manager" fills it from the chats open in VS Code. That misses cloud chats on claude.ai. This skill adds the chat you are in, wherever it runs.

## Where it lives

- Page: Instances Manager, https://app.notion.com/p/417a26a143ba81e18389cf6fc92f3e72
- Database: Claude Code instances, data source `collection://ba530ced-3fd4-4540-963a-7cc18f7ae243`

Fetch the data source first and use its property names exactly. If it can't be found, search Notion for "Claude Code instances".

## Steps

1. Find this chat's ID.
   - Cloud chat: call `get_session` with no ID. Use the `session_...` ID. The resume link is `https://claude.ai/code/<session id>`.
   - VS Code chat: use the session ID from the transcript file name. Copy the resume link format from an existing row.
2. Look for an existing row with that Session ID. If there is one, update it. Never make a duplicate.
3. Fill in the row:

| Property | What to put |
|---|---|
| Name | What the chat is about, in under 8 words |
| Category | One of: VektorMark, Website builds, Skills & side projects, Other |
| Folder | The project folder, or "Cloud chat on claude.ai (not in VS Code)" |
| Overview | 2 or 3 plain-English sentences: what was done, then what's still open |
| Resume | The resume link from step 1 |
| Session ID | The ID from step 1 |
| Tickets | Jira keys the chat created or worked on, comma separated |
| Last active | Today's date |
| Closed | Unticked, unless Joe says he's closing the chat |

4. Reply with one line and the link to the row.

## Rules

- Follow CLAUDE.md: plain English, no jargon, no em dashes or en dashes.
- The Overview must make sense to Joe with no other context. Say what each project is the first time you name it.
- Don't put secrets, passwords or email addresses in any field.
- For a cloud chat, tell Joe the nightly refresh may tick it as Closed, because the refresh only sees VS Code. The resume link still works.
