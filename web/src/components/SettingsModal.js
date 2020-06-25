import React, { useState, useRef } from 'react'

function SettingsModal() {

  const [isOpen, setIsOpen] = useState(false)
  const modal = useRef(null)

  const handleSave = () => {
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