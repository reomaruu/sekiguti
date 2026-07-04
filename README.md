# Sekiguti iOS

This repository is an iOS WebView rebuild of the uploaded macOS Electron app.

## What was converted

The original `my-transparent-app.app` was a macOS Electron application. Its `app.asar` contained:

- `index.html`
- `kibou.css`
- `main.js`
- `package.json`

The iOS version keeps the visible HTML/CSS UI and wraps it with Capacitor for iOS.

## Important limitations

Electron desktop features cannot be converted directly to iOS:

- `BrowserWindow.transparent` does not exist on iOS.
- `frame: false` and draggable desktop windows do not exist on iOS.
- `alwaysOnTop` does not exist for normal iOS apps.
- `window.close()` cannot close an iOS app, so the button now hides the card instead.

## Local build on Mac

```bash
npm install
npx cap add ios
npx cap sync ios
cd ios/App
pod install
open App.xcworkspace
```

Then select a simulator in Xcode and run the `App` scheme.

## Codemagic

`codemagic.yaml` contains an unsigned simulator workflow.

This produces a `.app` artifact for iOS Simulator. It does **not** produce an installable device IPA, because real iPhone/iPad installation requires Apple code signing and a provisioning profile.
