# Spotters AI layer

Checks a student's answer against a stored radiology case and returns a verdict plus a short explanation. It replaces the mock `aiService.js` in the Navigation AI service.

## Files
- `aiService.js` - the only file the app needs. Exports `evaluateAnswer(caseData, studentAnswer)`.
- `cases.json` - 4 sample cases (for testing only; a doctor should review them).
- `test.js` - dev check with 22 sample answers. Not part of the app.
- `.env.example` - copy to `.env` and add your own Gemini key (free at aistudio.google.com).

## Use
```js
const { evaluateAnswer } = require('./aiService');
const result = await evaluateAnswer(caseData, studentAnswer);
// { verdict: 'correct' | 'partial' | 'wrong', missed: [...], explanation: '...' }
```
`caseData` must have `diagnosis` (string), `keyFindings` (array of strings) and optionally `commonMistakes` (array). If your MySQL columns are named differently, map them first.

It uses only the facts in `caseData`; it does not look at the image. Needs Node 20.12+ (uses built-in `fetch` and `.env` loading), no npm packages.

## Behaviour
- Retries up to 3 times on Gemini 503/429, 20 s timeout per request, throws an Error on failure (catch it in your route).
- Run `node test.js` after changing the prompt or model (takes about 1.5 minutes; free-tier limits apply).
- Never commit `.env`.
