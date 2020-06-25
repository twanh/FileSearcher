import React, { useState } from 'react';
import "bulma/css/bulma.css"
import { css } from '@emotion/core'

import { searchFile, openFile } from '../eel'
import SettingsModal from './SettingsModal';

const FolderIcon = () => <span className="icon  is-small"><i className='fas fa-folder' aria-hidden="true" /></span>
const FileIcon = () => <span className="icon  is-small"><i className='fas fa-file' aria-hidden="true" /></span>
const DocIcon = () => <span className="icon  is-small"><i className='fas fa-file-word' aria-hidden="true" /></span>
const ImageIcon = () => <span className="icon  is-small"><i className='fas fa-file-image' aria-hidden="true" /></span>

function FileItem({ file, handleClick }) {
  return (
    <a
      className="panel-block	"
      href="#_"
      css={css`cursor: pointer;`}
      onClick={_ => handleClick(file.path)}
    >
      <span className="panel-icon has-text-info">
        {file.file_type === 'dir' && <FolderIcon />}
        {file.file_type === 'img' && <ImageIcon />}
        {file.file_type === 'doc' && <DocIcon />}
        {file.file_type === 'any' && <FileIcon />}
      </span>
      {file.name} <span style={{ marginLeft: 5, color: "gray", fontSize: 10 }}>{`.../${file.path.split("\\").slice(-2).join('/')}`}</span>
    </a>
  )
}

function App() {

  // const [currentTab, setCurrentTab] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [files, setFiles] = useState([])

  // Get the files and add them to the state
  const getAndSetFiles = async () => {
    const result = await searchFile(searchQuery)
    setFiles(result)
  }

  // Handle the on change event on the main (search) input
  const handleSearchChange = (e) => {
    e.preventDefault()
    setSearchQuery(e.target.value)
    // We check if the query is larger then 4 because otherwise the result will be to 
    // large and create a performance hit (see issue: #1)
    if (searchQuery.length >= 4) {
      getAndSetFiles()
    }
  }

  // Handle the enter press on the main input
  // If enter is pressed we should search
  const handleEnter = async (e) => {
    if (e.keyCode === 13) {
      getAndSetFiles()
    }
  }

  const handleFileItemClick = (path) => {
    openFile(path)
  }


  return (
    <div className="App">
      <nav className="panel">
        <div className="panel-block">
          <p className="control has-icons-left">
            <input className="input" type="text" onChange={e => handleSearchChange(e)} onKeyDown={e => handleEnter(e)} value={searchQuery} placeholder="Search files or use /command" />
            <span className="icon is-left">
              <i className="fas fa-search" aria-hidden="true"></i>
            </span>
          </p>
        </div>
        <div className="panel-tabs">
          <a className="is-active" href='#_'>All <FileIcon /></a>
          <a href="#_">Documents</a>
          <a href="#_">Images</a>
          <SettingsModal />
        </div>
        {files.length > 0 ? files.map(file => (
          <FileItem file={file} handleClick={file_path => handleFileItemClick(file_path)} key={file.path} />
        )) : (
            <p className="panel-block has-text-centered	 ">Start searching to find!</p>
          )}

      </nav>
    </div >
  );
}

export default App;
