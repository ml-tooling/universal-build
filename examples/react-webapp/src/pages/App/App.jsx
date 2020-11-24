import React from 'react';

import { useTranslation } from 'react-i18next';

import logo from './logo.svg';
import './App.css';

import Button from '../../components/Button';

function App() {
  const { t } = useTranslation();

  /**
   * This is an example function in arrow notation and with typed JSDoc.
   * @param {number} a Summand 1.
   * @param {number} b Summand 2.
   */
  const exampleArrowFunctionWithJSDoc = (a, b) => {
    return a + b;
  };
  exampleArrowFunctionWithJSDoc();

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          {t('edit-and-reload', {
            defaultValue: '',
            file: 'src/pages/App/App.jsx',
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          {t('learn')} React
        </a>
        <Button />
      </header>
    </div>
  );
}

export default App;
