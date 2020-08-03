export const searchFile = async filename => {
  const files = await window.eel.search_file(filename)();
  return files;
};

export const openFile = path => {
  window.eel.open_file(path);
};

export const getSettings = async () => {
  const settings = await window.eel.get_settings()();
  return settings;
};

export const saveSettings = async settings => {
  const error = await window.eel.update_settings(settings)();
  return error;
};
