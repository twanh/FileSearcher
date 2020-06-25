
export const searchFile = async (filename) => {
  const files = await window.eel.search_file(filename)()
  return files
}