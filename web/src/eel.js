
export const searchFile = async (filename) => {
  const files = await window.eel.search_file(filename)()
  return files
}


export const openFile = (path) => {
  window.eel.open_file(path)
}