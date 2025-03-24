### Okay so upon reading up i came up with the main things that our app needs to have
1. Doesn't appear in app drawer
2. Doesn't appear in list of running apps
3. Doesn't appear under recently opened apps
4. Only shows up in settings
5. APK installation
6. No UI
7. Gestures for activation

We can't use React-Native to build the app since it does not have native android code editing services, and a lot of prerequisites which we cannot work around + it can't do proper gesture handling

# GPT suggests we stick to native Java / Kotlin or Flutter (dart)

Betweel Native or Flutter, the implementaion is equally hard, the only difference is the reliance on **plugins in flutter.** Which is a little difficult, but definitely possible.

Toh i think we should go with flutter. It'll make the development a lot lighter, and definitely 100x easier than learning native android. + Flutter is a good skill to have.

And also android studio is a bitch.
