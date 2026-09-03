# Reddit and Discord playbook

The rule: you are a developer who answers rejection questions, and you mention shipcheck only when it would actually have caught the problem. Never post the tool cold. Never let an agent post for you.

## Listening setup (free)

F5Bot (f5bot.com) keywords, all lowercase:
- app rejected
- app store rejection
- guideline 2.1
- guideline 4.2
- guideline 4.3
- guideline 3.1.2
- guideline 5.1.1
- itms-91061
- privacy manifest
- resolution center
- expo rejected
- react native rejected
- google play rejected
- data safety rejected

Alerts arrive by email. Forward interesting ones into a Claude.ai chat with the reply prompt below, review, then post yourself.

## Reply drafting prompt

"Here is a Reddit post from a developer whose app was rejected. Write a reply as a fellow indie developer. Diagnose the likely guideline clause and give the concrete fix first. Only if shipcheck would have caught this specific issue, add one sentence at the end: 'I built a Claude Code plugin that catches this class of thing before submission if you want to try it: [link].' If shipcheck would not have caught it, do not mention it. Under 150 words. No bullet points."

## Subreddit rules that matter

- r/iOSProgramming: self-promo only with genuine discussion; profile history checked. Reply in threads; don't post the tool as a link post until you have real comment history.
- r/reactnative and r/expo: link posts about tools allowed if you're an active member; put the useful content in the post body, not behind the link.
- r/androiddev: strict. Comments only.
- r/SideProject and r/ClaudeCode: promotion allowed. One launch post each, with the free-scan angle up front.
- Expo Discord and React Native Discord: use #showcase or #self-promo channels only, once.

## Ratio

At least nine helpful comments with no link for every one that mentions shipcheck. Track it in a spreadsheet; mods do.
