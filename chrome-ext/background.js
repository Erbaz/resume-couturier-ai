function configureSidePanelBehavior() {
  if (!chrome.sidePanel?.setPanelBehavior) {
    console.warn("sidePanel API is unavailable in this browser/context.");
    return;
  }
  chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: true })
    .catch((err) => {
      console.warn("Failed to configure side panel behavior:", err);
    });
}

chrome.runtime.onInstalled.addListener(() => {
  configureSidePanelBehavior();
});

chrome.runtime.onStartup?.addListener(() => {
  configureSidePanelBehavior();
});
