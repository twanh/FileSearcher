import React, { useState, useRef, useEffect } from 'react'
import { getSettings, saveSettings } from '../eel'

function SettingsModal() {

  const [isOpen, setIsOpen] = useState(false)
  const [hotkey, setHotkey] = useState("")
  const [root_dir, setRootDir] = useState("")
  const [search_timeout, setTimeout] = useState("")
  const modal = useRef(null)

  useEffect(() => {
    getSettings().then(settings => {
      console.log(settings)
      setHotkey(settings.hotkey)
      setRootDir(settings.root_dir)
      setTimeout(settings.search_timeout)
    })
  }, [])

  const handleSave = async () => {
    const error = await saveSettings({
      hotkey,
      root_dir,
      search_timeout
    })
    if (error !== "") {
      console.log(error)
    }
    toggleModal()
  }

  const toggleModal = () => {
    if (!isOpen) {
      modal.current.classList.add('is-active')
      setIsOpen(true)
      return
    }
    setIsOpen(false)
    modal.current.classList.remove('is-active')
  }

  const handleHotkeyChange = (e) => {
    setHotkey(e.target.value)
  }


  const handleRootDirChange = (e) => {
    setRootDir(e.target.value)
  }

  const handleTimeoutChange = (e) => {
    setTimeout(e.target.value)
  }



  return (
    <React.Fragment>
      <a href="#_" className='link' onClick={_ => toggleModal()}>
        <span className="icon is-small">
          <i className="fas fa-cog"></i>
        </span>
      </a>
      <div className="modal" ref={modal}>
        <div className="modal-background"></div>
        <div className="modal-card">
          <header className="modal-card-head">
            <p className="modal-card-title">Settings</p>
            <button onClick={_ => toggleModal()} className="delete" aria-label="close"></button>
          </header>
          <section className="modal-card-body">
            <form>
              <div className="field">
                <label className="label">Hotkey</label>
                <div className="control">
                  <input type="text" className="input" value={hotkey} onChange={e => handleHotkeyChange(e)} />
                </div>
                <p className="help">The shortcut for opening the application. Format: Key+Key. E.g.: Ctrl+Shift+Alt+Space</p>
              </div>
              <div className="field">
                <label className="label">Main directory</label>
                <div className="control">
                  <input type="text" className="input" value={root_dir} onChange={e => handleRootDirChange(e)} />
                </div>
                <p className="help">The directory all the files you want to search are located in.</p>
              </div>
              <div className="field">
                <label className="label">Fetch timeout</label>
                <div className="control">
                  <input type="number" className="input" step="0.1" value={search_timeout} onChange={e => handleTimeoutChange(e)} />
                </div>
                <p className="help">The timeout between re creating the folder structure</p>
              </div>
            </form>
          </section>
          <footer className="modal-card-foot">
            <button className="button is-success" onClick={_ => handleSave()}>Save changes</button>
            <button className="button" onClick={_ => toggleModal()}>Cancel</button>
          </footer>
        </div>
      </div>
    </React.Fragment>
  )

}


export default SettingsModal