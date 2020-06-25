import React, { useState } from 'react';
import "bulma/css/bulma.css"

import { searchFile } from '../eel'

const FolderIcon = () => <span className="icon  is-small"><i className='fas fa-folder' aria-hidden="true" /></span>
const FileIcon = () => <span className="icon  is-small"><i className='fas fa-file' aria-hidden="true" /></span>
const DocIcon = () => <span className="icon  is-small"><i className='fas fa-file-word' aria-hidden="true" /></span>
const ImageIcon = () => <span className="icon  is-small"><i className='fas fa-file-image' aria-hidden="true" /></span>

function App() {

  const [currentTab, setCurrentTab] = useState('all')
  const [searchQuery, setSearchQuery] = useState('Search files or use /command')
  const [files, setFiles] = useState([])

  const handleSearchChange = async (e) => {
    e.preventDefault()
    setSearchQuery(e.target.value)
    const result = await searchFile(searchQuery)
    setFiles(result)
  }

  return (
    <div className="App">
      <nav className="panel">
        <div className="panel-block">
          <p className="control has-icons-left">
            <input className="input" type="text" onChange={e => handleSearchChange(e)} value={searchQuery} placeholder="Search files or use /command" />
            <span className="icon is-left">
              <i className="fas fa-search" aria-hidden="true"></i>
            </span>
          </p>
        </div>
        <p className="panel-tabs">
          <a className="is-active">All <FileIcon /></a>
          <a>Documents</a>
          <a>Images</a>

        </p>
        {files.length > 0 ? files.map(file => (
          <span className="panel-block" >
            <span className="panel-icon">
              {file.file_type === 'dir' && <FolderIcon />}
              {file.file_type === 'img' && <ImageIcon />}
              {file.file_type === 'doc' && <DocIcon />}
              {file.file_type === 'any' && <FileIcon />}
            </span>
            {file.name}
          </span>
        )) : (
            <p className="panel-block has-text-centered	 ">Start searching to find!</p>
          )}

      </nav>
    </div >
  );
}

export default App;
