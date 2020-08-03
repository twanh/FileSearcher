# FileSearcher

## Migrate to Vue:

- [x] Cleanup the vue install
- [ ] Setup the connection between backend and frontend
  - [ ] Connect the websocket
  - [ ] Port over the connected functions
    - searchFile
    - openFile
    - getSettings
    - saveSettings
- [ ] Create Layout
  - [ ] Install buetify (bulma 4 vue component wrapper)
    - Setup beutify
  - [ ] Search bar
  - [ ] Tab bar
  - [ ] Results section
  - [ ] Settings popup
- [ ] Have the layout interact with the backend (make it functional 😀)
  - [ ] Searching
    - Auto start searching when 4 character are typed
    - Search on `enter` press (`submit` event).
  - [ ] Opening files
  - [ ] settings
    - Open settings modal
    - Change and save settings

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
