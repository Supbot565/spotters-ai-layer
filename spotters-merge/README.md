# Spotters: AI layer merged into your codebase

Everything here applies to the Spotters repo (`sharvanisarapady-sudo/spotters`). Nothing is pushed to it from here.

## 1. Apply the code changes
From the root of the Spotters repo:

    git checkout -b ai-judge
    git apply path/to/spotters-ai-judge.patch

What it changes:
- `server/services/providers/geminiJudge.js` (new): AI check for synonyms ("lobar pneumonia" for "pneumonia") and vague answers. Runs only when the strict match said "incorrect", only in Navigation AI. Test scoring is untouched. If the AI call fails, the strict result is used.
- `server/services/aiService.js`: calls the judge. Correct (AI-checked) flips to correct; partial sets `partial: true` (verdict stays `incorrect`, so no DB change).
- `server/services/providers/geminiProvider.js` and the Groq prompt in `aiService.js`: longer 3-paragraph explanations, still only using the recorded case text.
- `client/src/pages/NavigationAICase.jsx`: amber "Partially correct" box; paragraphs keep their line breaks.
- `client/src/components/practice/ImageViewer.jsx`: MRI-style slice scrolling (mouse wheel, arrow keys, slider) when a case has more than one image.

Run with `AI_PROVIDER=gemini` and `AI_API_KEY=<your Gemini key>` in `server/.env`.

## 2. Optional: mock MRI quiz (fake images, for testing the scroller)
    python mock-mri/make_mock_mri.py server/uploads/cases montage.png   # needs pillow + numpy
    mysql -u root -p spotters_db < mock-mri/mock_mri.sql

Creates 3 cases (right frontal lesion, left hemisphere wedge, enlarged ventricles; 20 slices each) in Neuroradiology and a "Mock MRI Quiz" (block 99, 60 s per question). The images are synthetic and stamped "MOCK - NOT REAL". The case text is a draft and needs medical review.
